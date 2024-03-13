import multiprocessing
from config import KAFKA_TOPIC_IN

def start_consumer():
    from api.database.manager import ProdutoProcessor

    processor_produtos = ProdutoProcessor(kafka_topic=KAFKA_TOPIC_IN)
    processor_produtos.processar_produto()

def start_consumers(num_consumers):
    # Iniciar vários consumidores em processos separados
    processes = []
    for _ in range(num_consumers):
        process = multiprocessing.Process(target=start_consumer)
        process.start()
        processes.append(process)

    # Aguardar todos os processos terminarem
    for process in processes:
        process.join()


if __name__ == '__main__':
    # Definir o número de consumidores
    num_consumers = 2  # Por exemplo, iniciar 3 consumidores

    # Iniciar os consumidores em processos separados
    start_consumers(num_consumers=num_consumers)
