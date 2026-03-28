# Testando Automação SITRAM - Guia Prático

## 3 Formas de Testar e Debug

### 1️⃣ INSPEÇÃO PROFUNDA (Recomendado Começar Por Aqui)

```bash
cd /workspaces/auto-sitram/backend
source venv/bin/activate
python detailed_inspection.py
```

**O que faz:**
- ✅ Abre a página SITRAM
- ✅ Lista TODOS os inputs, buttons, dropdowns
- ✅ Mostra ID, name, placeholder, classe de CADA elemento
- ✅ Gera seletores CSS recomendados
- ✅ Salva em `/tmp/sitram_analysis.json` e `/tmp/sitram_detailed.html`

**Resultado:**
```json
{
  "inputs": [
    {
      "text": "CNPJ",
      "id": "cnpj-input-123",
      "name": "cnpj",
      "placeholder": "00.000.000/0000-00",
      "selector": "#cnpj-input-123"  // ← Use este no código!
    }
  ],
  "buttons": [
    {
      "text": "Pesquisar",
      "id": "search-btn",
      "selector": "#search-btn"
    },
    {
      "text": "CSV",
      "selector": "button:has-text('CSV')"
    }
  ]
}
```

---

### 2️⃣ TESTE MANUAL COM NAVEGADOR VISUAL

```bash
cd /workspaces/auto-sitram/backend
source venv/bin/activate
python manual_test.py
```

**O que faz:**
- ✅ **Abre o navegador em modo VISUAL** (headless=False)
- ✅ Você consegue **VER e INSPECCIONAR** toda ação
- ✅ Pressione F12 para abrir DevTools
- ✅ Clique em elementos para ver seus seletores
- ✅ Teste preenchimentos manualmente
- ✅ Copie IDs/classes de elementos funcionando

**Ideal para:**
- Encontrar seletores exatos clicando nos elementos
- Ver em tempo real o que o Playwright vê
- Testar interações manualmente

---

### 3️⃣ GRAVADOR DE CÓDIGO AUTOMÁTICO (Codegen)

```bash
cd /workspaces/auto-sitram/backend
source venv/bin/activate
python codegen_test.py
```

**O que faz:**
- ✅ Abre navegador com **Playwright Inspector**
- ✅ **Cada ação que você faz é registrada como código Python**
- ✅ Você faz: clica em campo → Codegen gera: `page.fill('#field-id', 'value')`
- ✅ No painel direito, vê o código gerado em tempo real
- ✅ Salva em `/tmp/sitram_recorded.py`

**Como usar:**
```
1. Página SITRAM abre em navegador normal
2. Você preenche os campos (Start Date, End Date, CNPJ)
3. Clica em "Pesquisar"
4. Aguarda resultados
5. Clica em "CSV"
6. Fecha o navegador
7. Código foi gerado em /tmp/sitram_recorded.py
8. Copie esse código para playwright_service.py
```

**Exemplo de código gerado:**
```python
# Start recording
page.goto('https://portal-sitram...')
page.fill('#start-date', '01/12/2025')
page.fill('#end-date', '31/12/2025')
page.fill('#cnpj', '23602073000159')
page.click('button:has-text("Pesquisar")')
page.wait_for_load_state('networkidle')
page.click('button:has-text("CSV")')
# End recording - COPY TUDO ISTO!
```

---

## Passo a Passo Recomendado

### Dia 1: Descobrir Seletores
1. **Rodei `detailed_inspection.py`**
   ```bash
   python detailed_inspection.py
   ```
2. **Abri `/tmp/sitram_analysis.json`**
   - Vi todos os IDs dos elementos
   - Copiei os seletores corretos

### Dia 2: Validar Interações
1. **Rodei `manual_test.py`**
   ```bash
   python manual_test.py
   ```
2. **Mantive o navegador aberto**
   - Inspecionei (F12) os elementos
   - Confirmei que os seletores estavam corretos
   - Testei preencher campos manualmente

### Dia 3: Gerar Código Automático
1. **Rodei `codegen_test.py`**
   ```bash
   python codegen_test.py
   ```
2. **Fiz as ações na ordem:**
   - Preenchimento Start Date
   - Preenchimento End Date
   - Preenchimento CNPJ
   - Click Pesquisar
   - Click CSV
3. **Copiei código gerado para `playwright_service.py`**

---

## Se Ainda Tiver Problemas

### ❌ "Elemento não encontrado"
**Solução:**
1. Rodei `detailed_inspection.py`
2. Busquei no HTML gerado (`/tmp/sitram_detailed.html`)
3. Procurei o texto do elemento (ex: "Pesquisar")
4. Copiei o ID ou classe exata

### ❌ "Timeout esperando elemento"
**Solução:**
1. Rodei `manual_test.py`
2. Deixei o navegador aberto
3. Procurei manualmente os elementos
4. Verifiquei se realmente existem na página

### ❌ "Download não funciona"
**Solução:**
1. Rodei `codegen_test.py`
2. Gravei a ação de clique no botão CSV
3. Copiei exatamente o código que Codegen gerou

---

## Arquivos Gerados Para Debug

| Arquivo | Conteúdo |
|---------|----------|
| `/tmp/sitram_analysis.json` | Lista de todos inputs/buttons com seletores |
| `/tmp/sitram_detailed.html` | HTML completo da página para buscar elementos |
| `/tmp/sitram_page.png` | Screenshot do estado atual |
| `/tmp/sitram_recorded.py` | Código Playwright gravado automaticamente |

---

## Comandos Rápidos

```bash
# Terminal 1: Inspection
python detailed_inspection.py

# Terminal 2: Manual testing com navegador
python manual_test.py

# Terminal 3: Code generation (Codegen)
python codegen_test.py

# Terminal 4: API Django (para depois testar)
source venv/bin/activate
python manage.py runserver
```

---

## ✅ Checklist de Debug

- [ ] Rodei `detailed_inspection.py` e inspecionei output
- [ ] Vi arquivo `/tmp/sitram_analysis.json`
- [ ] Fiz teste manual com `manual_test.py`
- [ ] Abri DevTools (F12) e procurei elementos
- [ ] Usei `codegen_test.py` para gravar ações
- [ ] Copiei código gerado para `playwright_service.py`
- [ ] Testei API: POST `/api/sitram/search/`

---

**Agora vamos descobrir exatamente o que o Playwright precisa fazer! 🚀**
