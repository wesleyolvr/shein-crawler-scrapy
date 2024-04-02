from pydantic import BaseModel, validator
from datetime import datetime


class ProductBase(BaseModel):
    product_id: int
    name: str
    sn: str
    url: str
    imgs: str
    category: str
    store_code: int = None
    is_on_sale: bool
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discount_price_real_symbol: str
    discount_price_real: float
    discount_price_us_symbol: str
    discount_price_us: float
    datetime_collected: datetime


class ProductCreate(ProductBase):
    @validator('name', pre=True)
    # pylint: disable=no-self-argument
    def truncate_name(cls, v):
        # Trunca o nome para o tamanho máximo permitido
        return v[:350]

    @validator('category', pre=True)
    # pylint: disable=no-self-argument
    def truncate_category(cls, v):
        # Trunca a categoria para o tamanho máximo permitido
        return v[:400]


class ProductRead(ProductBase):
    datetime_collected: datetime

    class Config:
        from_attributes = True


class ProductUpdate(ProductBase):
    pass
