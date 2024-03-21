# Crawler Shein

# Bem-vindo ao projeto de Web Scraping automatizado do site Shein!

O projeto automatiza a obtenção de informações sobre produtos do site Shein.

## Funcionalidades

- **Web Scraping Automatizado com Scrapy:** Utiliza o framework Scrapy para extrair dados de produtos do site Shein. Os dados são recebidos via Apache Kafka, onde são processados e retornados como JSON para a API. 🌐📦
- **Armazenamento em Banco de Dados e Cache Redis:** Utiliza um banco de dados SQLite para armazenar os dados extraídos e um cache Redis para armazenar informações sobre a última extração de cada categoria. Os dados são atualizados no banco de dados e no cache Redis somente se houver diferença no preço do produto. 🗃️🔍
- **Validação de Dados com Pydantic:** Utiliza o Pydantic para validar os dados extraídos antes de armazená-los no banco de dados. ⚙️🔍
- **API FastAPI:** Disponibiliza uma API utilizando o FastAPI para gerenciar os endpoints da aplicação. A API recebe os dados dos produtos via Kafka, valida e verifica se o produto está presente no cache Redis antes de atualizar o banco de dados e o cache. 🚀🔌
- **Apache Kafka:** Utiliza o Apache Kafka para permitir a comunicação assíncrona e distribuída entre os módulos do projeto, como o crawler, a API e o banco de dados. 📡🔗




## Instalação

Para executar este projeto em sua máquina local, siga os passos abaixo:

1. **Clone o repositório**:
   ```sh
   git clone https://github.com/wesleyolvr/shein-crawler-scrapy.git
   ```

2. **Crie e Ative um Ambiente Virtual**:
   - No terminal, navegue até o diretório do seu projeto:
     ```sh
     cd /path/to/your/project
     ```
   - Crie um ambiente virtual:
     ```sh
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     - No Windows:
     ```sh
       venv\Scripts\activate
     ```
     - No macOS/Linux:
     ```sh
       source venv/bin/activate
     ```

3. **Ajuste os arquivos de variaveis de ambiente**:
   Renomeie o arquivo `config_sample.ini` para `config.ini` e insira as informações do banco de dados, Redis e do Kafka conforme necessário.


4. **Cria e inicie os serviços Kafka, Zookeeper, Redis, KafDrop, PgAdmin**:
   ```sh
   docker-compose up -d
   ```

5. **Inicie script consumidor dos produtos**:
   ```sh
   python start_consumidor.py
   ```
6. **Inicie a API FastAPI**:
   ```sh
   uvicorn api.main:app --reload
   ```
7. **Inicie o script do Spider:**
   ```sh
   python shein/run_spider.py
   ```

## Uso

Depois de seguir as etapas de instalação, a API estará disponível em `http://localhost:8000` e você pode acessar a documentação interativa do Swagger em `http://localhost:8000/docs`.

### Endpoints disponíveis:

- **`/produtos`**: Lista todos os produtos extraídos do site Shein.
- **`/produtos/{product_id}`**: Retorna um produto específico pelo ID.

## Contribuição

Se você deseja contribuir com melhorias para este projeto, siga as diretrizes abaixo:

1. Crie uma nova branch:
   ```sh
   git checkout -b feature-nova-funcionalidade
   ```

2. Faça suas alterações e commit:
   ```sh
   git commit -am 'Adiciona nova funcionalidade'
   ```

3. Envie para o GitHub:
   ```sh
   git push origin feature-nova-funcionalidade
   ```

4. Crie um novo Pull Request e aguarde a revisão.


## Próximos Passos

- **Serviço de Comparação de Preços:** Desenvolver um serviço que compara os preços atuais dos produtos com seus históricos para identificar oportunidades de compra. 💰🔍

- **Dockerização do Projeto:** Utilizar Docker para empacotar e distribuir todo o projeto, garantindo portabilidade, consistência e facilitando a escalabilidade. Isso simplificará a gestão de dependências e garantirá uma implantação mais eficiente. 🐳🚀



## Licença

Este projeto é licenciado sob a [MIT License](https://opensource.org/licenses/MIT) - veja o arquivo [LICENSE](https://github.com/seu-usuario/nome-do-projeto/blob/main/LICENSE) para mais detalhes. 🚀🤝