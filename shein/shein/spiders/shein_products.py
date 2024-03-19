from datetime import datetime

import scrapy

from shein.cache.redis_cache import RedisCache
from shein.items import ProductItem


class SheinProductsSpider(scrapy.Spider):
    name = 'shein'
    allowed_domains = ['m.shein.com']
    url_base = 'https://m.shein.com/br'
    headers = {
        'authority': 'm.shein.com/br',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'anti-in': '1_1.2.0_339c00_mHqKNQayozVzie1e1eOexOdmSDAKC4223xv-670_XXiiEOCtE2gRLe1ohNShayNi4XTZNIEYPrmVWa8Q48VMgZgMisxGcmvCLI9C5cez-cskyaBMvUNOyXDZNuGJDkZeQ7BrbQFvkvXO2eCtjcY99iv8ZlhDRoICwRUsIsrLueA4Zb7kqHav-6GKXz7UZLgzimYMx7y4I9xr7FiThkXFZbXhHRYheNbXEDRGQPtPtUZA-8ZFyYkq6VaXQCcxYAITtWX5TOczl_o3fO-CxnFR3zNKpUn7ASJrozFIU0kVH5mQtElI0LC6k0vxWnfyFzS15ii9kciRXK71WUTeMFnJV_rT3bfu97CcnzuVd47r6wWmKVaL4i33LS770LLGc-IVIqXlKJcsYqwwZOw1lacTSt7lHLQZ2yCfNRR54cXFRfu2NIh59yEPhWvQyUAoZPQ-ZbFt12ttWDg86QkDLh7Sbg',
        'armortoken': 'T1_2.3.1_8cNFAa4O_Bb73t87kkrbRKr-Dew2EdoSJUIqSApdnL0RwLrGkOu1wj0U-A7TX_fs3SOy-7dXaVTYbs9dVS7LfTXvkRO-kpG9IbqVHa-BYPPjymkWL52gLs_jiaSzzQsHZCYEzNw-ONHJ3gzJyWS5dBX4ByiwCsgzm5XoGV6ik_Im2ZtNiXx69ZwsQQkiPyju_1710356529020',
        # 'cookie': 'smidV2=202307181939240ecdf8b419d6708819c2d3b0d4073c09008ed54d6c28470c0; rskxRunCookie=0; rCookie=15p2kkck4h6f8vwmh9pbcolk8vnjwi; cto_bundle=gKB_qV9LMGdibU5DY3R0cTMxOXpsSURKU1pqN2o3TFVtTSUyRjhhRnNxRHNaeXhhOFNQQ0xOWGdPcHVXZEQ5SFdOblhPVzBkWHJBbHlrTVd1b0Fyb1ptJTJGS28zTlNLJTJGcEFjSE1lTXolMkZTNmNMQ0IlMkZpZ1BUd0dDM0RaNGh2TUtNeThQTyUyRkdvVTVEOVJEUFV5bSUyQlBxY2daRW80ZUFPQSUzRCUzRA; lastRskxRun=1695571958351; _ga_SC3MXK8VH1=GS1.1.1695571857.5.1.1695571958.59.0.0; _ga=GA1.1.999905272.1689719966; _uetvid=f303cf5025bb11eeb2545b2b230aa28f; inId=202401231418468d91e15b0f82a62f6775f5b12aac446200159b64f72afe710; cookieId=2ACE3BC0_C2C0_97D4_793A_5ABB5AFCD51E; armorUuid=2024020223362845c98645ab0957bc75f4d7fe23509ad8009859607a5ef40300; jump_to_mbr=1; g_state={"i_l":0}; country=BR; countryId=30; jump_to_mus=1; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+06+2024+18%3A12%3A42+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=b4c2f38a-8fb7-4d85-ad7e-946d8a5030e2&interactionCount=1&landingPath=https%3A%2F%2Fm.shein.com%2Fus%2F%3Fref%3Dm%26rep%3Ddir%26ret%3Dmus&groups=C0001%3A1%2CC0003%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1; RESOURCE_ADAPT_WEBP=1; forterToken=0ee57ac8168f4af5935d5f1fc370cce8_1710298134593_768_UAS9_17ck; sessionID_shein_m_pwa=s%3ATll1rLBO9BnvSWx_AT1m52Ws2w1zQmCI.XM%2BRkpm8wZwzNlac7pRP55t%2B4gV9jlAUoSB%2ByLiH%2FxM; _abck=5A1EDC683300FA60AE1F74FFA8A15391~0~YAAQZKQSAqzudDWOAQAA9YimOAtYd9/i9RuhF++IubyRZ4N9YDPylvJ9Wd+hbqlghIm/r8pe8u2WWRFuBBhKgTds7T/l4nxkZ6uPQDk7xHCCO+wLlhub6Ak4VA/epfhYNrCZcvDhaZdSOYoH1RDDR2xNgYP+dxlRxoRhRETbQA0x6hkff//AvWo1f0+iZhpNDE2DdOUl4q5M0WprF4BQkVKI+iUQMEpL8ocLVzjIRWEv6yd4mR4bVp4DcldYCTqUr2ejzRgRc2WBRkJbFPVbbUTzK8iC9wbSZTMWxnnDOpVC+BQmJy1Odfu+DQmGk2HVwCMlQwnKSCg2vw9uvmZNoIg+g7quttI0wF13leaDy8O/KJqgN5YxfBOtv7RjHTr6ir6HOnwtVMM3Etia/E0PTyLlCUoO+cg=~-1~-1~-1; bm_sz=FC6F83E8933BE34480DD17BB6425779C~YAAQZKQSAq/udDWOAQAA9YimOBeJswED3+eiGEvNau4Oj7s+HnIvuoGUrcCCigC/HvWVQEgDKbpkidp3IR2SDLMeI6NtgLrN0XilywoDIJrIwtw6zAMo2Q6TqsIU48/JMCr2Ja254vwRpMg0mKsMMLM7FKWo5SOjRR/zL9bzNvmY/i3qhz3eL/0XAh5Z3vv6kmIgOb4HlGcYdP9o0+KQXXgPwTitMfnW/W0FrXL5JvvJD0rqa/kzHk9aBWIThINwdLtmspRZdV8/UkWKqeeXlAA0TUJdqoJ4O6OZfm4+R+ea5B1buuKkf4le8EEUK0R53OrQyhQPBCD04vgkNkSVnIBlJQl5uo2qBni4xjlGgXTUBj+XL3Q=~3290424~4536372; _fmdata=WktSk2tFwCrOgVLtn61lym8I7TuPP9AQYu41uuiROGkIVc%2FWc%2B5uEaRNzRa%2FdacRLmHP4EbCj1i0nbBKTP92%2Bw%3D%3D; c=yqz2Sexx-1689719964407-867c2f0df4f8f647663969; E0701BBE33D9FD0A=yqz2Sexx-1689719964407-867c2f0df4f8f647663969; _f_c_llbs_=K1901_1710356150_KvSG_kZBZXn3GdrqcbvytLCHXkvasymOpD789m4XT4c8iKT7rv1yr-oLVPrFdhdzS9lkruq-kxu256BEcDVOePaAPr1bIbyp8Gl0S4tEsLE5Y-McEDky5QC8eTCzDNUaYFZslE-qfumQmNCsfZp8b287jwztvjm-uIO7bCh5Zfi2dDxjY5Q6rI6Ft5g98ycpj-CBOyKzWRvnrSEGgsp71ngZLd8t-PWkozXSLFBkL4YdkbUamY6Qkxp4mcaEn15L7PhjMkxC3D5wEFi8EDfd156N345KaOivOqp4VVLB_f6JjEWe10RdN9gp0pnIDbOca1JnoIAQOEuH5c-pAEkT_A; bm_mi=79DA211F4BDBA00D36DD2791834735B6~YAAQWmdCF8OvCy6OAQAA/uMrORf3Mt3ykzojSIwGG2SVQzKDtEjIO4px38FavnH5RBEmIA1GwLW+ClMyNqWt3oX9stPawJ+nR7cPf0KPtHz++otlhIdNgNDhmvFLsGq7Wl+s6E0G6ygoCC7bMQd5O1RGeMhZRERw6UrwKvrVtMqV+vX5vCoJakJ0z4/c4acpQj6AK5N64wVHBc6SGw70fhuQKJ7DppOWDzta4+tocCTHIbdDcftN+fMvDcj+nX6Aq7bCP3mbNRrT33Y56ZoSfJQLTlXljgK7+L4MfJ5r+LC55eeVwsuup8EuxabsWsfc2cZFEBuQ66f2q8doGHJUJ+6lZwSvL5m+4II=~1; bm_sv=D3236563186AFC9239C9EB3F7A68E518~YAAQWmdCF3WzCy6OAQAAgPErORfFIR4aXz27DR1NsXRKS6X0tTEDdI2bzp4XmEDYJ6Y63URkGaljVk4d6HPcgZsPxq+C13LXkpyhiyDOtL4RJyykN9D0U9wUCWlUvT6Fv2wooCTyc1yNV58FFm+U+BkNLLxsjZCv0nZI3dLze9cvzYoquLDsb6QkKn7wVfdUPc6ohlO4oEdcriS5pvji3xl4R+FUl1ydar0q/8VMekClwMdRM4X3Su/idNcZnUS1~1; ak_bmsc=441EEBC4E4EBBC9DD08736F1DF475F09~000000000000000000000000000000~YAAQWmdCF4VFDC6OAQAAR5MtOReMgubjE66svndPLIUk9JFp7Z7MYyKCOSTMBfNXzkFuQJ2fTRSXDIZ+2Eo5kx8Yfdr35JA374OT6YnvCW2yOyQtzv0ZRYVPl9ubeg5r/t15M82TFLe48PgooEDiuI6AMBZ0muZTQVpdmZCkrrd80epfi6Rx+ACttis5kWL7J3YmNyr1jVFme5xDwVeAmG3GYoDWJBs4Hv5g57wnkP2KVfMl0wLy11F2sLK6KehNlJpy6DRNAgGzqIFD9AQ9Zp6r3ZeOT8CgC1V5I2qPrwUOHqFWA/PSs/79XZWuUJM9n2wT6pMrsmycjOmJfwi2TEdeBrWsTa8xhqRshwwifbi3vosJPH2+3XlUld4gVF9i1ZLeORs/KJRjNSeC4odNpX81sRUBYl9KFSjj4DU7CLlIQc3zt91iJwKKX2n0VTWWES/+v37oA8CY8iESyAuttz1Mf4vU; pwa_countryId=226; app_country=US; branchmbrbr=%5Em.shein.com%5C%2Fbr%5C%2F_-c-_-vc-_-sc-_-cat-_-p-_%5C%2Fcampaign%5C%2F_flash-sale; cf_clearance=v1CzqSUmj27lKCHtXsoJdWS8b0.pO2Wm8VM6AHyC7mo-1710356530-1.0.1.1-b2ONJ.gCuTLsyyLyey38GtP3F15j.rMUmGvjHpuqprEEMvtCSnQCtBC10w4vkVO3Gidf9clen28Lwxk3z41Rvg; 62BB9B5EB31B00B0=WktSk2tFwCrOgVLtn61lym8I7TuPP9AQYu41uuiROGny6tvRG6ZS%2BfiNzVPPuy3H8mrpWhqePaQGkdWQJ%2F%2BLtg%3D%3D; _xid=YkhkMIQ7I5j%2F0JZ3pBExARxImQPzVh6%2FNn5EvmRgIYE%3D; __cf_bm=bOQuawRStAfctBEKJwKV2741HvlNVP4JpGW9EiZ2RG8-1710356533-1.0.1.1-LcS695I5czwgRhOjhIUpUG1UsvXB5dtv4wa_c0o5GuLr8sTDzOzO2WP_V7xGKfs1V_0vbvmyyKQDlmMzucKVKw; _cfuvid=nXpnC6Nfd221ahHtVvw9JGq_ItwXR0RBq39nhBAosWE-1710356533139-0.0.1.1-604800000',
        'local-time': '2024/3/13 16:2:18',
        'referer': 'https://m.shein.com/br',
        'screen-pixel': '686X554',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'smdeviceid': 'WHJMrwNw1k/GFp00r0LK9MaXfA3Wu9hrPWoJChLwNPqtE61wWGPusEvDKN0jdt4S3YzYPstCxXaXa2ONaJeHhzMSwLvA22uX8vTLYedm0UEk1+djV4N+GQM5g8LyURrS6TZOJg5hGkZYfhwDCeHJsqFqRPoL7FhKirjl+d2XxfVgeHFtPfuX8iNCpI3Tsb+2fTF5iRjvOBBLCNZetNNUFPuzuIEFgtRSwVQ/FNY66kYxsMiwK8usc45fglP7Dmafde5685hmEETs=1487582755342',
        'timezone': 'GMT-3',
        'uber-trace-id': 'ff28ddf5ba69c031:ff28ddf5ba69c031:0:0',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        'x-csrf-token': 'f1xJUxht-3oehszRN43UR_GmxGt2Jj3ZKTIM',
        'x-gw-auth': 'a=xjqHR52UWJdjKJ0x6QrCsus66rNXR9@2.0.13&b=1710356538287&d=e7c5c76d23685b673b769b0b7672b4be&e=nn5lWZWZlMTNkM2U0NTI0NDJiZTBmNDk3NjUwYWQ2MDk2ZGIzNTEyYTk2ZDIwNGFkYjMzZTA1ODE1ZjZhYTY1YjE3MQ%3D%3D',
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
                try:
                    if not product.get('retailPrice'):
                        continue
                    item = ProductItem(
                        product_id=product['goods_id'],
                        name=product['goods_name'],
                        sn=product['goods_sn'],
                        url=f"{self.url_base}/pdsearch/{product['goods_sn']}/",
                        imgs=','.join(product['detail_image']),
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
                except Exception as e:
                    self.logger.error(
                        f'Erro ao processar o item: {str(e)}'
                    )
                yield item
            self.redis_cache.set_cache(self.categorys[0], '1')
        else:
            self.logger.info(
                f'Nenhum produto encontrado para a URL: {response.url}'
            )
