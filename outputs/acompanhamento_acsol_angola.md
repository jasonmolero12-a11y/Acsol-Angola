# Acompanhamento ACSOL Angola

Estado geral: **99% concluido para a V1 funcional**.

## Atualizacao desta etapa

- Corrigido bloqueio do GitHub `Push blocked: secret detected`.
- Removidos do historico Git os backups JSON que continham chave/API do chatbot.
- Recriado o ramo `main` com um commit limpo para publicar no GitHub.
- Atualizado `.gitignore` para nao publicar `outputs/*.json`, `media/`, `staticfiles/`, `db.sqlite3` e `.env`.
- Confirmado que a chave bloqueada nao aparece no commit limpo.
- Confirmado que `media/`, `staticfiles/`, backups JSON, `.env` e `db.sqlite3` nao estao rastreados.
- Corrigido erro em `/admin/auth/user/3/change/`: `Object of type Group is not JSON serializable`.
- O historico/auditoria do admin agora converte grupos e objetos Django para JSON simples antes de salvar.
- Criada migracao `core.0012` com campos novos para editar no admin:
  - `Os Nossos Parceiros`.
  - `Os Nossos Valores`.
  - `Porque Ser Voluntario?`.
- `Admin > Configuracoes do site` agora tem secoes proprias para Valores, Voluntariado e Parceiros.
- A pagina inicial e a pagina de parceiros passam a usar os textos configurados no admin.
- Parceiros cadastrados no admin agora aparecem no site; os exemplos ficam apenas como fallback quando nao houver parceiros reais.
- `Admin > Parceiros` agora tem campo de logotipo, link do website e pre-visualizacao do logo.
- Os parceiros da pagina inicial ficam clicaveis quando o campo `website` estiver preenchido.
- Redes sociais do site foram ligadas aos campos de `Configuracoes do site`: Facebook, Instagram, YouTube, LinkedIn e WhatsApp.
- Botao flutuante do WhatsApp agora usa o numero/link configurado no admin.
- `Admin > Configuracao de doacoes` ficou mais claro: agora mostra a coluna `Ativar Quero Doar` na lista.
- Criadas acoes rapidas no admin para `Ativar Quero Doar` e `Desativar Quero Doar`.
- Adicionado botao `Sair` visivel no topo do admin para terminar sessao e voltar ao login.
- A foto da equipa foi ajustada para preencher corretamente o cartao, com enquadramento pelo topo.
- A foto do Francisco e outros membros deve ajustar melhor em `A Nossa Equipa`.
- Tamanho recomendado para `A Nossa Equipa`: **900 x 1200 px** ou **1080 x 1350 px**, formato vertical 3:4 ou 4:5.
- `Quero Doar` monetario ficou indisponivel por padrao.
- O visitante ve uma mensagem clara informando que os dados bancarios oficiais ainda estao em confirmacao.
- Tentativas diretas de envio monetario tambem sao bloqueadas no servidor.
- O admin pode ativar a opcao depois em `Configuracao de doacoes > Ativar Quero Doar`.
- O admin pode preencher as instrucoes reais de pagamento nacional, internacional, Multicaixa e gateway.
- Doacao em especie continua disponivel e registrando pedidos no admin.
- Criado guia completo do admin.
- Criado guia simples para utilizadores sem experiencia tecnica.
- Confirmado que todos os 24 modelos do app `core` estao registados no Django Admin.
- Auditoria geral do frontend do admin feita.
- Corrigida sidebar do admin que podia ficar escondida por CSS padrao do Django.
- CSS do admin versionado para evitar cache antiga no navegador.
- Login, dashboard, listas e formularios principais continuam funcionais.
- Corrigido fluxo de criacao de utilizador no admin.
- Criar utilizador agora ficou mais simples: primeiro utilizador/senha, depois editar perfil, funcao e permissoes.

## Onde Jason deve mexer depois

- `Admin > Configuracao de doacoes`: ativar/desativar `Quero Doar` e preencher dados reais.
- `Admin > Doacoes em especie`: acompanhar doacoes de bens.
- `Admin > Projetos` e `Projetos feitos`: gerir projetos.
- `Admin > Galeria e videos`: gerir fotos e videos.
- `Admin > Noticias e eventos`: gerir eventos e noticias.
- `Admin > Equipa`: alterar equipa e fotos.
- `Admin > Parceiros`: adicionar nome, logotipo, link e marcar ativo.
- `Admin > Configuracoes do site`: alterar redes sociais e dados gerais.

## Documentos criados

- `docs/GUIA_ADMIN_COMPLETO_ACSOL.md`
- `docs/GUIA_USO_SIMPLES_ACSOL.md`
- `docs/RELATORIO_ACSOL_ATUALIZADO.md`

## Validacao

- `manage.py migrate`: OK.
- `manage.py check`: OK.
- `node --check static/js/site.js`: OK.
- `collectstatic --noinput`: OK.
- Pagina inicial: HTTP 200.
- Mensagem `Quero Doar indisponivel`: confirmada no HTML.
- Endpoint de instrucoes monetarias: devolve indisponivel.
- POST de doacao monetaria: bloqueado com HTTP 403.
- Admin dashboard/listas/formularios: HTTP 200.
- Sidebar ACSOL: visivel e sem overflow no teste desktop.
- Criacao de utilizador temporario: OK.
- Perfil automatico do utilizador criado: OK.
- Tela de edicao do utilizador com perfil/funcao: OK.
- PostgreSQL local: ligado na porta `54321`.
- Base `acsol_angola`: criada.
- `.env`: criado com `DATABASE_URL` para PostgreSQL.
- Dados antigos do SQLite: exportados, convertidos para UTF-8 e importados.
- Objetos importados para PostgreSQL: 104.
- Escrita no PostgreSQL: OK.
- `Quero Doar`: indisponivel no frontend e bloqueado no backend ate liberacao do admin.
- Script criado: `scripts/start_postgres_54321.ps1`.
- Servico Windows `postgresql-x64-18`: aparece como parado nesta sessao, mas PostgreSQL esta ativo via `pg_ctl` na porta `54321`.
- Problema do `runserver` analisado: Django sobe, mas precisa do PostgreSQL ativo para servir a pagina.
- Script criado: `scripts/run_local.ps1`.
- Campo novo no admin: `Configuracoes do site > Imagem da secao Quem Somos`.
- Imagem do `Quem Somos`: agora usa foto do admin ou fallback local, sem depender da Pexels principal.
- Migracao `core.0011_siteconfig_imagem_sobre`: aplicada.
- Pagina inicial: HTTP 200 depois da correcao.
- `core.0012_siteconfig_texto_parceiros_siteconfig_texto_valores_and_more`: aplicada.
- `serialize_instance(User #3/francisco)`: OK, grupo `Gerente` serializado como lista JSON.
- `/admin/auth/user/3/change/`: HTTP 200.
- `/admin/core/siteconfig/1/change/`: HTTP 200.
- `collectstatic --noinput`: OK, CSS atualizado copiado.
- `Admin > Parceiros > Adicionar`: HTTP 200.
- Redes sociais configuradas no banco: Facebook, Instagram, YouTube e WhatsApp encontrados; LinkedIn vazio.
- `Admin > Configuracao de doacoes`: HTTP 200 e texto `Ativar Quero Doar` confirmado no HTML.
- `/admin/`: HTTP 200 com botao `Sair` e formulario de logout confirmados.
