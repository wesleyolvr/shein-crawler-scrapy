# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class ProductItem(Item):
    product_id = Field()
    name = Field()
    sn = Field()
    url = Field()
    imgs = Field()
    category = Field()
    store_code = Field()
    is_on_sale = Field()
    price_real_symbol = Field()
    price_real = Field()
    price_us_symbol = Field()
    price_us = Field()
    discount_price_real_symbol = Field()
    discount_price_real = Field()
    discount_price_us_symbol = Field()
    discount_price_us = Field()
    datetime_collected = Field()
