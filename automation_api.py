from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel
import uuid
from datetime import datetime
import sys

# Importar suas automações existentes
from automacao_clientes_corrigida_testes import processar_clientes
from automacao_carros_corrigida_testes import processar_automoveis

app = FastAPI(
    title="API Automação Seguros",
    version="2.0.0"
)

# CORS para n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Armazenar tarefas em memória (SIMPLES!)
tarefas_memoria = {}

# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
def home():
    """Health check"""
    return {
        "status": "online",
        "tarefas_ativas": len([t for t in tarefas_memoria.values() if t["status"] in ["pendente", "processando"]]),
        "total_tarefas": len(tarefas_memoria)
    }

@app.post("/api/clientes")
async def api_cadastrar_clientes(request: Union[List[Dict], Dict], background_tasks: BackgroundTasks):
    """
    Recebe JSON do n8n e processa clientes
    
    ACEITA 2 FORMATOS:
    
    Formato 1 - ARRAY DIRETO (n8n):
    [
      {
        "output": {
          "datos_cliente": {...}
        }
      }
    ]
    
    Formato 2 - COM ENVELOPE:
    {
      "clientes": [...]
    }
    """
    # Detectar formato e extrair dados
    if isinstance(request, list):
        # Formato direto do n8n (ARRAY)
        dados_clientes = request
        print("📡 Formato detectado: ARRAY DIRETO (n8n)")
    elif isinstance(request, dict) and "clientes" in request:
        # Formato com envelope
        dados_clientes = request["clientes"]
        print("📦 Formato detectado: OBJETO COM ENVELOPE")
    else:
        return {"erro": "Formato inválido. Envie array ou objeto com chave 'clientes'"}
    
    tarefa_id = str(uuid.uuid4())[:8]  # ID curto
    
    # Criar registro da tarefa
    tarefas_memoria[tarefa_id] = {
        "tarefa_id": tarefa_id,
        "tipo": "clientes",
        "status": "pendente",
        "total": len(dados_clientes),
        "processados": 0,
        "criado_em": datetime.now().isoformat(),
        "atualizado_em": datetime.now().isoformat()
    }
    
    print(f"✅ Nova tarefa criada: {tarefa_id} ({len(dados_clientes)} clientes)")
    
    # Processar em background
    background_tasks.add_task(
        processar_clientes_background,
        tarefa_id,
        dados_clientes
    )
    
    return {
        "tarefa_id": tarefa_id,
        "status": "pendente",
        "mensagem": f"Processando {len(dados_clientes)} cliente(s)",
        "consultar_status": f"/api/status/{tarefa_id}"
    }

@app.post("/api/carros")
async def api_cadastrar_carros(request: Union[List[Dict], Dict], background_tasks: BackgroundTasks):
    """
    Recebe JSON do n8n e processa carros
    
    ACEITA 2 FORMATOS:
    
    Formato 1 - ARRAY DIRETO (n8n):
    [
      {
        "output": {
          "datos_poliza": {...},
          ...
        }
      }
    ]
    
    Formato 2 - COM ENVELOPE:
    {
      "carros": [...]
    }
    """
    # Detectar formato
    if isinstance(request, list):
        dados_carros = request
        print("📡 Formato detectado: ARRAY DIRETO (n8n)")
    elif isinstance(request, dict) and "carros" in request:
        dados_carros = request["carros"]
        print("📦 Formato detectado: OBJETO COM ENVELOPE")
    else:
        return {"erro": "Formato inválido. Envie array ou objeto com chave 'carros'"}
    
    tarefa_id = str(uuid.uuid4())[:8]
    
    tarefas_memoria[tarefa_id] = {
        "tarefa_id": tarefa_id,
        "tipo": "carros",
        "status": "pendente",
        "total": len(dados_carros),
        "processados": 0,
        "criado_em": datetime.now().isoformat(),
        "atualizado_em": datetime.now().isoformat()
    }
    
    print(f"✅ Nova tarefa criada: {tarefa_id} ({len(dados_carros)} carros)")
    
    background_tasks.add_task(
        processar_carros_background,
        tarefa_id,
        dados_carros
    )
    
    return {
        "tarefa_id": tarefa_id,
        "status": "pendente",
        "mensagem": f"Processando {len(dados_carros)} carro(s)",
        "consultar_status": f"/api/status/{tarefa_id}"
    }

