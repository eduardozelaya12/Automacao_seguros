# 📊 Pasta de Dados

Coloque aqui seus arquivos de dados para automação:

- **JSON**: Configurações, credenciais, dados estruturados
- **CSV**: Listas, tabelas, dados tabulares
- **Excel** (.xlsx): Planilhas complexas

## Exemplo de estrutura JSON:

```json
{
  "credenciais": {
    "usuario": "seu_usuario",
    "senha": "sua_senha"
  },
  "configuracoes": {
    "tempo_espera": 2,
    "screenshot_on_error": true
  }
}
```

## Exemplo de uso no Python:

```python
import json

# Ler JSON
with open('data/config.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

usuario = dados['credenciais']['usuario']
```

**Nota**: Arquivos nesta pasta são ignorados pelo Git por segurança (podem conter dados sensíveis).
