import logging
import multiprocessing

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from config import KAFKA_TOPIC_url
from shein.kafka.consumer import KafkaConsumer
from shein.spiders.shein_products import SheinProductsSpider


def run_spider_for_url(url):
    """
    Execute o spider fornecido para a URL fornecida.
    """
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(SheinProductsSpider, url_categoria=url)
    process.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    kafka_consumer = KafkaConsumer(topic=KAFKA_TOPIC_url)
    while True:
        try:
            for mensagem in kafka_consumer.consume():
                url = mensagem.get('category_url')
                urls = [url]

                # Crie um processo separado para cada URL e inicie o processo de rastreamento
                processes = []
                for url in urls:
                    process = multiprocessing.Process(
                        target=run_spider_for_url, args=(url,)
                    )
                    processes.append(process)
                    process.start()

                # Espere que todos os processos terminem
                try:
                    for process in processes:
                        process.join()
                except OSError as e:
                    logging.error(f'Erro ao iniciar o processo: {e}')

        except Exception as e:
            kafka_consumer.close()
            logging.error(f'Erro ao consumir a mensagem: {e}')
            break
