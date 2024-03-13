from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.manager import Base


class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(String)  # Alterado para armazenar a data como uma string
    price = Column(Float)
    price_real_symbol = Column(String)
    price_real = Column(Float)
    price_us_symbol = Column(String)
    price_us = Column(Float)
    discountPrice_real_symbol = Column(String)
    discountPrice_price_real = Column(Float)
    discountPrice_price_us_symbol = Column(String)
    discountPrice_us = Column(Float)

    # Chave estrangeira para o produto
    product_id = Column(
        Integer, ForeignKey('products.id')
    )  # A chave estrangeira deve referenciar a coluna 'id' de 'products'

    # Relacionamento com o produto
    product = relationship('Product', back_populates='price_history')
