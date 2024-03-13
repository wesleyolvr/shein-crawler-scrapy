import multiprocessing


def start_consumer():
    from api.database.manager import ProdutoProcessor

    processor_produtos = ProdutoProcessor('produtos')
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


def start_api():
    import uvicorn

    uvicorn.run('api.main:app', reload=True)


if __name__ == '__main__':
    # Definir o número de consumidores
    num_consumers = 4  # Por exemplo, iniciar 3 consumidores
    
    # Iniciar os consumidores em processos separados
    start_consumers(num_consumers)
    
    # Iniciar a API FastAPI
    start_api()