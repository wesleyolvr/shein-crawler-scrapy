import os

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URL do Redis e o tempo de expiração do ambiente
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_EXPIRE_TIME = int(
    os.getenv('REDIS_EXPIRE_TIME', 345600)
)  # 4 dias em segundos
KAFKA_TOPIC_products = os.getenv('KAFKA_TOPIC_products', 'products')
KAFKA_TOPIC_url = os.getenv('KAFKA_TOPIC_url', 'url_to_spider')
KAFKA_SERVERS = os.getenv('KAFKA_SERVERS', 'localhost:9093')
