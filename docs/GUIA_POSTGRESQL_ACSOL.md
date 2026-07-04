# Guia para Migrar a Base de Dados para PostgreSQL

Este guia explica como sair do SQLite local e usar PostgreSQL no projeto ACSOL Angola.

## 1. Instalar PostgreSQL

No Windows, instale PostgreSQL pelo instalador oficial ou use uma ferramenta como Laragon/Docker.

Durante a instalacao guarde:

- usuario do banco
- senha
- porta, normalmente `5432`

## Estado atual deste projeto

Neste computador, a ACSOL ja foi ligada ao PostgreSQL local com:

- Host: `127.0.0.1`
- Porta: `54321`
- Base de dados: `acsol_angola`
- Utilizador: `postgres`
- Senha: definida localmente no ficheiro `.env`

O erro encontrado foi que o PostgreSQL estava a tentar usar `5432` por causa de `postgresql.auto.conf`, mesmo depois de alterar `postgresql.conf`. Foi corrigido com `ALTER SYSTEM SET port = 54321` e reinicio via `pg_ctl`.

O ficheiro `.env` esta no `.gitignore` e nao deve ser publicado.

Observacao local: nesta sessao o Windows nao permitiu controlar o servico `postgresql-x64-18` pelo PowerShell, mas o PostgreSQL foi iniciado com `pg_ctl` e ficou a responder na porta `54321`. Se reiniciar o computador e a porta estiver fechada, execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_postgres_54321.ps1
```

Ou abra `Servicos` do Windows como administrador e inicie `postgresql-x64-18`.

## 2. Criar a base de dados

Abra o pgAdmin ou terminal PostgreSQL e crie:

```sql
CREATE DATABASE acsol_angola;
CREATE USER acsol_user WITH PASSWORD 'troque_esta_senha';
GRANT ALL PRIVILEGES ON DATABASE acsol_angola TO acsol_user;
```

## 3. Configurar o `.env`

No projeto, crie ou edite o ficheiro `.env`:

```env
DEBUG=True
SECRET_KEY=troque-esta-chave-em-producao
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://acsol_user:troque_esta_senha@localhost:5432/acsol_angola
```

Configuracao local atual:

```env
DATABASE_URL=postgresql://postgres:SENHA_LOCAL@127.0.0.1:54321/acsol_angola
```

## 4. Instalar driver PostgreSQL

Com o ambiente virtual ativo:

```powershell
cd C:\Users\jason\Documents\Codex\2026-06-08\Acsol-Angola
.\.venv\Scripts\python.exe -m pip install psycopg[binary]
```

Se o projeto ja tiver `requirements.txt`, depois atualize:

```powershell
.\.venv\Scripts\python.exe -m pip freeze > requirements.txt
```

## 5. Migrar as tabelas

Depois de configurar `DATABASE_URL`, rode:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

## 6. Levar os dados atuais do SQLite para PostgreSQL

Antes de trocar para PostgreSQL, exporte os dados atuais:

```powershell
.\.venv\Scripts\python.exe manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > backup_acsol.json
```

Depois configure o `.env` com PostgreSQL e importe:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py loaddata backup_acsol.json
```

Neste projeto foi criado um backup em:

```text
outputs/acsol_sqlite_backup_before_postgres.json
outputs/acsol_sqlite_backup_before_postgres_utf8.json
```

O segundo ficheiro foi convertido para UTF-8 e importado com sucesso para PostgreSQL.

## 7. Criar admin se necessario

Se preferir criar um admin novo:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Ou recriar os dados iniciais:

```powershell
.\.venv\Scripts\python.exe manage.py seed_initial_data
```

Isto recria:

- admin `jason`
- gerentes
- configuracoes iniciais
- eventos de exemplo
- divisoes de exemplo

## 8. Testar

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Acesse:

- site: `http://127.0.0.1:8000/`
- admin: `http://127.0.0.1:8000/admin/`

## 9. Producao

Em producao use:

```env
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DATABASE_URL=postgres://usuario:senha@host:5432/base
```

Tambem configure:

- HTTPS
- backups automaticos
- email institucional
- `SECRET_KEY` forte
- permissao correta para pasta `media/`

## 10. Backup recomendado

Backup JSON pelo Django:

```powershell
.\.venv\Scripts\python.exe manage.py dumpdata --indent 2 > backup_acsol_YYYYMMDD.json
```

Backup nativo PostgreSQL:

```powershell
pg_dump -U acsol_user -d acsol_angola > backup_acsol.sql
```
