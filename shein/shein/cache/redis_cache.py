import json
import redis
import logging

from config import REDIS_EXPIRE_TIME, REDIS_URL

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self):
        try:
            # Conectar-se ao servidor Redis usando as variáveis do arquivo config.py
            self.redis_client = redis.Redis.from_url(REDIS_URL)
            self.expire_time = REDIS_EXPIRE_TIME
        except Exception as e:
            logger.error(f"Erro ao conectar-se ao Redis: {e}")
            self.redis_client = None

    def check_cache(self, key):
        if self.redis_client:
            return self.redis_client.exists(key)
        else:
            logger.error("Não foi possível verificar o cache, conexão com o Redis não estabelecida.")
            return False

    def set_cache(self, key, value):
        if self.redis_client:
            self.redis_client.setex(key, self.expire_time, value)
            logger.debug(f"Dados definidos no cache para a chave '{key}'")
        else:
            logger.error("Não foi possível definir o cache, conexão com o Redis não estabelecida.")

    def get_cache(self, key):
        if self.redis_client:
            cached_data = self.redis_client.get(key)
            if cached_data:
                logger.debug(f"Dados recuperados do cache para a chave '{key}'")
                return json.loads(cached_data.decode('utf-8'))  # Decodificar os dados JSON
            else:
                logger.debug(f"Nenhum dado encontrado no cache para a chave '{key}'")
                return None
        else:
            logger.error("Não foi possível obter o cache, conexão com o Redis não estabelecida.")
            return None

    def cache_data(self, key, data):
        if self.redis_client:
            # Verificar se os dados já estão no cache
            if not self.check_cache(key):
                # Se não estiverem, armazenar os dados no cache
                self.set_cache(key, json.dumps(data))  # Codificar os dados JSON
        else:
            logger.error("Não foi possível armazenar no cache, conexão com o Redis não estabelecida.")
