# Relatorio Atualizado - ACSOL Angola

Data: 10/06/2026

## Estado geral

**99% concluido para uma V1 funcional.**

O que falta para fechar a V1 e principalmente inserir os dados reais da ACSOL: textos oficiais, fotos, videos, eventos, provincias, dados de doacao e decisao de hospedagem.

## Feito nesta etapa

- Corrigido erro ao salvar utilizador no admin: `Object of type Group is not JSON serializable`.
- A auditoria reversivel do admin agora grava grupos/permissoes como dados JSON simples.
- Adicionados campos editaveis em `Configuracoes do site` para:
  - `Os Nossos Parceiros`.
  - `Os Nossos Valores`.
  - `Porque Ser Voluntario?`.
- Criada migracao `core.0012_siteconfig_texto_parceiros_siteconfig_texto_valores_and_more`.
- A pagina inicial passou a ler titulo/texto de parceiros, valores e voluntariado a partir do admin.
- A pagina de parceiros passou a mostrar os parceiros cadastrados no admin, com logo e link.
- Os parceiros de exemplo ficam apenas como fallback quando nao houver parceiros reais cadastrados.
- `Admin > Parceiros` recebeu formulario mais claro com nome, logotipo, link, estado ativo e pre-visualizacao do logo.
- Parceiros da pagina inicial ficam clicaveis quando tiverem `website`.
- Redes sociais do site publico foram ligadas aos campos de `Configuracoes do site`.
- Botao flutuante do WhatsApp agora usa o WhatsApp configurado no admin.
- O campo WhatsApp aceita numero simples ou link completo.
- A foto dos membros em `A Nossa Equipa` foi ajustada para preencher o cartao corretamente.
- A foto do Francisco e dos demais membros agora usa `object-fit: cover` com enquadramento pelo topo.
- Galeria ficou apenas para fotos.
- Galeria voltou a ter filtros: Todas, Projetos, Eventos, Voluntarios e Comunidades.
- Videos ganharam uma nova secao separada no site.
- Admin pode cadastrar fotos, videos enviados e links do YouTube em `Galeria`.
- Admin pode apagar conteudo de demonstracao e substituir por dados reais.
- Criado modelo `Flyers e banners`, para o admin/gerente editar banners/flyers sem mexer no codigo.
- Criada doacao em especie completa.
- Formulario de doacao em especie tem nome, email, telefone, tipo de item, quantidade, estado do item, descricao, localizacao de entrega e foto opcional.
- Admin pode aprovar, rejeitar, marcar como recebida e marcar como distribuida.
- Admin pode atribuir doacao em especie a uma familia ou projeto.
- Painel admin recebeu dashboard visual com atalhos para as funcoes principais.
- Painel admin recebeu guia de preenchimento para facilitar uso por gerentes sem conhecimento tecnico.
- Tela de login do admin recebeu fundo com imagem, gradiente e card mais profissional.
- Listas do admin receberam filtros, tabelas e botoes com visual mais moderno.
- Menu lateral do admin recebeu fundo escuro com identidade ACSOL.
- Criado manual para migrar a base de dados para PostgreSQL.
- Redesign premium do Django Admin aplicado sem alterar models, views, URLs, permissões ou banco de dados.
- Login premium com glassmorphism, geometria visual, logo em destaque e botao com hover.
- Dashboard com cards modernos, indicadores, painel operacional e atalhos críticos.
- Header com pesquisa visual e atalho `Ctrl + K`.
- Ícones Lucide adicionados visualmente ao dashboard e sidebar.
- Tabelas, formulários, filtros e paginação receberam visual SaaS 2025.
- Corrigido alinhamento do login para remover título solto fora do card.
- Corrigido excesso de largura/overflow no dashboard e nas listas.
- Adicionado modo claro/escuro visual no admin.
- Adicionado botão visual para recolher/expandir sidebar.
- Adicionado espaço de gráfico ApexCharts no dashboard.
- Adicionada seção `Redes sociais` no dashboard principal.
- Links de redes sociais são editados em `Configurações do site`: Facebook, Instagram, YouTube, LinkedIn e WhatsApp.
- Login ajustado para o modelo enviado: card branco central, logo acima, campos simples e botão dourado.
- Admin ajustado para referência Materialize: topbar azul, sidebar clara, cards coloridos e layout mais limpo.
- Nova área pública `Projetos Realizados` criada na tela principal.
- `Projetos Realizados` usa o cadastro existente de `Projetos` com estado `Concluído`, foto e descrição.
- Admin pode editar esses projetos em `Projetos`, sem nova tabela.
- Admin refeito visualmente com base no estilo do projeto `condominio_kussanguluka`.
- Visual escuro pesado foi substituido por fundo claro, sidebar branca, topo limpo, acentos dourados, cards legiveis e botoes mais simples.
- Login foi mantido com fundo institucional escuro, mas o card ficou branco, centralizado e mais facil de usar.
- Fundo com imagem foi removido do admin para melhorar a visibilidade.
- Botoes do admin foram padronizados: azul petroleo para acoes comuns, dourado para acao principal e vermelho para apagar.
- Corrigido carregamento do dashboard do admin: `admin.site.index_template` agora aponta explicitamente para `admin/index.html`.
- Sidebar padrao do Django Admin foi substituida por menu institucional da ACSOL com Dashboard, Gestao, Conteudo e Configuracoes.
- Lista antiga `Todos os modulos` foi retirada da pagina inicial do admin para nao parecer a tela padrao do Django.
- Criada nova aba `Projetos feitos` no admin.
- `Projetos feitos` usa os mesmos dados de `Projetos`, mas mostra apenas projetos com estado `Concluido`.
- Ao criar por `Projetos feitos`, o sistema define automaticamente `Estado = Concluido` e `Progresso = 100`.
- Auditoria de permissoes feita: grupo `Gerente` tem permissoes de ver, adicionar, alterar e apagar em todos os 26 modelos registados no admin.
- Acoes de gerentes em `Users` e `Perfis de utilizadores` tambem passaram a entrar no historico/notificacoes.
- A estetica foi devolvida para o modo com internet/CDN, conforme solicitado.
- Site voltou a depender de Bootstrap, Bootstrap Icons, Google Fonts, Animate.css e imagens Pexels.
- Admin voltou a depender de Lucide e ApexCharts por CDN.
- Ficheiros locais de fallback offline foram removidos para evitar confusao.
- Configuracao HTTPS reforcada com `CSRF_TRUSTED_ORIGINS` e suporte a proxy HTTPS por `USE_X_FORWARDED_PROTO`.
- `Quero Doar` monetario foi colocado como indisponivel por padrao.
- Criada opcao no admin `Ativar Quero Doar` em `Configuracao de doacoes`.
- Criada mensagem editavel para explicar ao visitante quando `Quero Doar` estiver indisponivel.
- Admin pode preencher depois as instrucoes bancarias reais nacionais, internacionais, Multicaixa e gateway.
- Endpoint de doacao monetaria tambem bloqueia envio direto enquanto a opcao estiver desativada.
- Doacao em especie continua ativa e registrando dados no admin.
- Criado guia completo do admin: `docs/GUIA_ADMIN_COMPLETO_ACSOL.md`.
- Criado guia simples para utilizadores sem experiencia tecnica: `docs/GUIA_USO_SIMPLES_ACSOL.md`.

