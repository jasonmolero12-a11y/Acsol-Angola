# Guia completo do Admin - ACSOL Angola

Este guia explica como o administrador e os gerentes devem usar o painel da ACSOL Angola sem mexer no codigo.

## 1. Acesso ao painel

1. Abrir o navegador.
2. Entrar em `/admin/`.
3. Usar o utilizador e senha definidos pelo administrador.
4. Depois de entrar, usar o menu lateral para escolher a area que deseja alterar.

Conta principal atual:

- Utilizador: `jason`
- Nome: `Jason`
- Senha: definida no ambiente local/produção em `ACSOL_ADMIN_PASSWORD`.

Por seguranca, nao publique senhas reais no GitHub. Depois de hospedar, altere a senha no painel admin.

## 2. Regra principal

Quase todo conteudo visivel no site deve ser alterado pelo admin:

- Textos institucionais.
- Fotos.
- Videos.
- Flyers.
- Projetos.
- Projetos feitos.
- Noticias.
- Eventos.
- Equipa.
- Provincias.
- Doacoes.
- Doacoes em especie.
- Chatbot.
- Redes sociais.

Evite alterar ficheiros do projeto para mudar conteudo normal. Use o painel.

## 2.1. Subir o sistema localmente

Como a aplicacao esta ligada ao PostgreSQL local, primeiro confirme que a porta `54321` esta ativa.

Forma recomendada:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_local.ps1
```

Esse script verifica/inicia o PostgreSQL local e depois executa o Django em `127.0.0.1:8000`.

Se executar apenas:

```powershell
python manage.py runserver
```

e o site nao abrir, normalmente o motivo e o PostgreSQL estar parado.

## 3. Doacoes monetarias: Quero Doar

A opcao `Quero Doar` esta desativada por padrao porque ainda nao existem dados bancarios oficiais confirmados.

Para ativar no futuro:

1. Entrar no admin.
2. Abrir `Configuracao de doacoes`.
3. Editar o registo existente.
4. Preencher as instrucoes reais:
   - `Instrucoes nacionais`.
   - `Instrucoes internacionais`.
   - `Instrucoes multicaixa`.
   - `Instrucoes gateway`.
   - `Gateway URL`, se houver pagamento online.
5. Confirmar se os dados estao corretos.
6. Marcar `Ativar Quero Doar`.
7. Guardar.

Enquanto `Ativar Quero Doar` estiver desligado, o visitante ve uma mensagem de indisponibilidade e nao consegue enviar uma doacao monetaria.

## 4. Mensagem de indisponibilidade

Em `Configuracao de doacoes`, o campo `Mensagem quando Quero Doar estiver indisponivel` controla o texto mostrado ao visitante.

Use uma mensagem curta, por exemplo:

`A opcao Quero Doar esta temporariamente indisponivel enquanto confirmamos os dados bancarios oficiais. Para apoiar agora, contacte a ACSOL.`

## 5. Doacao em especie

A doacao em especie continua ativa porque nao depende de dados bancarios.

O visitante preenche:

- Nome.
- Email.
- Telefone.
- Tipo de item.
- Quantidade.
- Estado do item.
- Descricao.
- Localizacao de entrega.
- Foto opcional.

No admin, abrir `Doacoes em especie` para:

- Aprovar.
- Rejeitar.
- Marcar como recebida.
- Marcar como distribuida.
- Atribuir a uma familia ou projeto.
- Escrever observacoes internas.

## 6. Projetos e projetos feitos

Use `Projetos` para cadastrar todos os projetos.

Use `Projetos feitos` quando o projeto ja foi realizado. Esta area mostra apenas projetos concluidos.

Para aparecer no site:

1. Adicionar foto.
2. Escrever titulo.
3. Escrever descricao.
4. Definir estado correto.
5. Marcar `Publicado`.
6. Guardar.

## 7. Galeria e videos

Use `Galeria e videos`.

Para fotos:

- Tipo: `Imagem`.
- Adicionar imagem.
- Escolher categoria.
- Marcar `Publicado`.

Para videos:

- Tipo: `Video` para ficheiro enviado.
- Tipo: `YouTube` para link externo.
- Marcar `Publicado`.

## 8. Flyers e banners

Use `Flyers e banners` para trocar imagens promocionais sem alterar codigo.

Campos importantes:

- Titulo.
- Imagem.
- Posicao.
- Link opcional.
- Ativo.

## 9. Noticias e eventos

Use `Noticias e eventos`.

Para evento:

- Tipo: `Evento`.
- Adicionar titulo, descricao, data e imagem.
- Marcar `Publicado`.

Para noticia:

- Tipo: `Noticia`.
- Adicionar conteudo e imagem.
- Marcar `Publicado`.

## 10. Equipa

Use `Equipa` para alterar a area `A Nossa Equipa`.

Pode adicionar:

- Nome.
- Cargo.
- Foto.
- Biografia.
- Ordem.
- Estado ativo.

Recomendacao para fotos:

- usar fotos verticais ou quadradas;
- tamanho recomendado: `900 x 1200 px` ou `1080 x 1350 px`;
- formato ideal: vertical 3:4 ou 4:5;
- evitar imagem muito distante;
- se a foto cortar mal, reenviar uma imagem com mais espaco acima da cabeca;
- o site ajusta a foto automaticamente ao cartao da equipa.

## 11. Provincias

Use `Divisoes provinciais` para cadastrar presenca da ACSOL nas provincias.

Campos recomendados:

- Provincia.
- Municipio.
- Endereco.
- Contacto.
- Coordenadas ou mapa, quando existir.
- Estado ativo.

## 12. Redes sociais

Use `Configuracoes do site`.

Pode preencher:

- Facebook.
- Instagram.
- YouTube.
- LinkedIn.
- WhatsApp.

Estes links aparecem no painel e no site conforme o template.

No WhatsApp pode preencher numero simples, por exemplo `244923456789`, ou link completo. O site transforma numero em link `wa.me`.

## 12.1. Parceiros com logo e link

Use `Parceiros`.

Campos principais:

- `Nome`: nome oficial do parceiro.
- `Logo`: imagem do parceiro.
- `Website`: link completo, por exemplo `https://exemplo.com`.
- `Ativo`: marcado para aparecer no site.

