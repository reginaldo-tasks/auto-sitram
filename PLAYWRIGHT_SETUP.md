# Playwright Setup no GitHub Codespaces

## Problema Inicial
Ao tentar usar Playwright no Codespaces, obtínhamos o erro:
```
libgbm.so.1: cannot open shared object file: No such file or directory
```

## Solução

### 1. Instalar Dependências do Sistema
O Codespaces não vem com todas as bibliotecas necessárias para o Chromium funcionar. Execute:

```bash
sudo apt-get install -y libgbm1 libxkbcommon0 libpango-1.0-0 libpangoft2-1.0-0 libglib2.0-0
```

### 2. Instalar Python Dependencies
```bash
pip install playwright nest_asyncio django-cors-headers
```

Garanta que seu `requirements.txt` contém:
```
playwright
nest_asyncio
django-cors-headers
```

### 3. Problema: Asyncio em Django
Django é síncrono, mas Playwright é assíncrono. A solução é usar `nest_asyncio`:

**No arquivo `automation/services/playwright_service.py`:**
```python
import nest_asyncio
nest_asyncio.apply()

def extract_sitram_data_sync(search_params):
    return asyncio.run(extract_sitram_data(search_params))
```

## Verificação
Para verificar se tudo funciona:

```bash
python -c "
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        print('✓ Playwright works!')
        await browser.close()

asyncio.run(test())
"
```

## Performance
- Primeira execução: ~5-10 segundos (download do navegador)
- Execuções subsequentes: ~2-3 segundos

## Debugging
Se encontrar erros, verifique:
1. `libgbm1` instalado: `dpkg -l | grep libgbm`
2. Playwright bins: `ls ~/.cache/ms-playwright/`
3. Logs do Django: `python manage.py runserver --debug-toolbar`
