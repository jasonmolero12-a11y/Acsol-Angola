# Guia de hospedagem gratis no PythonAnywhere

Este guia e para colocar a ACSOL Angola online no plano gratis do PythonAnywhere, mantendo Django, painel admin, gerentes, conteudo editavel, galeria, voluntariado, doacoes em especie e chatbot programado.

## 1. Criar conta

1. Aceda a `https://www.pythonanywhere.com`.
2. Crie uma conta gratuita.
3. O site ficara num endereco parecido com:

```text
seuusuario.pythonanywhere.com
```

## 2. Enviar o projeto

Opção recomendada:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git Acsol-Angola
cd Acsol-Angola
```

Se ainda nao usar GitHub, envie o zip do projeto e descompacte em:

```text
/home/seuusuario/Acsol-Angola
```

## 3. Criar ambiente Python

No console Bash do PythonAnywhere:

```bash
cd ~/Acsol-Angola
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Se o PythonAnywhere oferecer outra versao, use a versao disponivel na sua conta.

## 4. Criar ficheiro .env

Crie `~/Acsol-Angola/.env`:

```env
DEBUG=False
SECRET_KEY=troque-por-uma-chave-grande-e-segura
PYTHONANYWHERE_DOMAIN=seuusuario.pythonanywhere.com
ALLOWED_HOSTS=seuusuario.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://seuusuario.pythonanywhere.com
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
ACSOL_ADMIN_PASSWORD=troque-a-senha-admin
ACSOL_MANAGER_DEFAULT_PASSWORD=troque-a-senha-gerentes
```

No plano gratis, `SECURE_SSL_REDIRECT=False` evita conflito de redirecionamento. O PythonAnywhere ja entrega o endereco com HTTPS.

## 5. Preparar banco e ficheiros estaticos

```bash
cd ~/Acsol-Angola
source .venv/bin/activate
python manage.py migrate
python manage.py seed_initial_data
python manage.py collectstatic --noinput
```

Depois entre no admin e troque as senhas iniciais.

## 6. Configurar Web App

No painel do PythonAnywhere:

1. Va em `Web`.
2. Clique em `Add a new web app`.
3. Escolha `Manual configuration`.
4. Escolha a versao de Python usada no venv.

Configure:

```text
Source code: /home/seuusuario/Acsol-Angola
Working directory: /home/seuusuario/Acsol-Angola
Virtualenv: /home/seuusuario/Acsol-Angola/.venv
```

## 7. Editar ficheiro WSGI

No ficheiro WSGI do PythonAnywhere, deixe parecido com:

```python
import os
import sys

path = "/home/seuusuario/Acsol-Angola"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acsol.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 8. Mapear static e media

Em `Web > Static files`, adicione:

```text
URL: /static/
Directory: /home/seuusuario/Acsol-Angola/staticfiles
```

```text
URL: /media/
Directory: /home/seuusuario/Acsol-Angola/media
```

## 9. Recarregar o site

Clique em `Reload`.

Depois aceda:

```text
https://seuusuario.pythonanywhere.com
https://seuusuario.pythonanywhere.com/admin/
```

## 10. Backup

No console Bash:

```bash
cd ~/Acsol-Angola
bash scripts/pythonanywhere_backup.sh
```

O backup fica em:

```text
/home/seuusuario/acsol_backups
```

Faça download desses backups regularmente.

## Limites do plano gratis

- Nao permite dominio proprio no plano gratis.
- Espaco limitado.
- Trafego e CPU limitados.
- Banco recomendado no inicio: SQLite.
- Chatbot deve ficar em `Respostas programadas`, sem API paga.
- Para muitos acessos ou uso institucional mais serio, migrar depois para VPS ou plano pago.

## O que fica funcionando

- Site publico.
- Painel administrativo.
- Gerentes.
- Edicao de textos, fotos, parceiros, galeria, videos, eventos, projetos e equipa.
- Formularios de voluntariado, contacto, doacao em especie e newsletter.
- Doacoes monetarias bloqueadas ate o admin ativar com dados reais.
- Chatbot por perguntas frequentes programadas.
