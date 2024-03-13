from typing import Optional
import json
from pydantic import BaseModel, Field, validator
from typing import List


class ProductBase(BaseModel):
    id: int
    name: str
    sn: str
    url: str
    imgs: List[str]
    category: str
    store_code: int = None
    is_on_sale: int
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discountPrice_real_symbol: str
    discountPrice_price_real: float
    discountPrice_price_us_symbol: str
    discountPrice_us: float
    datetime_collected: str


class ProductCreate(ProductBase):
    
    @validator('imgs')
    # pylint: disable=no-self-argument
    def convert_to_json(cls, value):
        """Converte a lista de URLs de imagens para uma string JSON."""
        return json.dumps(value)

    @validator('store_code', 'is_on_sale', pre=True)
    # pylint: disable=no-self-argument
    def convert_to_integer(cls, value):
        """Converte para int."""
        if value is None or value == '':
            return 0
        return int(value)

    @validator(
        'price_real',
        'price_us',
        'discountPrice_price_real',
        'discountPrice_us',
        pre=True,
    )
    # pylint: disable=no-self-argument
    def check_comma_and_convert(cls, value):
        """Verifica se o valor tem vírgula e converte para float."""
        if ',' in str(value):
            return float(value.replace(',', '.'))
        return float(value)



class ProductRead(ProductBase):
    datetime_collected: str

    class Config:
        orm_mode = True


class ProductUpdate(ProductBase):
    pass