## Onde editar

- Fotos: `Admin > Galeria`, tipo `Imagem`.
- Videos: `Admin > Galeria`, tipo `Video` ou `YouTube`.
- Flyers/banners: `Admin > Flyers e banners`.
- Eventos: `Admin > Noticias e eventos`, tipo `Evento`.
- Equipa: `Admin > Equipa`.
- Doacoes monetarias recebidas: `Admin > Doacoes`.
- Ativar/desativar `Quero Doar`: `Admin > Configuracao de doacoes > Ativar Quero Doar`.
- Doacoes em especie: `Admin > Doacoes em especie`.
- Dados bancarios/instrucoes: `Admin > Configuracao de doacoes`.
- Provincias: `Admin > Divisoes provinciais`.
- Chatbot: `Admin > Chatbot IA`.
- Projetos realizados: `Admin > Projetos`, definir `Estado = Concluido`, marcar `Publicado`, adicionar imagem e descricao.
- Projetos feitos: `Admin > Projetos feitos`, adicionar foto, descricao, datas, beneficiarios e publicar.
- Valores do site: `Admin > Configuracoes do site > Secao: Os Nossos Valores`.
- Texto de voluntariado: `Admin > Configuracoes do site > Secao: Porque Ser Voluntario`.
- Texto de parceiros: `Admin > Configuracoes do site > Secao: Os Nossos Parceiros`.
- Parceiros reais: `Admin > Parceiros`, adicionar nome, logo, website e marcar ativo.
- Redes sociais: `Admin > Configuracoes do site`, preencher Facebook, Instagram, YouTube, LinkedIn e WhatsApp.
- Tamanho recomendado das fotos em `A Nossa Equipa`: 900 x 1200 px ou 1080 x 1350 px, formato vertical 3:4 ou 4:5.

## O que fica para Jason preencher

