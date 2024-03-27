# No seu código Python
import os

from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


# Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')
REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', '3600'))

# Kafka
KAFKA_SERVERS = os.getenv('KAFKA_SERVERS', 'kafka:9092')
KAFKA_TOPIC_url = os.getenv('KAFKA_TOPIC_url', 'url_to_spider')
KAFKA_TOPIC_products = os.getenv('KAFKA_TOPIC_products', 'products')
KAFKA_TOPIC_grupo_id = os.getenv('KAFKA_TOPIC_grupo_id', 'my_consumer_group')
CONSUMERS_API = int(os.getenv('CONSUMERS_API', '2'))

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URL = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
