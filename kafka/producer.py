import json

from confluent_kafka import Producer

from logs.logger import logger


class KafkaProducer:
    def __init__(self):
        self.producer = Producer(
            {
                'bootstrap.servers': 'localhost:9093',
                'client.id': 'python-producer',
            }
        )

    def produce(self, topic, value):
        try:
            if isinstance(value, str):
                # Se o valor for uma string, codifica como utf-8
                value = value.encode('utf-8')
            if isinstance(value, dict):
                # Se o valor for um dicionário, serializa como JSON e codifica como utf-8
                value = json.dumps(value).encode('utf-8')
            self.producer.produce(topic, value)
            self.producer.flush()
            logger.info(
                f"Mensagem enviada com sucesso para o tópico '{topic}'."
            )
        except Exception as e:
            logger.error(f'Erro ao enviar mensagem para o Kafka: {e}')

    def close(self):
        self.producer.close()
