# 📝 Logs

Esta pasta armazena **arquivos de log** das execuções de automação.

## Criar Logs:

```python
import logging
from datetime import datetime

# Configurar logging
log_filename = f'logs/automacao_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()  # Também mostra no console
    ]
)

# Usar
logging.info("Automação iniciada")
logging.warning("Atenção: elemento não encontrado")
logging.error("Erro ao processar dados")
logging.info("Automação concluída com sucesso")
```

## Benefícios:

- ✅ Rastreabilidade de execuções
- ✅ Debug de problemas
- ✅ Auditoria de processos
- ✅ Histórico de ações

**Nota**: Arquivos .log nesta pasta são ignorados pelo Git.
