import json

from api.schemas.price_history import PriceHistoryUpdate
from api.schemas.product import ProductCreate
from cache.redis_cache import RedisCache
from db.database import DATABASE_URL
from sqlalchemy.orm import Session
from db.database import get_db
from db.manager import DatabaseManager
from kafka.consumer import KafkaConsumer


class ProdutoProcessor:
    def __init__(self, kafka_topic,kafka_group_id):
        self.kafka_consumer = KafkaConsumer(topic=kafka_topic,group_id=kafka_group_id)
        self.db_manager = DatabaseManager(database_url=DATABASE_URL)
        self.cache = RedisCache()

    def processar_produto(self):
        try:
            for mensagem in self.kafka_consumer.consume():
                produto = json.loads(mensagem)
                key = produto['product_id']
                # checa se o produto esta no cache e se o valor de price_real é diferente do que esta no cache, se for diferente ou se não existir, armazena no cache
                if (
                    self.cache.check_cache(key)
                    and self.cache.get_cache(key)['price_real']
                    == produto['price_real']
                ):
                    print('Dados armazenados no cache.')
                    continue
                produto_bd = self.db_manager.get_product_by_id(produto['product_id'])
                if produto_bd:
                    # Comparar preços
                    if (
                        abs(
                            produto_bd.price_real
                            - float(produto['price_real'])
                        )
                        > 1
                    ):
                        print(
                            f"O preço do produto {produto['product_id']} foi alterado de {produto_bd.price_real} para {produto['price_real']}"
                        )
                        produto_bd.price_real = produto['price_real']
                        update_data = PriceHistoryUpdate(
                            product_id=produto['product_id'],  # Substitua 'product_id' pelo nome correto do campo
                            date=produto['datetime_collected'],
                            price=produto['price_real'],
                            price_real_symbol=produto['price_real_symbol'],
                            price_real=produto['price_real'],
                            price_us_symbol=produto['price_us_symbol'],
                            price_us=produto['price_us'],
                            discount_price_real=produto[
                                'discount_price_real'
                            ],
                            discount_price_us=produto['discount_price_us'],
                            discount_price_real_symbol=produto[
                                'discount_price_real_symbol'
                            ],
                            discount_price_us_symbol=produto[
                                'discount_price_us_symbol'
                            ],
                        )
                        self.db_manager.update_product_price(update_data)
                        mensagem = json.dumps(produto)
                        self.cache.set_cache('cached_data', mensagem)
                else:
                    try:                       
                        produto_create = ProductCreate(
                            product_id=produto['product_id'],
                            name=produto['name'],
                            sn=produto['sn'],
                            url=produto['url'],
                            imgs=produto['imgs'],
                            category=produto['category'],
                            store_code=produto['store_code'],
                            is_on_sale=produto['is_on_sale'],
                            price_real_symbol=produto['price_real_symbol'],
                            price_real=produto['price_real'],
                            price_us_symbol=produto['price_us_symbol'],
                            price_us=produto['price_us'],
                            discount_price_real_symbol=produto[
                                'discount_price_real_symbol'
                            ],
                            discount_price_real=produto['discount_price_real'],
                            discount_price_us_symbol=produto['discount_price_us_symbol'],
                            discount_price_us=produto['discount_price_us'],
                            datetime_collected=produto['datetime_collected'],
                        )

                        self.db_manager.create_product(produto_create)
                        print(f"O produto {produto['product_id']} foi adicionado")
                        mensagem = json.dumps(produto)
                        self.cache.set_cache(f"product_{produto['product_id']}", mensagem)
                    except Exception:
                        self.db_manager.session.rollback()
                        continue

        except KeyboardInterrupt:
            self.kafka_consumer.close()
