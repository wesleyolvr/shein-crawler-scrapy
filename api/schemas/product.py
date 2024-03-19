import json
from typing import List

from pydantic import BaseModel, validator


class ProductBase(BaseModel):
    product_id: int
    name: str
    sn: str
    url: str
    imgs: str
    category: str
    store_code: int = None
    is_on_sale: int
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discount_price_real_symbol: str
    discount_price_real: float
    discount_price_us_symbol: str
    discount_price_us: float
    datetime_collected: str


class ProductCreate(ProductBase):
    @validator('is_on_sale')
    # pylint: disable=no-self-argument
    def convert_is_on_sale(cls, value):
        """Converte para booleano."""
        if value in [1, '1', True, 'True', 'true']:
            return True
        elif value in [0, '0', False, 'False', 'false','']:
            return False
        else:
            raise ValueError("O campo is_on_sale deve ser um booleano ou representação válida.")

    @validator('store_code')
    # pylint: disable=no-self-argument
    def convert_to_integer(cls, value):
        """Converte para int."""
        if value is None or value == '':
            return 0
        return int(value)
    
    @validator('store_code')
    # pylint: disable=no-self-argument
    def convert_imgs_string(cls, value):
        """Converte para int."""
        if value is None or value == '':
            return ''
        return ','.join(value)


class ProductRead(ProductBase):
    datetime_collected: str

    class Config:
        orm_mode = True


class ProductUpdate(ProductBase):
    pass
