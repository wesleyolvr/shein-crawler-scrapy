from pydantic import BaseModel


class PriceHistoryBase(BaseModel):
    date: str
    price: float
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discount_price_real_symbol: str
    discount_price_real: float
    discount_price_us_symbol: str
    discount_price_us: float


class PriceHistoryCreate(PriceHistoryBase):
    pass


class PriceHistoryRead(PriceHistoryBase):
    product_id: int

    class Config:
        orm_mode = True


class PriceHistoryUpdate(PriceHistoryBase):
    product_id: int
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discount_price_real_symbol: str
    discount_price_real: float
    discount_price_us_symbol: str
    discount_price_us: float
