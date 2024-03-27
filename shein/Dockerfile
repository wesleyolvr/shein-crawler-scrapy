# Use a imagem oficial do Python 3.11 com Alpine como base
FROM python:3.11-alpine

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instale as dependências necessárias
RUN apk update && \
    apk add --no-cache build-base librdkafka-dev && \
    pip install --upgrade pip 

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do diretório do projeto para o diretório de trabalho
COPY . .

# Defina o comando para iniciar o aplicativo
CMD ["python", "run_spider.py"]