@app.get("/api/status/{tarefa_id}")
def obter_status(tarefa_id: str):
    """Consultar status de uma tarefa"""
    if tarefa_id not in tarefas_memoria:
        return {"erro": "Tarefa não encontrada", "tarefa_id": tarefa_id}
    
    return tarefas_memoria[tarefa_id]

@app.get("/api/tarefas")
def listar_tarefas(status: Optional[str] = None):
    """Listar todas as tarefas"""
    tarefas = list(tarefas_memoria.values())
    
    if status:
        tarefas = [t for t in tarefas if t["status"] == status]
    
    # Ordenar por data (mais recentes primeiro)
    tarefas.sort(key=lambda x: x["criado_em"], reverse=True)
    
    return {"total": len(tarefas), "tarefas": tarefas}

# ============================================
# FUNÇÕES DE BACKGROUND
# ============================================

def processar_clientes_background(tarefa_id: str, dados_json: List[Dict]):
    """
    Executa automação de clientes em background
    Chama diretamente a função processar_clientes()
    """
    try:
        print(f"🔄 Iniciando processamento da tarefa {tarefa_id}")
        
        # Atualizar status
        tarefas_memoria[tarefa_id]["status"] = "processando"
        tarefas_memoria[tarefa_id]["atualizado_em"] = datetime.now().isoformat()
        
        # ⭐ AQUI É QUE A MÁGICA ACONTECE!
        # Chamar SUA automação passando os dados
        processar_clientes(dados_json=dados_json)
        
        # Sucesso!
        tarefas_memoria[tarefa_id]["status"] = "concluido"
        tarefas_memoria[tarefa_id]["processados"] = tarefas_memoria[tarefa_id]["total"]
        tarefas_memoria[tarefa_id]["atualizado_em"] = datetime.now().isoformat()
        
        print(f"✅ Tarefa {tarefa_id} concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na tarefa {tarefa_id}: {e}")
        import traceback
        traceback.print_exc()
        
        tarefas_memoria[tarefa_id]["status"] = "erro"
        tarefas_memoria[tarefa_id]["erro"] = str(e)
        tarefas_memoria[tarefa_id]["atualizado_em"] = datetime.now().isoformat()

def processar_carros_background(tarefa_id: str, dados_json: List[Dict]):
    """
    Executa automação de carros em background
    """
    try:
        print(f"🔄 Iniciando processamento da tarefa {tarefa_id}")
        
        tarefas_memoria[tarefa_id]["status"] = "processando"
        tarefas_memoria[tarefa_id]["atualizado_em"] = datetime.now().isoformat()
        
        # ⭐ Chamar automação de carros
        processar_automoveis(dados_json=dados_json)
        
        tarefas_memoria[tarefa_id]["status"] = "concluido"
        tarefas_memoria[tarefa_id]["processados"] = tarefas_memoria[tarefa_id]["total"]
        tarefas_memoria[tarefa_id]["atualizado_em"] = datetime.now().isoformat()
        
        print(f"✅ Tarefa {tarefa_id} concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro na tarefa {tarefa_id}: {e}")
        import traceback
        traceback.print_exc()
        
        tarefas_memoria[tarefa_id]["status"] = "erro"
        tarefas_memoria[tarefa_id]["erro"] = str(e)
        tarefas_memoria[tarefa_id]["atualizado_em"] = datetime.now().isoformat()

# ============================================
# INICIAR SERVIDOR
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════╗
    ║   API SUPER SIMPLES - Automação Seguros  ║
    ╚═══════════════════════════════════════════╝
    
    🌐 API: http://localhost:8000
    📚 Docs: http://localhost:8000/docs
    
    📡 Endpoints:
    • POST /api/clientes  → Cadastrar clientes
    • POST /api/carros    → Cadastrar carros
    • GET  /api/status/{id} → Ver status
    • GET  /api/tarefas   → Listar todas
    
    ✅ ACEITA FORMATO DIRETO DO n8n (array)!
    ✅ ACEITA FORMATO COM ENVELOPE (objeto)!
    ⚡ Sem SQLite - Armazena em memória
    
    Ctrl+C para parar
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
