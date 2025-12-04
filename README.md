# 🚗 Automação de Seguros

Sistema de automação para cadastro de clientes e veículos em sistema de seguros, com API FastAPI para integração.

## 📋 Descrição

Este projeto automatiza o processo de cadastro de clientes e veículos no sistema Velneo vClient, incluindo:

- **Automação de cadastro de clientes** (pessoa física e jurídica)
- **Automação de cadastro de veículos** (25 categorias suportadas)
- **API FastAPI** para execução assíncrona das automações
- **Sistema de filas** para processamento em background
- **Integração com n8n** via webhooks

## 🛠️ Tecnologias

- Python 3.8+
- PyAutoGUI (automação de interface)
- FastAPI (API REST)
- SQLite (banco de dados)
- Pydantic (validação de dados)

## 📁 Estrutura do Projeto

```
automacao_seguros/
├── api/                                    # API FastAPI
│   ├── __init__.py
│   ├── main.py                            # Servidor FastAPI
│   ├── worker.py                          # Worker para processamento
│   └── database.py                        # Gerenciamento de banco de dados
├── automacao_clientes_corrigida_testes.py # Script de automação de clientes
├── automacao_carros_corrigida_testes.py   # Script de automação de carros
├── clientes_exemplo_multiplos.json        # Exemplo de JSON de clientes
├── carros_exemplo_multiplos.json          # Exemplo de JSON de carros
├── requirements.txt                        # Dependências Python
├── .gitignore                             # Arquivos ignorados pelo Git
└── README.md                              # Este arquivo
```

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/eduardozelaya12/Automacao_seguros.git
cd Automacao_seguros
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Executar automação de clientes (standalone)

```bash
python automacao_clientes_corrigida_testes.py
```

### Executar automação de carros (standalone)

```bash
python automacao_carros_corrigida_testes.py
```

### Executar API

```bash
cd api
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## 📊 Endpoints da API

### POST `/api/clientes`
Cadastra um cliente

**Body:**
```json
{
  "output": {
    "tipo_cliente": "FISICA",
    "nombre_completo": "João da Silva",
    "documento": "12345678",
    "telefono": "099123456",
    "direccion": "Rua Exemplo, 123"
  }
}
```

### POST `/api/carros`
Cadastra um veículo

**Body:**
```json
{
  "output": {
    "datos_poliza": {
      "numero_poliza": "2024-001"
    },
    "datos_vehiculo": {
      "marca_modelo": "Toyota Corolla",
      "ano": "2020",
      "categoria": "AUTOMOVIL",
      "combustible": "NAFTA"
    }
  }
}
```

### GET `/api/jobs/{job_id}`
Consulta status de um job

## 📝 Categorias Suportadas

### Veículos
- AMBULANCIA, AUTOMOVIL, CABINA EXTENDIDA, CAMION, CAMIONETA
- CASA RODANTE, CHATA, CISTERNA, CUADRICICLOS, DOBLE CABINA
- EXCAVADORA, FURGON, JEEP, MAQ. AUTOMOTRIZ, MINI BUS
- MOTO, MOTORHOME, OMNIBUS, PICK UP, REMOLQUE
- RETROEXCAVADORA, RURAL, SEMIREMOLQUE, TRACTOR, TRAILER

### Destinos de Uso
- ALQUILER SIN CHOFER, AUXILIO MECANICO, COMERCIAL
- EASY GO Y UBER, PARTICULAR, PARTICULAR Y TRABAJO
- PASEO, PLACER, REMISE, TAXIMETROS, TRABAJO
- TRABAJO PERSONAL, UBER

### Calidad
- ARRENDATARIO, PR. COMPRADOR, PROPIETARIO, USUARIO

### Coberturas
- BASICA, TERCEROS, TERC.+ROBO+INCENDIO, TODO RIESGO
- E mais 11 opções...

### Zonas de Circulação
28 zonas incluindo MONTEVIDEO, CANELONES, MALDONADO, etc.

## ⚠️ Importante

1. **Configurações de segurança PyAutoGUI:**
   - FAILSAFE está ativado (mova o mouse para o canto superior esquerdo para interromper)
   - PAUSE de 0.8s entre ações

2. **Antes de executar:**
   - Certifique-se de que o Velneo vClient está fechado
   - Posicione-se na tela inicial
   - Não mexa no mouse/teclado durante a execução

3. **JSONs de dados reais:**
   - `clientes.json` e `carros.json` são ignorados pelo Git
   - Use os arquivos `*_exemplo_multiplos.json` como template

## 📄 Licença

MIT License

## 👤 Autor

Eduardo Zelaya
