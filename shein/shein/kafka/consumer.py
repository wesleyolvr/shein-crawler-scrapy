import json
import logging

from confluent_kafka import Consumer

from config import KAFKA_SERVERS


class KafkaConsumer:
    def __init__(
        self, topic, servers=KAFKA_SERVERS):
        self.consumer = Consumer(
            {
                'bootstrap.servers': servers,
                'group.id': 'my_consumer_group',
                'auto.offset.reset': 'earliest',
            }
        )
        self.topic = topic
        self.consumer.subscribe([self.topic])

    def consume(self):
        while True:
            msg = self.consumer.poll(5.0)
            if msg is None:
                logging.info('Aguardando mensagens...')
                continue
            msg_text = msg.value().decode('utf-8')
            if 'Application maximum poll interval' in msg_text:
                logging.error('Application maximum poll interval reached')
                break
            logging.info(f'Mensagem recebida: {msg_text}')
            msg_json = json.loads(msg_text)
            return [msg_json]

    def close(self):
        self.consumer.close()
