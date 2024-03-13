from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from db.manager import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
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
    discountPrice_real_symbol = Column(String)
    discountPrice_price_real = Column(Float)
    discountPrice_price_us_symbol = Column(String)
    discountPrice_us = Column(Float)
    datetime_collected = Column(String)
    
    price_history = relationship('PriceHistory', back_populates='product')
