import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return dict(config["database"])


database_config = get_config()

DATABASE_URL = database_config["database_url"]
REDIS_URL = database_config["redis_url"]
REDIS_EXPIRE_TIME = int(database_config["redis_expire_time"])
KAFKA_SERVERS = database_config["kafka_servers"]
KAFKA_TOPIC_OUT = database_config["kafka_topic_out"]
