from datetime import datetime

import scrapy
import json

from shein.cache.redis_cache import RedisCache
from shein.items import ProductItem


class SheinProductsSpider(scrapy.Spider):
    name = 'shein'
    allowed_domains = ['m.shein.com']
    url_base = 'https://m.shein.com/br'
    headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'anti-in': '1_1.2.0_d9023c_jX-yX89ZqGWsAFlAtSg5cylcUS0MZ-dCUnIwBOg2Gu1onfwxX6fsBskqx0FbQxChqDgcpAioSGD6Ol6jQEKAMoVUZQ1uOCRNbYftRg4wLKdowdrmUYvHGASXkCfAIgutJdS32nx34sUVyy30Wm9rXFGa0jyA52ENLX9OEXKJnD8bSZJ0t2zCdn_7kIN-3feh0hzRTHiJoTnq1h3-vZrRTVMy_oJ9ryqPU37kxk_EBsFgReBaSjW6CFcHjkxXtc19GBYHYDz9KZznJTkbaeLoL-XTynX909xIGYRiQL-aNUGNqLXBDQQckstcmhyXO2ARs7_cDmtu1eWocrA1uey45mIBkqYJ1Z__mTepCBG8mmehC9SvZf22vXCv9-XUvoDcsviljQc8vvMhiDF9Du4miO3MeQ5pR1A7Lei-JtrevGbSL9KEt61mBbFfRPPwo1vCC1CwOLFe_5oWzLqciZxLqgX9R6GSacHDH1iPG07LHp-lMvQ3J6yBC1VyEqL3-EqYGMMdiGGF9QAemW4UdRnJM1GinYQz3uFAu-1xTufMh20',
    'armortoken': 'T1_2.3.2_OPpk1HXXcuQjRiE-cGLsgAiKc_cEWOKLAAiSNeSaa2yAZjrthcMfrEON1aXfJLSWCP1qSlncqx67C51hEZRcbMT8CRFgHeumxs0DvuFhR_NTpl1zpUJdLIGcqIU4rM80eqXAp0kgRXl2Q0VC8f7JUCTgK6Qfxwua9oaqN7E_Gx1zHLXkbY4xQgjXPumZ0eqj_1711981003367',
    # 'cookie': 'smidV2=202307181939240ecdf8b419d6708819c2d3b0d4073c09008ed54d6c28470c0; rskxRunCookie=0; rCookie=15p2kkck4h6f8vwmh9pbcolk8vnjwi; cto_bundle=gKB_qV9LMGdibU5DY3R0cTMxOXpsSURKU1pqN2o3TFVtTSUyRjhhRnNxRHNaeXhhOFNQQ0xOWGdPcHVXZEQ5SFdOblhPVzBkWHJBbHlrTVd1b0Fyb1ptJTJGS28zTlNLJTJGcEFjSE1lTXolMkZTNmNMQ0IlMkZpZ1BUd0dDM0RaNGh2TUtNeThQTyUyRkdvVTVEOVJEUFV5bSUyQlBxY2daRW80ZUFPQSUzRCUzRA; lastRskxRun=1695571958351; _ga_SC3MXK8VH1=GS1.1.1695571857.5.1.1695571958.59.0.0; _ga=GA1.1.999905272.1689719966; _uetvid=f303cf5025bb11eeb2545b2b230aa28f; inId=202401231418468d91e15b0f82a62f6775f5b12aac446200159b64f72afe710; cookieId=2ACE3BC0_C2C0_97D4_793A_5ABB5AFCD51E; armorUuid=2024020223362845c98645ab0957bc75f4d7fe23509ad8009859607a5ef40300; jump_to_mbr=1; jump_to_mus=1; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+06+2024+18%3A12%3A42+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=b4c2f38a-8fb7-4d85-ad7e-946d8a5030e2&interactionCount=1&landingPath=https%3A%2F%2Fm.shein.com%2Fus%2F%3Fref%3Dm%26rep%3Ddir%26ret%3Dmus&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1; _fmdata=WktSk2tFwCrOgVLtn61lym8I7TuPP9AQYu41uuiROGkIVc%2FWc%2B5uEaRNzRa%2FdacRLmHP4EbCj1i0nbBKTP92%2Bw%3D%3D; c=yqz2Sexx-1689719964407-867c2f0df4f8f647663969; E0701BBE33D9FD0A=yqz2Sexx-1689719964407-867c2f0df4f8f647663969; _abck=5A1EDC683300FA60AE1F74FFA8A15391~0~YAAQkGdCF8vUFDiOAQAAS0XhPAv8H08pc980s390weldDqdm5f/Qah3/8VjEJ6CbCcyKJdOx4WZwhGfKj/0ft/Uta8NtYyxiLcfdPvqQGrLXOxc69WGZpUnTH1XhhM5X6RkYqttXYLm6cj5fX4MctUtLwYBE2EJVe0Pr0s0Nk2/K2Nj6vBZah4xo/udenIZa5BLe+9DKoC8ef89RXFd8h1g9nVaT42VNn3tNRpggxZO+03SKQFuOVGyiIIEEESxXkD4K/nQAHdwD9RopF5LbFOkn3znYfESBY6rARL0adirOyVUJdek2DfahAmsNoD5l0RI6Tn/zLLsW7LZqP44kpdzzT5xLMpZzH1FlQXEQsmRZVBlizBoEDZ8ehf8R4cBfuI0mcqQBNe4LQLhYA7TNOiupGqFBL2Q=~-1~-1~-1; RESOURCE_ADAPT_WEBP=1; country=BR; countryId=30; forterToken=0ee57ac8168f4af5935d5f1fc370cce8_1711975686089_19_UDF9_17ck; location_ban=BR; _xid=2zKtjKYofTPkXflB5W9m8obuGZ0haGdoquJ0el6kEJ0%3D; g_state={"i_l":1,"i_p":1711986199886}; 62BB9B5EB31B00B0=WktSk2tFwCrOgVLtn61lym8I7TuPP9AQYu41uuiROGmlZrtPIXUB2jFrSUNY2KulohzUytf7qc5N0%2FYUo0yi1Q%3D%3D; _f_c_llbs_=K1901_1711979081_eog_QHZ33rhepT8aRnHz2b-zOfeXdL11dcfckebTZRXRRbmgW-g_lSuBcfey_UxR0Ja4irVygkwJfj-ua0kCtYKkwjQsSSujwwutgMMJAR__DQo-n_sCrKg-LFCQwY84tge206nqg13aWGEIJeKcc7IPky7q22cNWKSo8sxPWXSM9gJgHAHnAqqHO03k1y7AZeVaJL7osDSNFppSrDFKJ64-S7lqsQ1fuqAgUso5-w0nSmY3L6tALVmhC1HUeYOX3PTCdnjgdGK3M_V4q7u1mnITSrDPiorlRq7B2Sr7-iSiaQWQ-lt3kTAngS3gDxF_zZxlUN3mARqPh1Pi38jhiw; pwa_countryId=226; app_country=US; sessionID_shein_m_pwa=s%3AmISwmA0rt4HcQVvCd2BnQ3mKVSd-ZnnJ.0g3z%2FwPt4WDizYCO7obUkH%2FctL67tJv%2B6O6%2BKBfko7E; cf_clearance=.RvUY3AgTNMiAWvy9LrWzgG7SX6Y4HUlvkrsuMAGEyQ-1711981100-1.0.1.1-B1y6eB6LjzmRk64DVljhT2kZeXeP1rtTqrVjHuBaErHj2uC6iCpvYlDHEiBhclp6F24RAQ.WCRfvcbGuXHlBgQ; __cf_bm=hwetBxvNFVkAkLRlF_EsVhuF5pnvZuVOctj_LY0PkRc-1711981512-1.0.1.1-kzgXpQskhcfZ3AWEHV0pmRivpWYJsBQjQtZV1U4TQYdbcnTA6uFnKbgbvPAMpzKFA7jpaFdj6ZPOMStSKYy5pg; _cfuvid=Zj6SH.sajiJlspe7ZbivwZ48jjBwM7o_60g8w.oWfwY-1711981512473-0.0.1.1-604800000; branchmbrbr=-indexHome-',
    'local-time': '2024/4/1 11:25:27',
    'referer': 'https://m.shein.com/br/',
    'screen-pixel': '686X540',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'smdeviceid': 'WHJMrwNw1k/GFp00r0LK9MaXfA3Wu9hrPWoJChLwNPqtE61wWGPusEvDKN0jdt4S3YzYPstCxXaXa2ONaJeHhzMSwLvA22uX8dCW1tldyDzmQI99+chXEilH1Hai/njq89lCUKKcsmkSqmJzoPeggwzYmmmXo8LlTkQE5YcNLqNriNYPfoOP/brSGTwDEQqy3FRRuSg/X1FURTkAd7H/eWpPfHpU6Y9P34nlXr6I24OILNJHmmY07b9rnv6GpOE7t1487582755342',
    'timezone': 'GMT-3',
    'uber-trace-id': 'ffe7eacecf1e3a74:ffe7eacecf1e3a74:0:0',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'x-csrf-token': 'XwYBfImz-g4JNKVXF5tdWrlsX7-zTOynlg10',
    'x-gw-auth': 'a=xjqHR52UWJdjKJ0x6QrCsus66rNXR9@2.0.13&b=1711981527344&d=e7c5c76d23685b673b769b0b7672b4be&e=JovOeNWZjOWFkMmMyZWIwZjY2Mjk5YTBhZjBhMzc4OGE5ZDgxMzY5NGU1NGFjODM2ZjA5YmY2NGM2NzhjMzI1NzEwOQ%3D%3D',
    'x-requested-with': 'XMLHttpRequest',
}

    categorys = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'shein.pipelines.KafkaPipeline': 100,  # Prioridade 100
        },
        'RETRY': True,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 7,
        'RETRY_DELAY': 7,
        'RETRY_HTTP_CODES': [404, 403],
    }

    def __init__(self, url_categoria=False, *args, **kwargs):
        super(SheinProductsSpider, self).__init__(*args, **kwargs)
        self.categorys = [url_categoria]
        self.redis_cache = RedisCache()  # Inicialize aqui

    def start_requests(self):
        if self.categorys[0]:
            for category in self.categorys:
                url_category = self.url_base + category
                # Verifica se a URL já está no cache
                if not self.redis_cache.check_cache(url_category):
                    yield scrapy.Request(
                        url=url_category,
                        callback=self.parse,
                        headers=self.headers,
                    )
                else:
                    self.logger.info(
                        f'A URL {url_category} já está no cache. Pulando...'
                    )
        else:
            self.logger.info('A URL não foi passada.')

    def parse(self, response):
        id_category = response.url.split('-')[-1].split('.')[0]
        limit = 99999
        URL = f'https://m.shein.com/br/api/productList/info/get?_ver=1.1.8&_lang=pt-br&type=selection&routeId={id_category}&page=1&limit={limit}&requestType=nextpage&viewed_goods=29089719-m23112047417,28482793-m23120882174,26549386-m23101001415,26437234-m23101733288,26649930-m23101739193,24566412-m23091959966,28489354-m23120819665,26254358-m23101722611,28246422-m23112078282,28377187-m23111571742,28742852-m23120858731,25872615-m23101007970,28795726-m23112172969,25954515-m23101094419,27308969-m23110849011,28843441-m23110945445,29813504-m23120815795,29314211-m23112289889,28815821-m23112213153,28158796-m23112067267&asyncPromotionIds=2,14,15,24,28&reqSheinClub=true&deliverItemLimitObject=%7B%7D'
        yield scrapy.Request(
            URL, callback=self.parse_all_products, headers=self.headers
        )

    def parse_all_products(self, response):
        if self.redis_cache.check_cache(response.url):
            self.logger.info(
                f'Dados já presentes no cache para a URL: {response.url}'
            )
            return

        products = response.json()['goods']
        if products:
            for product in products:
                if self.check_product_in_cache_and_if_price_updated(product):
                    self.logger.info(
                        f'Produto with name : {product["goods_name"]} e ID: {product["goods_id"]} atualizado. Pulando...'
                    )
                    continue
                try:
                    item = ProductItem(
                            product_id=product['goods_id'],
                            name=product['goods_name'],
                            sn=product['goods_sn'],
                            url=f"{self.url_base}/pdsearch/{product['goods_sn']}/",
                            imgs=product['detail_image'],
                            category=product['goods_url_name'],
                            store_code=product['store_code'],
                            is_on_sale=product['is_on_sale'],
                            price_real_symbol=product['retailPrice'][
                                'amountWithSymbol'
                            ],
                            price_real=product['retailPrice']['amount'],
                            price_us_symbol=product['retailPrice'][
                                'usdAmountWithSymbol'
                            ],
                            price_us=product['retailPrice']['usdAmount'],
                            discount_price_real_symbol=product['salePrice'][
                                'amountWithSymbol'
                            ],
                            discount_price_real=product['salePrice']['amount'],
                            discount_price_us_symbol=product['salePrice'][
                                'usdAmountWithSymbol'
                            ],
                            discount_price_us=product['salePrice']['usdAmount'],
                            datetime_collected=datetime.now().strftime(
                                '%Y-%m-%d %H:%M:%S'
                            ),
                        )
                    item_json = json.dumps(dict(item))
                    self.redis_cache.set_cache(f"product_{item.product_id}", item_json)
                    yield item
                    
                except Exception as e:
                    self.logger.error(f'Erro ao processar o item: {str(e)}')

            self.redis_cache.set_cache(self.categorys[0], '1')
        else:
            self.logger.info(
                f'Nenhum produto encontrado para a URL: {response.url}'
            )
    
    def check_product_in_cache_and_if_price_updated(self, product):
        """
        Verifica se o preço do produto está no cache e se o preço estar atualizado.
        """
        key = f"product_{product['goods_id']}"
        if self.redis_cache.check_cache(key):
            cached_product = self.redis_cache.get_cache(key)
            if product['retailPrice']['amount'] == cached_product['price_real']:
                return True
            else:
                return False
        else:
            return False
        
    
