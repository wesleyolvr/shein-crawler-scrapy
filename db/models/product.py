from sqlalchemy import TIMESTAMP, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    name = Column(String)
    sn = Column(String)
    url = Column(String)
    imgs = Column(String)
    category = Column(String)
    store_code = Column(Integer)
    is_on_sale = Column(Integer)
    price_real_symbol = Column(String)
    price_real = Column(Float)
    price_us_symbol = Column(String)
    price_us = Column(Float)
    discount_price_real_symbol = Column(String)
    discount_price_real = Column(Float)
    discount_price_us_symbol = Column(String)
    discount_price_us = Column(Float)
    datetime_collected = Column(TIMESTAMP)

    price_history = relationship('PriceHistory', back_populates='product')
