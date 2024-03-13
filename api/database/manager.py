import json
from datetime import datetime

from api.schemas.product import ProductCreate
from api.schemas.price_history import PriceHistoryUpdate
from db.database import DATABASE_URL
from db.manager import DatabaseManager
from kafka.consumer import KafkaConsumer
from cache.redis_cache import RedisCache


class ProdutoProcessor:
    def __init__(self, kafka_topic):
        self.kafka_consumer = KafkaConsumer(kafka_topic)
        self.db_manager = DatabaseManager(database_url=DATABASE_URL)
        self.cache = RedisCache()

    def processar_produto(self):
        try:
            for mensagem in self.kafka_consumer.consume():
                produto = json.loads(mensagem)
                key = produto["id"]
                # checa se o produto esta no cache e se o valor de price_real é diferente do que esta no cache, se for diferente ou se não existir, armazena no cache
                if (
                    self.cache.check_cache(key)
                    and self.cache.get_cache(key)["price_real"] == produto["price_real"]
                ):
                    print("Dados armazenados no cache.")
                    continue
                produto_bd = self.db_manager.get_product_by_id(produto["id"])
                if produto_bd:
                    # Comparar preços
                    if abs(produto_bd.price_real - float(produto["price_real"])) > 1:
                        print(
                            f"O preço do produto {produto['id']} foi alterado de {produto_bd.price_real} para {produto['price_real']}"
                        )
                        produto_bd.price_real = produto["price_real"]
                        update_data = PriceHistoryUpdate(
                            product_id=produto_bd.id,  # Substitua 'product_id' pelo nome correto do campo
                            new_price=produto["price_real"],
                            date=produto["datetime_collected"],
                            price=produto["price_real"],
                            price_real_symbol=produto["price_real_symbol"],
                            price_real=produto["price_real"],
                            price_us_symbol=produto["price_us_symbol"],
                            price_us=produto["price_us"],
                            discountPrice_price_real=produto[
                                "discountPrice_price_real"
                            ],
                            discountPrice_us=produto["discountPrice_us"],
                            discountPrice_real_symbol=produto[
                                "discountPrice_real_symbol"
                            ],
                            discountPrice_price_us_symbol=produto[
                                "discountPrice_price_us_symbol"
                            ],
                        )
                        self.db_manager.update_product_price(update_data)
                        mensagem = json.dumps(produto)
                        self.cache.set_cache("cached_data", mensagem)
                else:
                    # Criar um novo produto
                    produto_create = ProductCreate(**produto)
                    self.db_manager.create_product(produto_create)
                    print(f"O produto {produto['id']} foi adicionado")
                    mensagem = json.dumps(produto)
                    self.cache.set_cache(f"product_{produto['id']}", mensagem)

        except KeyboardInterrupt:
            self.kafka_consumer.close()
