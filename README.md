
## Como Executar o Projeto

Toda a infraestrutura do projeto (API + Bancos + Brokers) está configurada para iniciar com um único comando utilizando o Docker Compose.

### Passo a Passo

1. Clonar ou acessar a pasta do projeto:
   ```bash
   cd meu_projeto

2. Configurar as Variáveis de Ambiente (Opcional para Local):
Caso queira rodar scripts ou testes locais fora do container futuramente, crie o arquivo .env a partir do modelo:

cp .env.example .env


3. Subir todos os serviços com o Docker Compose:
Execute o comando abaixo na raiz do projeto.
Ele fará o build da imagem da API e baixará as imagens oficiais do MongoDB, RabbitMQ, Kafka e Zookeeper, inicializando-os na ordem correta de dependência:

docker-compose up --build

4. Verificar os serviços:
A API estará disponível e pronta para receber requisições em: http://localhost:8000


## Como Executar os Testes Automatizados
Os testes automatizados foram desenvolvidos utilizando pytest e httpx para chamadas assíncronas assíncronas. Eles validam o fluxo de cadastro e listagem mockando os brokers de mensageria para garantir isolamento.

Com os containers em execução, abra um novo terminal e execute os testes diretamente dentro do container da API utilizando o comando:

docker-compose exec fastapi-api pytest