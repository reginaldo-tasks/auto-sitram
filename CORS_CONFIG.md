# Configuração CORS e URLs

## Ambientes

### Local Development
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Endpoint**: http://localhost:8000/api/sitram/search/

### GitHub Codespaces (Production)
- **Frontend**: https://urban-potato-gxp745pxrjxc6gq-5173.app.github.dev
- **Backend**: https://urban-potato-gxp745pxrjxc6gq-8000.app.github.dev
- **API Endpoint**: https://urban-potato-gxp745pxrjxc6gq-8000.app.github.dev/api/sitram/search/

## Configuração CORS

O backend está configurado com `django-cors-headers` para aceitar requisições de:

**Local:**
- http://localhost:5173
- http://localhost:3000
- http://127.0.0.1:5173
- http://127.0.0.1:3000

**Production (GitHub Codespaces):**
- https://urban-potato-gxp745pxrjxc6gq-5173.app.github.dev

Para adicionar novos domínios, modifique `backend/core/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://seu-dominio.com",
]
```

## Auto-Detection no Frontend

O serviço `sitramService.ts` detecta automaticamente:
- Se `window.location.hostname` contém `github.dev` → usa URL de produção
- Caso contrário → usa `VITE_API_URL` ou localhost

```typescript
const getApiUrl = (): string => {
  if (typeof window !== 'undefined' && window.location.hostname.includes('github.dev')) {
    return 'https://urban-potato-gxp745pxrjxc6gq-8000.app.github.dev/api';
  }
  return import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
};
```

## Headers CORS

Requisições incluem:
```
Content-Type: application/json
Credentials: include (para cookies)
```

Respostas incluem:
```
Access-Control-Allow-Origin: https://urban-potato-gxp745pxrjxc6gq-5173.app.github.dev
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, OPTIONS
```
