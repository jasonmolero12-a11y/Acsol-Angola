# Guia de build e hospedagem - ACSOL Angola

Este projeto e Django. Ele nao gera uma pasta `build/` como React.

Para hospedar, o "build" de producao significa:

- instalar dependencias;
- coletar ficheiros estaticos com `collectstatic`;
- aplicar migracoes com `migrate`;
- iniciar o servidor com `gunicorn`;
- usar PostgreSQL em producao;
- configurar variaveis de ambiente.

## Ficheiros criados

- `build.sh`: instala dependencias, executa `collectstatic` e `migrate`.
- `Procfile`: comando de arranque para plataformas que usam Procfile.
- `render.yaml`: blueprint para Render.

## Variaveis obrigatorias em producao

Configure na hospedagem:

```env
DEBUG=False
SECRET_KEY=uma-chave-forte
DATABASE_URL=postgres://usuario:senha@host:5432/base
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,acsol-angola.onrender.com
CSRF_TRUSTED_ORIGINS=https://seudominio.com,https://www.seudominio.com,https://acsol-angola.onrender.com
ACSOL_ADMIN_PASSWORD=senha-forte-do-admin
ACSOL_MANAGER_DEFAULT_PASSWORD=senha-inicial-forte-dos-gerentes
```

Nunca publique `.env` no GitHub.

## Deploy no Render

1. Entrar no Render.
2. Criar `New > Blueprint`.
3. Escolher o repositorio GitHub `Acsol-Angola`.
4. O Render vai ler `render.yaml`.
5. Preencher manualmente:
   - `ALLOWED_HOSTS`.
   - `CSRF_TRUSTED_ORIGINS`.
   - `ACSOL_ADMIN_PASSWORD`.
   - `ACSOL_MANAGER_DEFAULT_PASSWORD`.
6. Fazer deploy.

Depois de o Render gerar o link, exemplo:

```text
https://acsol-angola.onrender.com
```

atualize:

```env
ALLOWED_HOSTS=acsol-angola.onrender.com
CSRF_TRUSTED_ORIGINS=https://acsol-angola.onrender.com
```

## Banco de dados

Use PostgreSQL. Nao use SQLite em producao.

O plano gratuito de PostgreSQL no Render e temporario. Para producao real, use plano pago ou outro PostgreSQL gerido.

## Uploads e imagens

O diretorio `media/` nao vai para o GitHub.

Para producao, as imagens enviadas pelo admin precisam de uma estrategia:

- usar armazenamento da propria hospedagem, se for persistente;
- usar Cloudinary/S3 no futuro;
- reenviar as imagens pelo admin depois do deploy.

## Teste local antes de publicar

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

## O que falta antes de ficar 100% producao

- escolher hospedagem;
- configurar dominio;
- configurar PostgreSQL de producao;
- configurar armazenamento das imagens enviadas pelo admin;
- criar backup automatico do banco;
- trocar chaves API antigas;
- configurar email profissional para mensagens reais.
