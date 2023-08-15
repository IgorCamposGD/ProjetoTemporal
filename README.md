# Projeto Temporal com Python
Este é um projeto que utiliza a lib temporalio da liguaguem python. Onde temos uma pizzaria e com comandos tctl realizamos o pedido de uma pizza passando nome, endereço e sabor. Usamos a lib do temporal para realizar um workflow de longa duração, que segue algumas atividades nescessarias para o pedido ser criado até ficar pronto para entrega de acordo com os dados passados, com a lib do temporal tambem podemos acessar o em qual status o pedido.

# Pré-requisitos:
Antes de começar, certifique-se de ter o Docker instalado em seu sistema. Se você ainda não tem o Docker instalado, siga as instruções em https://docs.docker.com/get-docker/ para instalar a versão adequada ao seu sistema operacional.

OBS: ajustar o .env como no exemplo env_example

Executando o projeto:
Para executar o projeto, siga os seguintes passos:

OBS: Para funcionar voce precisa ter um temporal server. Recomendamos usar o: https://github.com/temporalio/temporalite e seguir o passo a passo do mesmo para configura-lo. 

**1 - Clone o repositório para o seu ambiente local:**

```bash
git clone https://github.com/IgorCamposGD/ProjetoTemporal
```
**2 - Acesse o diretório do projeto:**

```bash
cd ProjetoTemporal
```

**3 - Após voce subir o temporal server, der o comando abaixo para criar o seu namespace antes de subir a docker do sistema:**

```bash
tctl --namespace your-namespace namespace register
```
OBS: Voce precisará de um client para passar os comandos para o temporal server caso voce esteja usando o temporal lite que foi recomendado acima. Recomandos usar o https://hub.docker.com/r/temporalio/admin-tools. 

**4 - Em seguida, você pode executar o comando:**

```bash
make build
```

```bash
make up
```

**5 - acessar o temporal com seu ip local na porta 8233:**

```bash
http://seuip:8233
```

Após validar que o seu worflow de longa duração está rodando no temporal server, agora voce pode realizar o pedido da pizza e ir monitorando os status.

**6 - realizar um pedido:**

OBS1: O sabor só pode ser um dos sitados no comando, caso esteja vazio ou diferente será retornado erro.

OBS2: Caso tenha alterado os valores de workflow_id e o namespace alterar tbm no comando.

```bash
tctl --namespace pizzahut workflow signal --workflow_id "PizzahutWorkflow-workflow" --name "new_order" --input '{\"name\": \"NOME\" , \"address\": \"ENDEREÇO\", \"flavor\": \"Calabresa,Frango ou Chocolate\"}'
```

OBS: Se voce tiver no sistema operacional Linux retire as barras antes das aspas.

**7 - Após realizar o pedido voce pode consultar o status do pedido com o comando:**

OBS: no input colocar o ID gerado na primeira ativiade, voce pode pegar o id no temporal server ou no log docker, com o comando make logs.

```bash
tctl --namespace pizzahut workflow query --workflow_id PizzahutWorkflow-workflow --query_type "get_order_status" --input 1111
```

**7 - Após chegar no status "Out_of_delivery" ele só vai ficar como "delivery" caso seja encaminhado um sinal:**

```bash
tctl --namespace pizzahut workflow signal --workflow_id "PizzahutWorkflow-workflow" --name "confirm_delivery" --input 1111
```
