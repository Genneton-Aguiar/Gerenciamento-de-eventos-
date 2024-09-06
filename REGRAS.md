Requisitos do Projeto:
Gerenciamento de Eventos:

[CHECK] Endpoints para criar, listar, atualizar e deletar eventos. Campos incluem nome, descrição, data, local, e capacidade máxima.
[CHECK] Endpoint para exibir os detalhes completos de um evento, incluindo os inscritos e informações adicioanais.

Gestão de Inscrições:

[CHECK] Endpoint para que os usuários possam se inscrever em eventos, respeitando a capacidade máxima do evento.
[CHECK] Endpoint para que os usuários possam cancelar suas inscrições em eventos, liberando vagas para outros interessados. O cancelamento só poderá ser feito em até 24h antes da data de realização do evento.
[CHECK] Endpoint para listar todos os eventos nos quais um usuário está inscrito.

Cadastro de usuários:

[CHECK] Implementar um cadastro de usuários básico, o usuário deve escolher entre usuário comum ou criador de eventos.

Autenticação e Autorização:

#Implementar autenticação para garantir que apenas usuários registrados possam se inscrever em eventos ou criar novos eventos (caso o sistema permita que usuários comuns criem eventos).

#Utilizar autenticação JWT.

Busca e Filtros:

#Implementar filtros na listagem de eventos para que os usuários possam buscar eventos por intervalo data, local ou nome do evento.

Exportação de Dados (EXTRA):

#Permitir que os organizadores exportem a lista de inscritos em formato CSV ou PDF.

