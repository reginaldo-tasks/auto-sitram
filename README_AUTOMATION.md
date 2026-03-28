# auto-sitram - Automação SITRAM

Sistema full-stack para automatizar a extração de dados do portal SITRAM usando Playwright + Django + React.

**Nota:** O portal SITRAM não requer autenticação para acessar os dados públicos.

## 📋 Estrutura

```
auto-sitram/
├── backend/
│   ├── automation/           # App Django para automação
│   │   ├── services/         # Lógica de automação Playwright
│   │   ├── views.py          # Endpoints REST
│   │   ├── serializers.py    # Validação de dados
│   │   └── urls.py           # Rotas
│   ├── core/                 # Config Django
│   └── venv/                 # Virtual environment
└── frontend/
    ├── src/
    │   ├── pages/           # React pages
    │   ├── services/        # API clients
    │   └── App.tsx
    └── package.json
```

## 🚀 Setup

### Backend

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

**Endpoints:**
- `POST /api/sitram/search/` - Buscar dados SITRAM

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📝 API

### POST /api/sitram/search/

**Request:**
```json
{
  "start_date": "01/01/2024",
  "end_date": "31/12/2024",
  "cnpj": "38.009.037/0001-53"
}
```

**Response:**
```json
{
  "success": true,
  "data": "CSV content as string"
}
```

## 🔧 Funcionamento

1. **Navegação** - Acessa página de ICMS por NF
2. **Filtros** - Preenche período (datas) e CNPJ
3. **Busca** - Clica em pesquisar
4. **Download** - Baixa arquivo CSV
5. **Retorno** - Envia CSV para frontend

## 📦 Dependências Principais

- **Django 6.0** - Framework backend
- **Playwright 1.58.0** - Automação de browsers
- **React 19** - Frontend
- **Pandas 3.0** - Análise de dados (opcional)

## ⚠️ Notas Importantes

- O portal SITRAM não requer login
- Para produção, considerar rate limiting
- O portal pode ter proteção contra bots
- Testar com CNPJs válidos
- Considerar caching de resultados

## 📄 Licença

MIT