- Textos oficiais da ACSOL.
- Fotos reais da equipa.
- Fotos dos parceiros.
- Texto oficial dos valores, parceiros e voluntariado.
- Fotos reais da galeria.
- Videos reais ou links do YouTube.
- Eventos reais.
- Provincias/divisoes reais.
- Dados reais de pagamento.
- Ativar `Quero Doar` apenas depois de confirmar dados bancarios oficiais.
- Instrucoes reais para doacao em especie.
- Decisao sobre gateway de pagamento.
- Dominio e hospedagem.

## Validacao

- `manage.py check`: sem erros.
- Migracoes aplicadas.
- Pagina inicial: HTTP 200.
- Admin: HTTP 200.
- Formulario de doacao em especie testado com sucesso.
- Login admin, dashboard admin e listas principais testados com HTTP 200.
- Listas de utilizadores, configurações do site, doações e doações em espécie testadas com HTTP 200.
- Página inicial testada com `Projetos Realizados`: HTTP 200.
- Login admin, dashboard admin e lista de utilizadores continuam com HTTP 200 depois do novo ajuste visual.
- `collectstatic --noinput` executado depois das alteracoes visuais.
- Dashboard admin confirmado com `Dashboard Institucional`, `acsol-main-nav` e `acsol-dashboard` no HTML.
- Nova migracao aplicada: `core.0009_completedproject`.
- Testado acesso como gerente `francisco`: dashboard, projetos feitos, projetos, utilizadores, configuracoes, chatbot, doacoes monetarias e doacoes em especie retornaram HTTP 200.
- Site publico confirmado com referencias CDN/Pexels novamente.
- Nova migracao criada para controlo de disponibilidade do `Quero Doar`: `core.0010`.
- Nova migracao aplicada: `core.0012_siteconfig_texto_parceiros_siteconfig_texto_valores_and_more`.
- `serialize_instance(User #3/francisco)`: OK; grupo `Gerente` serializado sem erro.
- Pagina de edicao do utilizador #3 no admin: HTTP 200.
- Pagina de configuracao do site no admin: HTTP 200.
- `collectstatic --noinput`: executado depois do ajuste de fotos/equipa/parceiros.
- `Admin > Parceiros > Adicionar`: HTTP 200.
- Redes sociais existentes no banco: Facebook, Instagram, YouTube e WhatsApp; LinkedIn ainda vazio.
- `manage.py check`: sem erros depois da alteracao.
- `node --check static/js/site.js`: sem erros.
- `collectstatic --noinput`: executado depois da alteracao.
- Pagina inicial testada: HTTP 200 e mostra `Quero Doar indisponivel`.
- `/doacoes/instrucoes/?tipo=nacional`: devolve `available=false` enquanto `Quero Doar` estiver desligado.
- `/doacoes/interesse/`: bloqueia POST monetario com HTTP 403 enquanto `Quero Doar` estiver desligado.
- Auditoria do admin: 24 modelos do app `core` estao registados no Django Admin; nenhum modelo do `core` ficou fora do painel.
- Auditoria geral do frontend do admin realizada no login, dashboard, listas e formularios principais.
- Corrigido problema da sidebar personalizada do admin que podia ficar escondida pelo comportamento padrao do Django Admin.
- CSS do admin passou a ser carregado com versao `?v=20260629-admin-audit` para evitar cache visual antiga no navegador.
- Adicionada regra responsiva para o admin em telas menores, reduzindo risco de overflow no header/sidebar.
- Dashboard, `Configuracao de doacoes`, formulario de `Projetos`, `Galeria` e `Utilizadores` testados com HTTP 200 depois da correcao.
- Corrigido problema ao criar novo utilizador no admin.
- `Utilizadores > Adicionar` agora mostra apenas os campos de criacao do utilizador e senha.
- Perfil, funcao, foto, telefone, grupos e permissoes continuam disponiveis na tela de edicao depois da criacao.
- Testado fluxo completo: criar utilizador temporario, criar perfil automatico e abrir tela de edicao com perfil inline.
- PostgreSQL local corrigido para responder na porta `54321`.
- Corrigido conflito de porta causado por `postgresql.auto.conf` que ainda forçava `5432`.
- Criada base PostgreSQL `acsol_angola`.
- Criado ficheiro `.env` local apontando `DATABASE_URL` para PostgreSQL.
- Dados do SQLite exportados para `outputs/acsol_sqlite_backup_before_postgres.json`.
- Backup convertido para UTF-8 em `outputs/acsol_sqlite_backup_before_postgres_utf8.json`.
- Importados 104 objetos do SQLite para PostgreSQL.
- Django validado usando `django.db.backends.postgresql`, base `acsol_angola`, porta `54321`.
- Escrita na base PostgreSQL testada com criacao temporaria de utilizador e perfil automatico.
- `Quero Doar` confirmado indisponivel no frontend e bloqueado no backend ate o admin liberar.
- Criado script `scripts/start_postgres_54321.ps1` para verificar/iniciar PostgreSQL local se a porta estiver fechada apos reiniciar o computador.
- Observacao: servico Windows `postgresql-x64-18` apareceu como `Stopped`, mas o PostgreSQL esta ativo via `pg_ctl` e responde em `54321`.
- Verificado problema do `python manage.py runserver`: o servidor Django sobe, mas a pagina falha quando o PostgreSQL esta parado.
- PostgreSQL reiniciado via `pg_ctl` e porta `54321` validada.
- Criado script `scripts/run_local.ps1` para iniciar PostgreSQL e Django juntos no desenvolvimento local.
- Criado campo `Imagem da secao Quem Somos` em `Configuracoes do site`.
- A imagem principal da secao `Quem Somos` deixou de depender de Pexels e agora usa imagem cadastrada no admin, logo enviado no admin ou logo local como fallback.
- Ajustado CSS da imagem do `Quem Somos` para evitar corte ruim quando estiver usando logo/foto institucional.
- Nova migracao aplicada: `core.0011_siteconfig_imagem_sobre`.
- Site validado com HTTP 200 depois da alteracao e do PostgreSQL ativo.

