"""
Banco de dados simples para gerenciar tarefas
Usa SQLite para persistência
"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading


class TarefaDB:
    """
    Gerenciador de banco de dados para tarefas de automação
    """
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "data"
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / "tarefas.db")
        
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()
    
    def _get_connection(self):
        """Obter conexão thread-safe"""
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn
    
    def _init_db(self):
        """Inicializar banco de dados"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                tarefa_id TEXT PRIMARY KEY,
                tipo TEXT NOT NULL,
                status TEXT NOT NULL,
                total_itens INTEGER NOT NULL,
                itens_processados INTEGER DEFAULT 0,
                dados TEXT NOT NULL,
                prioridade TEXT DEFAULT 'normal',
                webhook_callback TEXT,
                resultado TEXT,
                erro TEXT,
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL
            )
        """)
        
        # Índices para melhorar performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON tarefas(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tipo ON tarefas(tipo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_criado_em ON tarefas(criado_em)")
        
        conn.commit()
    
    def create_task(self, tarefa: Dict[str, Any]) -> str:
        """Criar nova tarefa"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tarefas (
                tarefa_id, tipo, status, total_itens, itens_processados,
                dados, prioridade, webhook_callback, criado_em, atualizado_em
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tarefa['tarefa_id'],
            tarefa['tipo'],
            tarefa['status'],
            tarefa['total_itens'],
            tarefa.get('itens_processados', 0),
            json.dumps(tarefa['dados'], ensure_ascii=False),
            tarefa.get('prioridade', 'normal'),
            tarefa.get('webhook_callback'),
            tarefa['criado_em'],
            tarefa['atualizado_em']
        ))
        
        conn.commit()
        return tarefa['tarefa_id']
    
    def get_task(self, tarefa_id: str) -> Optional[Dict[str, Any]]:
        """Obter tarefa por ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tarefas WHERE tarefa_id = ?", (tarefa_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def update_task(self, tarefa_id: str, updates: Dict[str, Any]):
        """Atualizar tarefa"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Preparar campos para atualização
        set_clauses = []
        values = []
        
        for key, value in updates.items():
            if key == 'resultado' or key == 'dados':
                value = json.dumps(value, ensure_ascii=False) if value else None
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        # Sempre atualizar timestamp
        if 'atualizado_em' not in updates:
            set_clauses.append("atualizado_em = ?")
            values.append(datetime.now().isoformat())
        
        values.append(tarefa_id)
        
        query = f"UPDATE tarefas SET {', '.join(set_clauses)} WHERE tarefa_id = ?"
        cursor.execute(query, values)
        conn.commit()
    
    def list_tasks(
        self,
        status: Optional[str] = None,
        tipo: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Listar tarefas com filtros"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM tarefas WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)
        
        query += " ORDER BY criado_em DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [self._row_to_dict(row) for row in rows]
    
    def count_tasks(self, status: Optional[str] = None) -> int:
        """Contar tarefas por status"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("SELECT COUNT(*) FROM tarefas WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT COUNT(*) FROM tarefas")
        
        return cursor.fetchone()[0]
    
    def delete_old_tasks(self, days: int = 30):
        """Deletar tarefas antigas"""
        from datetime import timedelta
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM tarefas WHERE criado_em < ? AND status IN ('concluido', 'erro', 'cancelado')",
            (cutoff_date,)
        )
        
        deleted_count = cursor.rowcount
        conn.commit()
        
        return deleted_count
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Converter linha do SQLite para dicionário"""
        result = dict(row)
        
        # Parsear JSON
        if result.get('dados'):
            result['dados'] = json.loads(result['dados'])
        
        if result.get('resultado'):
            result['resultado'] = json.loads(result['resultado'])
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Obter estatísticas gerais"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total por status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM tarefas
            GROUP BY status
        """)
        stats['por_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Total por tipo
        cursor.execute("""
            SELECT tipo, COUNT(*) as count
            FROM tarefas
            GROUP BY tipo
        """)
        stats['por_tipo'] = {row['tipo']: row['count'] for row in cursor.fetchall()}
        
        # Total geral
        cursor.execute("SELECT COUNT(*) as total FROM tarefas")
        stats['total'] = cursor.fetchone()['total']
        
        # Taxa de sucesso
        cursor.execute("""
            SELECT
                SUM(CASE WHEN status = 'concluido' THEN 1 ELSE 0 END) as concluidos,
                SUM(CASE WHEN status = 'erro' THEN 1 ELSE 0 END) as erros
            FROM tarefas
        """)
        row = cursor.fetchone()
        total_finalizado = row['concluidos'] + row['erros']
        if total_finalizado > 0:
            stats['taxa_sucesso'] = round((row['concluidos'] / total_finalizado) * 100, 2)
        else:
            stats['taxa_sucesso'] = 0
        
        return stats
