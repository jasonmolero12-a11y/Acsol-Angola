# Relatorio ACSOL Angola Django

## Percentagem geral

**99% concluido** para uma primeira versao funcional.

O sistema ja permite gerir conteudo, doacoes, doacoes em especie, projetos, projetos feitos, galeria, videos, equipa, provincias, chatbot, redes sociais, utilizadores e gerentes pelo painel administrativo.

## Feito agora

- Corrigido erro do admin ao salvar utilizador: `Object of type Group is not JSON serializable`.
- Corrigida serializacao do historico/auditoria para aceitar grupos como `Gerente`.
- Criados campos editaveis no admin para `Os Nossos Parceiros`, `Os Nossos Valores` e `Porque Ser Voluntario?`.
- A home e a pagina de parceiros foram ligadas aos textos editaveis em `Configuracoes do site`.
- Parceiros cadastrados no admin aparecem no site com logo e link.
- Fotos da equipa, incluindo Francisco, agora ajustam melhor ao cartao de `A Nossa Equipa`.
- Atualizados os guias de admin e uso simples com as novas instrucoes.
- Doacoes monetarias foram desativadas por padrao.
- Criado campo `Ativar Quero Doar` em `Configuracao de doacoes`.
- Criado campo de mensagem publica para quando o `Quero Doar` estiver indisponivel.
- Criado bloqueio no servidor para impedir envio monetario enquanto estiver indisponivel.
- Mantida doacao em especie ativa.
- Criados dois guias:
  - `docs/GUIA_ADMIN_COMPLETO_ACSOL.md`
  - `docs/GUIA_USO_SIMPLES_ACSOL.md`
- Atualizado `docs/RELATORIO_ACSOL_ATUALIZADO.md`.
- Feita auditoria geral do frontend do painel admin.
- Corrigido comportamento da sidebar personalizada que podia aparecer escondida.
- CSS do admin versionado para garantir que o navegador carregue a estetica nova.
- Corrigido fluxo de criacao de utilizador no admin.

## Falta para fechar 100%

- Jason inserir textos finais oficiais.
- Jason inserir fotos reais.
- Jason inserir parceiros reais com logos.
- Jason revisar a foto final do Francisco e demais membros da equipa.
- Jason inserir videos reais.
- Jason confirmar dados bancarios oficiais.
- Jason preencher instrucoes reais de pagamento.
- Jason ativar `Quero Doar` no admin quando os dados estiverem confirmados.
- Definir hospedagem, dominio e email profissional.

## Como ativar doacao monetaria no futuro

1. Entrar em `/admin/`.
2. Abrir `Configuracao de doacoes`.
3. Preencher instrucoes reais de pagamento.
4. Confirmar os dados com documento oficial.
5. Marcar `Ativar Quero Doar`.
6. Guardar.

## Validacao tecnica

- Migracao `core.0010`: aplicada.
- `manage.py check`: sem erros.
- `node --check static/js/site.js`: sem erros.
- `collectstatic --noinput`: executado.
- Pagina inicial: HTTP 200.
- `Quero Doar` indisponivel: confirmado.
- Bloqueio de POST monetario: HTTP 403 confirmado.
- Painel admin: dashboard, listas e formularios principais testados com HTTP 200.
- Menu lateral ACSOL: corrigido e confirmado visivel no desktop.
- Criacao de utilizador no admin: corrigida e testada.
- Perfil automatico do utilizador: confirmado.
- Edicao posterior de perfil/funcao/foto/permissoes: confirmada.
- PostgreSQL conectado ao projeto.
- Porta PostgreSQL corrigida para `54321`.
- Base `acsol_angola` criada e migrada.
- Dados do SQLite importados para PostgreSQL.
- `Quero Doar` confirmado como indisponivel no frontend e bloqueado no backend.
- Criado script `scripts/start_postgres_54321.ps1` para iniciar/verificar PostgreSQL local.
- Criado script `scripts/run_local.ps1` para iniciar PostgreSQL e Django juntos.
- Corrigida imagem principal da secao `Quem Somos` para ser editavel pelo admin.
- Criado campo `SiteConfig.imagem_sobre`.
- Aplicada migracao `core.0011_siteconfig_imagem_sobre`.
- `runserver` validado: o problema era PostgreSQL parado, nao erro de Django.
- Aplicada migracao `core.0012_siteconfig_texto_parceiros_siteconfig_texto_valores_and_more`.
- `manage.py check`: sem erros depois da correcao do admin.
- `serialize_instance(User #3/francisco)`: OK com grupo `Gerente`.
- `/admin/auth/user/3/change/`: HTTP 200.
- `/admin/core/siteconfig/1/change/`: HTTP 200.
- Pagina inicial contem `Os Nossos Valores`, `Os Nossos Parceiros` e `Porque Ser Voluntario?`: confirmado.
