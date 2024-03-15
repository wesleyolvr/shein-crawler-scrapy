import os

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URL do Redis e o tempo de expiração do ambiente
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_EXPIRE_TIME = int(
    os.getenv('REDIS_EXPIRE_TIME', 345600)
)  # 4 dias em segundos
KAFKA_TOPIC_IN = os.getenv('KAFKA_TOPIC_IN', 'produtos_shein')
KAFKA_TOPIC_OUT = os.getenv('KAFKA_TOPIC_OUT', 'produtos')
KAFKA_SERVERS = os.getenv('KAFKA_SERVERS', 'localhost:9093')
