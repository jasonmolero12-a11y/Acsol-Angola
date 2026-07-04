# Chatbot IA e Doacoes

## Chatbot IA com Llama API

O chatbot tem um menu proprio no painel administrativo: `Chatbot IA`.

No admin, pode alterar:

- chave da API
- URL da API
- modelo utilizado
- mensagem inicial
- prompt do sistema
- perguntas frequentes

## Como colocar a API no sistema

1. Acesse `http://127.0.0.1:8000/admin/`.
2. Entre com o utilizador administrativo.
3. Abra `Chatbot IA`.
4. Edite `Chatbot IA ACSOL`.
5. Preencha:
   - `Provider`: Llama API
   - `API key`: a chave recebida do fornecedor
   - `API url`: `https://api.llama-api.com/chat/completions` ou a URL do fornecedor usado
   - `Modelo`: o modelo desejado, por exemplo `llama-3.1-8b-instruct`
6. Salve.

Se a chave da API nao estiver preenchida, o chatbot responde usando as perguntas frequentes locais e informa que falta configurar a chave.

## Doacoes

A pagina publica mostra o fluxo profissional:

- explicacao do impacto
- botao/formulario `Quero Doar`
- valor sugerido
- nome, email, telefone
- tipo de doacao: nacional, internacional, Multicaixa Express ou gateway online
- upload opcional de comprovativo

As instrucoes do tipo escolhido aparecem quando o visitante seleciona o tipo de doacao. Esses dados ficam guardados no admin em `Configuracao de doacoes`, para o administrador poder alterar sem mexer no codigo.

Todas as intencoes de doacao ficam guardadas no admin em `Doacoes`. As candidaturas de voluntariado ficam guardadas em `Candidaturas de voluntarios`.

## Fase avancada

Ainda falta implementar:

- gateway real de pagamento
- Multicaixa Express com referencia automatica
- historico detalhado do doador
- emissao automatica de recibos
- dashboard financeiro
