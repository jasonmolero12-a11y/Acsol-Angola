# ACSOL Angola - Plataforma Django

Este projeto converte a versao inicial em HTML estatico da ACSOL Angola para uma base web em Python/Django.

## Tecnologias

- Python 3
- Django 5
- PostgreSQL em producao
- SQLite para desenvolvimento local
- CSS/JS local com fallback offline para Bootstrap, icones e animacoes
- HTML, CSS e JavaScript

## Como executar localmente

```powershell
cd C:\Users\jason\Documents\Codex\2026-06-08\Acsol-Angola
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_initial_data
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Acesse:

- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Admin local criado:

- Usuario: `jason`
- Nome: Jason
- Senha: definida conforme solicitado pelo dono do projeto

Para alterar nome ou senha depois:

1. Entre no admin.
2. Abra `Users`.
3. Clique no utilizador `jason`.
4. Altere o nome nos campos do usuario.
5. Para senha, use o link de troca de password dentro da propria pagina do usuario.

## Estrutura

```text
acsol/                 Configuracoes, URLs ASGI/WSGI
core/                  App principal com modelos, views, forms e admin
templates/core/        Template principal convertido do HTML original
static/css/            CSS extraido do index.html
static/js/             JavaScript extraido e adaptado
media/                 Uploads em desenvolvimento
docs/                  Documentacao do projeto
```

## Producao

Crie um arquivo `.env` baseado em `.env.example` e configure:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS`
- `DATABASE_URL` com PostgreSQL
- chaves opcionais para OpenAI/Gemini

Com `DEBUG=False`, o projeto ativa redirecionamento HTTPS, cookies seguros e HSTS.

Para producao com dominio e HTTPS:

```env
DEBUG=False
ALLOWED_HOSTS=acsol.ao,www.acsol.ao
CSRF_TRUSTED_ORIGINS=https://acsol.ao,https://www.acsol.ao
SECURE_SSL_REDIRECT=True
USE_X_FORWARDED_PROTO=True
```

O layout publico e o admin nao dependem mais de CDN externas obrigatorias. Bootstrap, icones, animacoes, Lucide e grafico do admin possuem fallback local para funcionar mesmo sem internet.

## Chatbot e doacoes

Veja [docs/CHATBOT_E_DOACOES.md](docs/CHATBOT_E_DOACOES.md).
