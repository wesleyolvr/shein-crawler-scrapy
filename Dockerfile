# Use a imagem oficial do Python 3.11 como base
FROM python:3.10

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip
# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do diretório do projeto para o diretório de trabalho
COPY . .

# Exponha a porta que o aplicativo estará ouvindo
EXPOSE 5000

# Defina o comando para iniciar o aplicativo
CMD ["python", "start_consumidor.py"]