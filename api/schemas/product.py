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



# from typing import Optional

# from pydantic import BaseModel, Field, validator


# class ProductBase(BaseModel):
#     product_id: int
#     product_type: str
#     href: str
#     data_title: str
#     data_price: float
#     data_id_category: str
#     data_sku: str
#     data_spu: str
#     data_us_price: float
#     data_us_origin_price: float
#     discount: str
#     image_src: str


# class ProductCreate(ProductBase):
#     product_id: int
#     product_type: str
#     data_title: str
#     data_price: float
#     data_us_price: float
#     data_us_origin_price: float
#     discount: Optional[float] = Field(default=None)

#     @validator('data_price', 'data_us_price', 'data_us_origin_price', pre=True)
#     # pylint: disable=no-self-argument
#     def check_comma_and_convert(cls, value):
#         """Verifica se o valor tem vírgula e converte para float."""
#         if ',' in str(value):
#             return float(value.replace(',', '.'))
#         return float(value)

#     @validator(
#         'data_price',
#         'data_us_price',
#         'data_us_origin_price',
#         'discount',
#         pre=True,
#     )
#     # pylint: disable=no-self-argument
#     def check_empty_values(cls, value):
#         """Verifica se o valor esta vazio e retorna 0."""
#         if value is None or value == '':
#             return 0.0
#         return value

#     @validator('product_type', pre=True)
#     # pylint: disable=no-self-argument
#     def format_type_products(cls, value):
#         """Formata o nome dotipo de produto."""
#         return value.replace('-', ' ')

#     @validator('data_price', pre=False)
#     # pylint: disable=no-self-argument
#     def format_price(cls, value):
#         """Formata o preço para float."""
#         return float(value)


# class ProductRead(ProductBase):
#     class Config:
#         orm_mode = True


# class ProductUpdate(ProductBase):
#     pass
