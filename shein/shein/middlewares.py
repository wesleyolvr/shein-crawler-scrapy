# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import redis
from scrapy import signals
import base64
from scrapy.exceptions import NotConfigured

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy.http import Request

# class RedisCacheMiddleware:
#     def __init__(self, redis_url, expire_time):
#         self.redis_url = redis_url
#         self.expire_time = expire_time

#     @classmethod
#     def from_crawler(cls, crawler):
#         redis_url = crawler.settings.get('REDIS_URL')
#         expire_time = crawler.settings.getint('REDIS_CACHE_EXPIRE_TIME', 4 * 24 * 60 * 60)  # 4 dias em segundos
#         if not redis_url:
#             raise NotConfigured("REDIS_URL not configured")
#         return cls(redis_url, expire_time)

#     def open_spider(self, spider):
#         self.redis_client = redis.from_url(self.redis_url)

#     def close_spider(self, spider):
#         self.redis_client.close()

#     def process_request(self, request, spider):
#         # Verifica se a URL já está no cache
#         if self.redis_client.exists(request.url):
#             # Se estiver no cache, retorna None para indicar que a requisição deve ser ignorada
#             return None
#         # Se a URL não estiver no cache, permite que a requisição prossiga
#         return request

#     def process_response(self, request, response, spider):
#         # Verifica se a resposta contém dados de produtos
#         if response.json().get('goods', None):
#             # Se sim, armazena a URL no cache com o tempo de expiração configurado
#             self.redis_client.setex(request.url, self.expire_time, 1)
#         return response


class SheinSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SheinDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxyMiddleware:
    def __init__(self, proxy_settings):
        self.proxy_settings = proxy_settings

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("PROXY_ENABLED"):
            raise NotConfigured
        proxy_settings = {
            "endpoint": crawler.settings.get("PROXY_IP"),
            "port": crawler.settings.get("PROXY_PORT"),
        }
        return cls(proxy_settings)

    def process_request(self, request, spider):
        host = "http://{endpoint}:{port}".format(
            endpoint=self.proxy_settings["endpoint"], port=self.proxy_settings["port"]
        )
        request.meta["proxy"] = host
