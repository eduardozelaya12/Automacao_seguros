# 🖼️ Imagens de Referência

Esta pasta armazena **imagens de referência** usadas para localizar elementos na tela.

## Localizar Imagem na Tela:

```python
import pyautogui

# Procurar imagem na tela
posicao = pyautogui.locateOnScreen('imagens/botao_salvar.png')

if posicao:
    # Clicar no centro da imagem encontrada
    pyautogui.click(posicao)
    print("Botão encontrado e clicado!")
else:
    print("Imagem não encontrada na tela")
```

## Dicas:

1. **Capture imagens pequenas** - apenas o botão/elemento, não a tela toda
2. **Use alta qualidade** - PNG é preferível a JPG
3. **Mesma resolução** - capture na mesma resolução da tela onde vai rodar
4. **Contraste alto** - elementos bem definidos são mais fáceis de localizar

## Ferramentas para Capturar:

- Windows: **Ferramenta de Captura** (Win + Shift + S)
- Ou use o próprio PyAutoGUI: `pyautogui.screenshot(region=(x, y, w, h))`

**Nota**: Arquivos de referência podem ser versionados no Git.
