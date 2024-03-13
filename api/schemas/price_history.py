from pydantic import BaseModel


class PriceHistoryBase(BaseModel):
    date: str
    price: float
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discountPrice_real_symbol: str
    discountPrice_price_real: float
    discountPrice_price_us_symbol: str
    discountPrice_us: float


class PriceHistoryCreate(PriceHistoryBase):
    pass


class PriceHistoryRead(PriceHistoryBase):
    id: int

    class Config:
        orm_mode = True


class PriceHistoryUpdate(PriceHistoryBase):
    product_id: int
    new_price: float
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discountPrice_real_symbol: str
    discountPrice_price_real: float
    discountPrice_price_us_symbol: str
    discountPrice_us: float
