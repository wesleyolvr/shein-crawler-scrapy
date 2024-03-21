# No seu código Python
import os

from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


# Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', '3600'))

# Kafka
KAFKA_SERVERS = os.getenv('KAFKA_SERVERS', 'localhost:9093')
KAFKA_TOPIC_url = os.getenv('KAFKA_TOPIC_url', 'url_to_spider')
KAFKA_TOPIC_products = os.getenv('KAFKA_TOPIC_products', 'products')
KAFKA_TOPIC_grupo_id = os.getenv('KAFKA_TOPIC_grupo_id', 'my_consumer_group')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = (
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
