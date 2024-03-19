import json
import logging

import requests
from confluent_kafka import Producer

from config import KAFKA_SERVERS,KAFKA_TOPIC_url


class SheinCategoryProducer:
    def __init__(self, kafka_bootstrap_servers):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.headers = {
            'authority': 'm.shein.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'anti-in': '1_1.2.0_7e03ab_Wtj0c-U631D4azLNADhWeiFBFHKNKsYf4jE-WgestetvLQ7LunX6iUXUmqfSwAfyMpJXnE78DEtNDNVjXFGVpOmubwt6vEUvia0Fvd0HhRYOStY2yK6okvvMZV5NKQ7GnKJlwYVxXugI1i-v4qIA-cf23Y1hgqbRIThh5_MVDkQbSdweh4PHtFe2ovinbOV7OaONCSJnI2UL4vxrJPb2sbwvNagrVD_w5uU0ocwVKLBT7jK6agciVSlTdR_d-dMPCG7tjfsJdcefJ91PvNTHP0Fn3yV2WjeJYrZkTBMAt85e6ibHVhRIBmVy-4hmq8RSTiiurAdkFweThrfQyx74LT6PbUsvbjSSgk1hYWIUXtawVBEMvLEk2FcJZcYISlW4gjVm8q7I1irdC-8ZG1sFEteypqKetRiD_CE2GnkWq1Lpof4tj0lWlrxka1v0a6RtQM0kVZfeDK0LS4G8RmujACLH1l4awEhHnifMWWueyej7cdBtAcHCf-nNqFfPArMxD62xr7ez8Aq6gzW3cmI55sZrYOtBDohLZa4xFeQqoKsbz_y2AJyGrWjmyKdzQPUEkpZI8StDbbMvwLMh2Ef8wkOlqlIhCs1bdO-umtmVxV7KLbDfw6KxvDS74Wbe4-soj_ui98A1XUavG2A7UB2eFAZMAD9rmFr9CPswXmW7PwlaOPr28JnVuMwhX4n6yGFW_oDUg28-6jE_GEJ1ni--Z_ijXGMdHkb2Q82d4K0hPSNO128IEnPK5xmYueOoMpINHtjGgO5f0cy323-pg3Fw47pjLTiVus_A_52xPPHuqCr87GmiXGsZ67SuzAo0f3_oUBQmT0uVPvsj1k1v2PkTgbo3CIlqcLpKyvs6wF77_PFtLdEK_CKt_icuFspazynNYNfbvYiVLh5vFmcgx1vxEJSuBv8WUCKhbPQ11LnXYqASNXE-NpE7myTHpSpifamh7gkehq8bVtrytUM0_AuLmQeBuZ9RJdueNVQ9ZnM58QM',
            'armortoken': 'T1_2.3.1_8cNFAa4O_Bb73t87kkrbRKr-Dew2EdoSJUIqSApdnL0RwLrGkOu1wj0U-A7TX_fs3SOy-7dXaVTYbs9dVS7LfTXvkRO-kpG9IbqVHa-BYPNHXzuWXz46gUEhvJlIBqETOmQ2hYchWyRkF2EH7P1NpzI3qFnFvevfNv8bdnZaIObZOJmTJRHTRb4MX1NUzHXwi-4TW87_2ww9xb6Xn4vZmQ==',
            'local-time': '2024/3/6 10:17:21',
            'referer': 'https://m.shein.com',
            'screen-pixel': '969X554',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'smdeviceid': 'WHJMrwNw1k/GFp00r0LK9MaXfA3Wu9hrPWoJChLwNPqtE61wWGPusEvDKN0jdt4S3YzYPstCxXaXa2ONaJeHhzMSwLvA22uX8xTvD0et+g8NgM8/2KBWqKoYHqxuZPWulBJ7HANruhDjgssVEtOEyiJGebD4P9188sXxdxwOY7EbE9m9dmO48serqwSineJLDFagLVrcV2PO/WnoRbU0buf6PWJPTBr2R2eXJR0XVZt5H+31Zb+MisAUDic6AW2yIixSMW2OQhYo=1487582755342',
            'timezone': 'GMT-3',
            'uber-trace-id': 'ff39819f84ad7ec8:ff39819f84ad7ec8:0:0',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
            'x-csrf-token': 'N0UX17PQ-qEDqaMLklVgrLAHW3Fy05Ylmlg0',
            'x-gw-auth': 'a=xjqHR52UWJdjKJ0x6QrCsus66rNXR9@2.0.13&b=1709731041660&d=e7c5c76d23685b673b769b0b7672b4be&e=QIz9rMTdkNjI4ZGJlYWUwZTViNzE4NDhhNjAxY2NhZjc3N2U5YTJlZDc2NTljNDIxMzdlNGZkMDVkMmNiY2JkMTA3NQ%3D%3D',
            'x-requested-with': 'XMLHttpRequest',
        }

    def get_categories(self):
        categories = []
        NUM_CATEGORY = 1864
        URL_API_CATEGORY = f'https://m.shein.com/br/api/category/channel/get?_ver=1.1.8&_lang=pt-br&channelId=10&cateType=sidecat&oneCate={NUM_CATEGORY}'
        response = requests.get(url=URL_API_CATEGORY, headers=self.headers)
        json_response = json.loads(response.text)
        cate_links = json_response['data'][0]['cateLinks']
        for url in json_response['data'][0]['cateLinks']:
            categories.append(cate_links[url])
        return categories

    def produce_to_kafka(self, topic, categories):
        conf = {'bootstrap.servers': self.kafka_bootstrap_servers}
        producer = Producer(**conf)

        for category_url in categories:
            info_url = json.dumps({'category_url': category_url}).encode(
                'utf-8'
            )
            producer.produce(
                topic, value=info_url, callback=self.delivery_report
            )

        producer.flush()

    def delivery_report(self, err, msg):
        if err is not None:
            logging.error(f'Erro ao entregar a mensagem: {err}')
        else:
            logging.info(f'Mensagem entregue: {msg.value()}')


# Exemplo de uso
if __name__ == '__main__':

    category_producer = SheinCategoryProducer(KAFKA_SERVERS)
    categories = category_producer.get_categories()
    category_producer.produce_to_kafka(KAFKA_TOPIC_url, categories)
