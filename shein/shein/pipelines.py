import json
import sqlite3

from confluent_kafka import Producer
from scrapy import signals
from scrapy.exceptions import DropItem
from logging import logger
from config import KAFKA_SERVERS, KAFKA_TOPIC_products


class KafkaPipeline:
    def __init__(self, kafka_servers, kafka_topic):
        self.producer = Producer(
            {
                'bootstrap.servers': kafka_servers,
                'client.id': 'python-producer',
            }
        )
        self.topic = kafka_topic

    @classmethod
    def from_crawler(cls, crawler):
        if not KAFKA_SERVERS or not KAFKA_TOPIC_products:
            raise ValueError('KAFKA_SERVERS or KAFKA_TOPIC is not set')
        pipeline = cls(KAFKA_SERVERS, KAFKA_TOPIC_products)
        crawler.signals.connect(
            pipeline.spider_closed, signal=signals.spider_closed
        )
        return pipeline

    def process_item(self, item, spider):
        item_dict = dict(item)
        message = json.dumps(item_dict).encode('utf-8')
        try:
            self.producer.produce(KAFKA_TOPIC_products, message)
            self.producer.flush()
            logger.info(
                f"Item enviado com sucesso para o tópico '{self.topic}': '{message}'."
            )
        except Exception as e:
            raise DropItem(f'Failed to send item to Kafka: {str(e)}')
        return item

    def spider_closed(self, spider, reason):
        pass


class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        self.setup_database()

    def close_spider(self, spider):
        self.conn.close()

    def setup_database(self):
        # Criar a tabela se ela não existir
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                sn TEXT UNIQUE,
                url TEXT,
                imgs TEXT,
                category TEXT,
                store_code TEXT,
                is_on_sale INTEGER,
                price_real_symbol TEXT,
                price_real REAL,
                price_us_symbol TEXT,
                price_us REAL,
                discount_price_real_symbol TEXT,
                discount_price_real REAL,
                discount_price_us_symbol TEXT,
                discount_price_us REAL,
                datetime_collected TEXT
            )
        """
        )

        # Commit para salvar as alterações
        self.conn.commit()

    def process_item(self, item, spider):
        # Verificar se o produto já existe no banco de dados pelo ID
        self.cursor.execute('SELECT 1 FROM products WHERE id=?', (item['id'],))
        existing_product = self.cursor.fetchone()
        if existing_product:
            # Se o produto já existir, não faz nada
            return item

        # Converter a lista de imagens para uma string JSON
        imgs_str = json.dumps(item['imgs'])

        # Inserir o item no banco de dados
        self.cursor.execute(
            """
            INSERT INTO products (id, name, sn, url, imgs, category, store_code, is_on_sale, 
                                  price_real_symbol, price_real, price_us_symbol, price_us, 
                                  discount_price_real_symbol, discount_price_real, 
                                  discount_price_us_symbol, discount_price_us, datetime_collected)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                item['id'],
                item['name'],
                item['sn'],
                item['url'],
                imgs_str,
                item['category'],
                item['store_code'],
                item['is_on_sale'],
                item['price_real_symbol'],
                item['price_real'],
                item['price_us_symbol'],
                item['price_us'],
                item['discount_price_real_symbol'],
                item['discount_price_real'],
                item['discount_price_us_symbol'],
                item['discount_price_us'],
                item['datetime_collected'],
            ),
        )
        self.conn.commit()
        return item
