import multiprocessing

from api.database.manager import ProdutoProcessor
from config import KAFKA_TOPIC_IN


def start_consumer(kafka_topic):
    processor_produtos = ProdutoProcessor(kafka_topic=kafka_topic)
    processor_produtos.processar_produto()


def start_consumers(num_consumers, kafka_topic):
    # Iniciar vários consumidores em processos separados
    processes = []
    for _ in range(num_consumers):
        process = multiprocessing.Process(
            target=start_consumer, args=(kafka_topic,)
        )
        process.start()
        processes.append(process)

    # Aguardar todos os processos terminarem
    for process in processes:
        process.join()


if __name__ == '__main__':
    # Definir o número de consumidores
    num_consumers = 2  # Por exemplo, iniciar 3 consumidores

    # Iniciar os consumidores em processos separados
    start_consumers(num_consumers=num_consumers, kafka_topic=KAFKA_TOPIC_IN)
