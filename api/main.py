"""
API REST para Automação de Seguros
Recebe requisições do n8n e processa cadastros de clientes e carros
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import json
from pathlib import Path

# Importar worker de automação
import sys
sys.path.append(str(Path(__file__).parent.parent))
from api.worker import AutomacaoWorker
from api.database import TarefaDB

# Inicializar FastAPI
app = FastAPI(
    title="API de Automação de Seguros",
    description="API para automação de cadastros via n8n",
    version="1.0.0"
)

# CORS - permitir n8n fazer requisições
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instâncias globais
worker = AutomacaoWorker()
db = TarefaDB()


# ============================================
# MODELOS DE DADOS (Pydantic)
# ============================================

class DadosCliente(BaseModel):
    """Modelo para dados de cliente vindo do n8n"""
    numero_cliente: Optional[str] = None
    assegurado: str
    tipo_com_lista: str = "PARTICULAR"
    rut: Optional[str] = None
    razao_social: Optional[str] = None
    documento: Optional[str] = None
    categoria_a_confirmar: Optional[str] = None
    padron: Optional[str] = None
    telefono: Optional[str] = None
    celular: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    domicilio: Optional[str] = None
    Departamento_NOVO: Optional[str] = None
    localidad: Optional[str] = None
    codigo_postal: Optional[str] = None
    dir_cobro: Optional[str] = None
    email: Optional[str] = None
    observaciones: Optional[str] = None


class DadosCarro(BaseModel):
    """Modelo para dados de carro/apólice vindo do n8n"""
    datos_poliza: Dict[str, Any]
    datos_basicos: Dict[str, Any]
    datos_vehiculo: Dict[str, Any]
    datos_cobertura: Dict[str, Any]
    condiciones_pago: Dict[str, Any]
    datos_cliente: Dict[str, Any]


class RequestCadastroCliente(BaseModel):
    """Request para cadastrar um ou mais clientes"""
    clientes: List[DadosCliente]
    prioridade: str = "normal"  # normal, alta, baixa
    webhook_callback: Optional[str] = None  # URL para notificar quando concluir


class RequestCadastroCarro(BaseModel):
    """Request para cadastrar um ou mais carros"""
    carros: List[DadosCarro]
    prioridade: str = "normal"
    webhook_callback: Optional[str] = None


class TarefaStatus(BaseModel):
    """Status de uma tarefa"""
    tarefa_id: str
    status: str  # pendente, processando, concluido, erro
    tipo: str  # cliente, carro
    total_itens: int
    itens_processados: int
    criado_em: str
    atualizado_em: str
    resultado: Optional[Dict[str, Any]] = None
    erro: Optional[str] = None


# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "API de Automação de Seguros",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health():
    """Verificar saúde da API e componentes"""
    return {
        "api": "ok",
        "worker": "ok" if worker.is_alive() else "stopped",
        "database": "ok",
        "tarefas_pendentes": db.count_tasks("pendente"),
        "tarefas_processando": db.count_tasks("processando")
    }


@app.post("/api/clientes/cadastrar", response_model=TarefaStatus)
async def cadastrar_clientes(
    request: RequestCadastroCliente,
    background_tasks: BackgroundTasks
):
    """
    Endpoint para cadastrar clientes (chamado pelo n8n)
    
    Exemplo de payload:
    {
        "clientes": [
            {
                "assegurado": "João Silva",
                "tipo_com_lista": "PARTICULAR",
                "documento": "12345678",
                "telefono": "091234567",
                "email": "joao@email.com"
            }
        ],
        "prioridade": "alta",
        "webhook_callback": "https://seu-n8n.com/webhook/callback"
    }
    """
    try:
        # Criar tarefa
        tarefa_id = str(uuid.uuid4())
        
        tarefa_data = {
            "tarefa_id": tarefa_id,
            "tipo": "cliente",
            "status": "pendente",
            "total_itens": len(request.clientes),
            "itens_processados": 0,
            "dados": [c.dict() for c in request.clientes],
            "prioridade": request.prioridade,
            "webhook_callback": request.webhook_callback,
            "criado_em": datetime.now().isoformat(),
            "atualizado_em": datetime.now().isoformat()
        }
        
        # Salvar no banco
        db.create_task(tarefa_data)
        
        # Adicionar ao worker
        background_tasks.add_task(
            worker.process_task,
            tarefa_id=tarefa_id,
            tipo="cliente",
            dados=tarefa_data["dados"],
            callback=request.webhook_callback
        )
        
        return TarefaStatus(**tarefa_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar tarefa: {str(e)}")


@app.post("/api/carros/cadastrar", response_model=TarefaStatus)
async def cadastrar_carros(
    request: RequestCadastroCarro,
    background_tasks: BackgroundTasks
):
    """
    Endpoint para cadastrar carros/apólices (chamado pelo n8n)
    
    Exemplo de payload:
    {
        "carros": [
            {
                "datos_poliza": {"numero_poliza": "12345"},
                "datos_vehiculo": {"marca_modelo": "Toyota Corolla"},
                ...
            }
        ],
        "prioridade": "normal"
    }
    """
    try:
        tarefa_id = str(uuid.uuid4())
        
        tarefa_data = {
            "tarefa_id": tarefa_id,
            "tipo": "carro",
            "status": "pendente",
            "total_itens": len(request.carros),
            "itens_processados": 0,
            "dados": [c.dict() for c in request.carros],
            "prioridade": request.prioridade,
            "webhook_callback": request.webhook_callback,
            "criado_em": datetime.now().isoformat(),
            "atualizado_em": datetime.now().isoformat()
        }
        
        db.create_task(tarefa_data)
        
        background_tasks.add_task(
            worker.process_task,
            tarefa_id=tarefa_id,
            tipo="carro",
            dados=tarefa_data["dados"],
            callback=request.webhook_callback
        )
        
        return TarefaStatus(**tarefa_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar tarefa: {str(e)}")


@app.get("/api/tarefas/{tarefa_id}", response_model=TarefaStatus)
async def obter_status_tarefa(tarefa_id: str):
    """
    Consultar status de uma tarefa específica
    O n8n pode usar este endpoint para verificar o progresso
    """
    tarefa = db.get_task(tarefa_id)
    
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return TarefaStatus(**tarefa)


@app.get("/api/tarefas", response_model=List[TarefaStatus])
async def listar_tarefas(
    status: Optional[str] = None,
    tipo: Optional[str] = None,
    limit: int = 50
):
    """
    Listar tarefas com filtros opcionais
    """
    tarefas = db.list_tasks(status=status, tipo=tipo, limit=limit)
    return [TarefaStatus(**t) for t in tarefas]


@app.delete("/api/tarefas/{tarefa_id}")
async def cancelar_tarefa(tarefa_id: str):
    """
    Cancelar uma tarefa pendente
    """
    tarefa = db.get_task(tarefa_id)
    
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    if tarefa["status"] == "processando":
        raise HTTPException(status_code=400, detail="Tarefa já está sendo processada")
    
    db.update_task(tarefa_id, {"status": "cancelado"})
    
    return {"message": "Tarefa cancelada", "tarefa_id": tarefa_id}


@app.get("/api/logs/{tarefa_id}")
async def obter_logs_tarefa(tarefa_id: str):
    """
    Obter logs detalhados de uma tarefa
    """
    tarefa = db.get_task(tarefa_id)
    
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Ler arquivo de log se existir
    log_path = Path(__file__).parent.parent / "logs" / f"{tarefa_id}.log"
    logs = []
    
    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            logs = f.readlines()
    
    return {
        "tarefa_id": tarefa_id,
        "logs": logs,
        "tarefa": tarefa
    }


@app.post("/api/test/simulate")
async def simular_cadastro(tipo: str = "cliente"):
    """
    Endpoint de teste - simula um cadastro sem executar PyAutoGUI
    Útil para testar integração com n8n
    """
    if tipo == "cliente":
        dados_teste = {
            "clientes": [{
                "assegurado": "Teste João Silva",
                "tipo_com_lista": "PARTICULAR",
                "documento": "12345678",
                "email": "teste@example.com"
            }]
        }
    else:
        dados_teste = {
            "carros": [{
                "datos_poliza": {"numero_poliza": "TEST-001"},
                "datos_vehiculo": {"marca_modelo": "Toyota Test"},
                "datos_basicos": {},
                "datos_cobertura": {},
                "condiciones_pago": {},
                "datos_cliente": {"assegurado": "Cliente Teste"}
            }]
        }
    
    return {
        "message": "Simulação de teste",
        "tipo": tipo,
        "dados_recebidos": dados_teste,
        "status": "sucesso"
    }


# ============================================
# STARTUP E SHUTDOWN
# ============================================

@app.on_event("startup")
async def startup_event():
    """Inicializar componentes ao iniciar a API"""
    print("🚀 Iniciando API de Automação de Seguros...")
    print(f"📊 Tarefas pendentes: {db.count_tasks('pendente')}")
    print(f"⚙️  Worker status: {'OK' if worker.is_alive() else 'Iniciando...'}")
    worker.start()
    print("✅ API Online!")


@app.on_event("shutdown")
async def shutdown_event():
    """Finalizar componentes ao desligar a API"""
    print("🛑 Desligando API...")
    worker.stop()
    print("✅ API Desligada!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Apenas para desenvolvimento
        log_level="info"
    )
