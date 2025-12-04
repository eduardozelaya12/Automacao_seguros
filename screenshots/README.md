# 📸 Screenshots

Esta pasta armazena **capturas de tela** feitas durante as automações.

## Capturar Screenshot:

```python
import pyautogui

# Screenshot de tela inteira
screenshot = pyautogui.screenshot()
screenshot.save('screenshots/captura_completa.png')

# Screenshot de uma área específica (x, y, largura, altura)
screenshot = pyautogui.screenshot(region=(0, 0, 800, 600))
screenshot.save('screenshots/area_especifica.png')
```

## Uso Comum:

- ✅ Evidências de execução
- ✅ Debug visual
- ✅ Relatórios automáticos
- ✅ Captura de erros

**Nota**: Arquivos PNG/JPG nesta pasta são ignorados pelo Git.
