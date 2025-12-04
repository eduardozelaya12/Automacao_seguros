# 🚀 Guia: Transformando Automação em API

## 📋 Visão Geral

Você tem 2 scripts que funcionam localmente:
- `automacao_clientes_corrigida.py` ✅
- `automacao_carros_corrigida.py` ✅

Objetivo: Transformar em API para chamar remotamente (de n8n, por exemplo)

## 🏗️ Arquitetura Proposta

```
┌─────────────────────────────────────────────────────────────┐
│                     SERVIDOR WINDOWS                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ API FastAPI (main.py)                               │    │
│  │ Porta 8000                                          │    │
│  │                                                      │    │
│  │ Endpoints:                                          │    │
│  │  POST /api/clientes  ← Recebe JSON de clientes    │    │
│  │  POST /api/carros    ← Recebe JSON de carros      │    │
│  │  GET  /api/status/{id}                             │    │
│  └────────────────────────────────────────────────────┘    │
│                         ↓                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Sistema de Filas                                    │    │
│  │ - Gerencia tarefas pendentes                       │    │
│  │ - Processa uma por vez                             │    │
│  └────────────────────────────────────────────────────┘    │
│                         ↓                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Worker (processa em background)                     │    │
│  │ - Chama automacao_clientes_corrigida.py           │    │
│  │ - Chama automacao_carros_corrigida.py             │    │
│  └────────────────────────────────────────────────────┘    │
│                         ↓                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ PyAutoGUI + Velneo vClient                         │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
         ↑ HTTP POST                      ↓ Webhook callback
┌────────────────────┐           ┌────────────────────┐
│  n8n ou Cliente    │           │  Notificação       │
│  Remoto            │           │  (quando concluir) │
└────────────────────┘           └────────────────────┘
```

## 🔧 Implementação Simplificada

### Passo 1: Criar API FastAPI Simples

Arquivo: `api_simples.py`

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
import json
from datetime import datetime

# Importar suas automações
from automacao_clientes_corrigida import processar_clientes
from automacao_carros_corrigida import processar_automoveis

app = FastAPI(title="API Automação Seguros")

# Armazenar tarefas em memória (simples)
tarefas = {}

class ClienteInput(BaseModel):
    clientes: List[Dict[str, Any]]

class CarroInput(BaseModel):
    carros: List[Dict[str, Any]]

@app.post("/api/clientes")
async def cadastrar_clientes(request: ClienteInput, background_tasks: BackgroundTasks):
    """Cadastrar clientes via API"""
    tarefa_id = str(uuid.uuid4())
    
    # Salvar JSON temporário
    with open('clientes_temp.json', 'w', encoding='utf-8') as f:
        json.dump(request.clientes, f, ensure_ascii=False, indent=2)
    
    # Criar tarefa
    tarefas[tarefa_id] = {
        "status": "pendente",
        "tipo": "clientes",
        "total": len(request.clientes),
        "criado_em": datetime.now().isoformat()
    }
    
    # Processar em background
    background_tasks.add_task(executar_automacao_clientes, tarefa_id)
    
    return {"tarefa_id": tarefa_id, "status": "pendente"}

@app.post("/api/carros")
async def cadastrar_carros(request: CarroInput, background_tasks: BackgroundTasks):
    """Cadastrar carros via API"""
    tarefa_id = str(uuid.uuid4())
    
    with open('carros_temp.json', 'w', encoding='utf-8') as f:
        json.dump(request.carros, f, ensure_ascii=False, indent=2)
    
    tarefas[tarefa_id] = {
        "status": "pendente",
        "tipo": "carros",
        "total": len(request.carros),
        "criado_em": datetime.now().isoformat()
    }
    
    background_tasks.add_task(executar_automacao_carros, tarefa_id)
    
    return {"tarefa_id": tarefa_id, "status": "pendente"}

@app.get("/api/status/{tarefa_id}")
async def obter_status(tarefa_id: str):
    """Consultar status de uma tarefa"""
    if tarefa_id not in tarefas:
        return {"erro": "Tarefa não encontrada"}
    return tarefas[tarefa_id]

def executar_automacao_clientes(tarefa_id: str):
    """Executar automação de clientes em background"""
    try:
        tarefas[tarefa_id]["status"] = "processando"
        # Executar sua automação
        processar_clientes()
        tarefas[tarefa_id]["status"] = "concluido"
    except Exception as e:
        tarefas[tarefa_id]["status"] = "erro"
        tarefas[tarefa_id]["erro"] = str(e)