O logotipo recomendado e quadrado ou horizontal, preferencialmente PNG com fundo transparente.

## 12.2. Textos editaveis do site

Use `Configuracoes do site` para alterar estas areas sem mexer no codigo:

- `Secao: Os Nossos Valores`: titulo, texto introdutor e lista de valores.
- `Secao: Porque Ser Voluntario`: titulo e texto principal.
- `Secao: Os Nossos Parceiros`: titulo e texto principal.
- `Institucional`: missao, visao e valores gerais.

Na lista de valores, escreva um valor por linha.

## 12.3. Foto da secao Quem Somos

Use `Configuracoes do site > Imagem da secao Quem Somos`.

Recomendacao:

- usar foto horizontal;
- evitar imagem muito pequena;
- preferir imagem da equipa, acao social ou documento institucional;
- se ficar vazio, o site mostra o logo da ACSOL como provisoria.

## 13. Chatbot IA

Use `Chatbot IA`.

Pode alterar:

- Chave da API.
- Provedor.
- Modelo.
- Mensagem inicial.
- Modo livre ou restrito.
- Assuntos permitidos.
- Voz ativa.
- Perguntas frequentes.

Para limitar o chatbot a ACSOL e direitos humanos, use o modo restrito.

## 14. Gerentes

O admin pode criar e gerir gerentes em `Utilizadores`.

Regras:

- Gerente pode gerir o sistema conforme permissoes.
- Acoes importantes ficam no historico.
- Admin pode bloquear/desbloquear contas.
- Admin pode redefinir senha.

Para criar um gerente:

1. Abrir `Utilizadores`.
2. Clicar em `Adicionar`.
3. Escrever o nome de utilizador e a senha.
4. Guardar.
5. Na tela seguinte, preencher nome, email e marcar `Status de equipe` para permitir acesso ao painel.
6. Em `Grupos`, escolher `Gerente`.
7. Em `Perfil de utilizador`, escolher a funcao `Gerente`, adicionar foto/telefone se houver.
8. Guardar.

Se for uma conta administrativa principal, usar a funcao `Administrador` no perfil e manter permissao de superutilizador apenas para pessoas de confianca.

## 15. Cuidados antes de publicar

Antes de ativar qualquer conteudo:

- Confirmar se a foto e correta.
- Confirmar se o texto nao tem erros.
- Confirmar se o item esta marcado como `Publicado` ou `Ativo`.
- Confirmar dados bancarios com documento oficial antes de ativar `Quero Doar`.
