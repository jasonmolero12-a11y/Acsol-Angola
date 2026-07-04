# Arquitetura do Sistema ACSOL

## Camadas

- `acsol`: configuracao global do projeto Django, URLs principais e WSGI/ASGI.
- `core`: dominio principal do website e CMS.
- `templates`: camada de apresentacao.
- `static`: CSS e JavaScript.
- `media`: uploads de imagens, videos, curriculos e comprovativos.

## Modelos principais

- `SiteConfig`: identidade, contactos, redes sociais, hero, missao, visao e valores.
- `Category`: categorias para projetos, noticias, eventos, galeria e FAQ.
- `Project`: projetos sociais com estado, beneficiarios, localizacao, progresso e destaque.
- `Article`: noticias e eventos.
- `GalleryItem`: imagens, videos locais e videos do YouTube.
- `VolunteerApplication`: candidaturas de voluntarios.
- `Donation`: intencoes/comprovativos de doacao.
- `ContactMessage`: mensagens enviadas pelo formulario de contacto.
- `NewsletterSubscriber`: subscritores da newsletter.
- `Partner`, `TeamMember`, `Statistic`, `FAQ`, `ActivityLog`: conteudo institucional e gestao.

## URLs

- `/`: pagina publica principal.
- `/admin/`: painel administrativo.
- `/voluntariado/candidatura/`: submissao de candidatura.
- `/doacoes/interesse/`: registo de interesse em doacao.
- `/contacto/`: formulario de contacto.
- `/newsletter/`: subscricao de newsletter.

## Banco de dados

O projeto usa SQLite por padrao para desenvolvimento. Para producao, configure `DATABASE_URL` com PostgreSQL.

## Expansoes previstas

- API REST para app movel.
- Chatbot com provider OpenAI/Gemini configuravel.
- Gateway de pagamento para doacoes online.
- Dashboard estatistico com graficos.
- Area de membros com perfis e permissoes especificas.