def executar_automacao_carros(tarefa_id: str):
    """Executar automação de carros em background"""
    try:
        tarefas[tarefa_id]["status"] = "processando"
        processar_automoveis()
        tarefas[tarefa_id]["status"] = "concluido"
    except Exception as e:
        tarefas[tarefa_id]["status"] = "erro"
        tarefas[tarefa_id]["erro"] = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Passo 2: Adaptar Automações para Ler JSON Temporário

Modificar `automacao_clientes_corrigida.py`:

```python
# Linha 77 - onde carrega o JSON
try:
    # Tentar carregar JSON temporário da API primeiro
    json_file = 'clientes_temp.json' if os.path.exists('clientes_temp.json') else 'clientes.json'
    
    with open(json_file, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # ... resto do código
```

### Passo 3: Instalar Dependências

```bash
pip install fastapi uvicorn pydantic
```

### Passo 4: Iniciar API

```bash
python api_simples.py
```

API disponível em: `http://localhost:8000`
Documentação: `http://localhost:8000/docs`

## 📡 Como Usar a API

### Exemplo 1: Cadastrar Clientes

```bash
curl -X POST http://localhost:8000/api/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "clientes": [
      {
        "output": {
          "datos_cliente": {
            "numero_cliente": "123456",
            "assegurado": "SILVA, JOÃO",
            "tipo": "Particular",
            "celular": "099111111"
          }
        }
      }
    ]
  }'
```

**Resposta:**
```json
{
  "tarefa_id": "abc-123-def-456",
  "status": "pendente"
}
```

### Exemplo 2: Consultar Status

```bash
curl http://localhost:8000/api/status/abc-123-def-456
```

**Resposta:**
```json
{
  "status": "concluido",
  "tipo": "clientes",
  "total": 1,
  "criado_em": "2025-12-03T16:30:00"
}
```

## 🔄 Integração com n8n

### Workflow n8n:

```
1. Webhook (recebe PDF)
   ↓
2. PDF Parser (extrai dados)
   ↓
3. Function (formata JSON)
   ↓
4. HTTP Request POST
   URL: http://SEU_IP:8000/api/clientes
   Body: {{ $json }}
   ↓
5. Webhook Response
```

### Node HTTP Request - Configuração:

- **Method**: POST
- **URL**: `http://192.168.1.100:8000/api/clientes`
- **Body**: JSON
- **Body Content**:
```json
{
  "clientes": [
    {
      "output": {
        "datos_cliente": {{ $json }}
      }
    }
  ]
}
```

## 🎯 Vantagens desta Abordagem

✅ **Simples**: Aproveita código existente  
✅ **Assíncrono**: Não bloqueia enquanto processa  
✅ **Rastreável**: Cada tarefa tem ID único  
✅ **Escalável**: Fácil adicionar mais endpoints  
✅ **Testável**: Documentação Swagger automática  

## 🚀 Próximos Passos (Opcional)

1. **Persistência**: Usar banco SQLite para tarefas
2. **Callbacks**: Notificar n8n quando concluir
3. **Logs**: Salvar logs detalhados
4. **Autenticação**: Adicionar tokens de segurança
5. **Fila Robusta**: Usar Celery ou RQ

## 🔒 Segurança

### Firewall Windows:
```powershell
New-NetFirewallRule -DisplayName "API Automacao" \
  -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### Autenticação Básica:
```python
from fastapi import Header, HTTPException

TOKEN_SECRETO = "seu-token-aqui"

@app.post("/api/clientes")
async def cadastrar_clientes(
    request: ClienteInput,
    authorization: str = Header(None)
):
    if authorization != f"Bearer {TOKEN_SECRETO}":
        raise HTTPException(status_code=401)
    # ... resto
```

## 📊 Monitoramento

Ver todas as tarefas:
```bash
curl http://localhost:8000/api/tarefas
```

Logs em tempo real:
```bash
# Adicionar logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nos endpoints:
logger.info(f"Nova tarefa criada: {tarefa_id}")
```

## ❓ FAQ

**P: Consigo processar 10 clientes de uma vez?**  
R: SIM! Apenas adicione 10 objetos no array `clientes`.

**P: A API bloqueia enquanto processa?**  
R: NÃO! Usa `BackgroundTasks` do FastAPI.

**P: Como saber quando terminou?**  
R: Consulta `/api/status/{tarefa_id}` periodicamente.

**P: Posso chamar de qualquer lugar?**  
R: SIM! Desde que tenha acesso à rede do servidor.