## Documentos uteis

- `docs/GUIA_ADMIN_ACSOL.md`
- `docs/GUIA_ADMIN_COMPLETO_ACSOL.md`
- `docs/GUIA_USO_SIMPLES_ACSOL.md`
- `docs/GUIA_POSTGRESQL_ACSOL.md`
# Atualizacao para PythonAnywhere Free

Data: 2026-07-07

## Objetivo desta fase

Preparar a copia `Acsol-Angola 1 - Cópia` para ir ao ar primeiro em hospedagem gratis, mantendo o maximo de funcoes do sistema e evitando custos de API e banco externo.

## Feito nesta atualizacao

- Configuracao ajustada para aceitar dominio do PythonAnywhere por variavel `PYTHONANYWHERE_DOMAIN`.
- URLs de ficheiros estaticos e media padronizadas como `/static/` e `/media/`.
- Chatbot passou a suportar o provedor `Respostas programadas`, sem depender de Llama, OpenAI ou Gemini.
- Adicionado campo `resposta_padrao` no Chatbot IA para responder quando nao houver FAQ correspondente.
- Admin do Chatbot atualizado para explicar o modo gratis.
- Dados iniciais de doacoes monetarias deixaram de trazer dados bancarios falsos.
- `Quero Doar` monetario continua desligado por padrao ate o admin preencher dados oficiais e ativar.
- Criado script de backup para SQLite e media: `scripts/pythonanywhere_backup.sh`.
- Criado manual de hospedagem gratis: `docs/GUIA_PYTHONANYWHERE_FREE_ACSOL.md`.
- `.gitignore` atualizado para ignorar pasta `backups/`.

## Validacao tecnica executada

- `python manage.py check`: sem problemas.
- `python manage.py migrate`: migração `core.0013_chatbot_programado` aplicada na copia local.
- `python manage.py collectstatic --noinput`: executado com sucesso.
- `python manage.py makemigrations --check --dry-run`: sem alteracoes pendentes.

## Percentagem geral estimada

- Sistema Django funcional: 90%
- Painel admin e gerentes: 88%
- Conteudo editavel pelo admin: 90%
- Doacoes monetarias seguras/desativadas: 95%
- Doacao em especie: 90%
- Chatbot economico programado: 90%
- Preparacao para PythonAnywhere Free: 85%
- Documentacao para hospedagem: 85%

Percentagem geral atual: **89%**

## O que falta fazer

- Testar deploy real no PythonAnywhere com o nome de usuario final.
- Criar `.env` real no servidor, sem colocar no GitHub.
- Rodar `migrate`, `seed_initial_data` e `collectstatic` no PythonAnywhere.
- Mapear `/static/` e `/media/` no painel Web do PythonAnywhere.
- Fazer upload das imagens reais da ACSOL pelo admin.
- Preencher links reais de redes sociais, parceiros e contactos.
- Trocar senhas iniciais no admin depois do primeiro acesso.
- Ativar `Quero Doar` apenas quando existirem dados bancarios oficiais confirmados.

## Recomendacao atual

Para comecar gratis, usar PythonAnywhere Free com SQLite e chatbot programado. Nao usar Netlify para o sistema completo, porque Netlify nao executa Django, admin, banco de dados e uploads.
