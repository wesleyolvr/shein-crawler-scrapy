from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import sessionmaker, Session

from api.schemas.price_history import PriceHistoryUpdate
from api.schemas.product import ProductCreate, ProductRead
from db.database import Base
from db.models.price_history import PriceHistory
from db.models.product import Product
from logs.logger import logger


class DatabaseManager:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(self.database_url)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Se desejar, você pode adicionar lógica para criar tabelas
        # específicas do PostgreSQL aqui

    def create_product(self, product_data: ProductCreate):
        """
        Cria um novo registro de produto no banco de dados.
        """
        new_product = Product(
            product_id=product_data.product_id,
            name=product_data.name,
            sn=product_data.sn,
            url=product_data.url,
            imgs=product_data.imgs,
            category=product_data.category,
            store_code=product_data.store_code,
            is_on_sale=product_data.is_on_sale,
            price_real_symbol=product_data.price_real_symbol,
            price_real=product_data.price_real,
            price_us_symbol=product_data.price_us_symbol,
            price_us=product_data.price_us,
            discount_price_real_symbol=product_data.discount_price_real_symbol,
            discount_price_real=product_data.discount_price_real,
            discount_price_us_symbol=product_data.discount_price_us_symbol,
            discount_price_us=product_data.discount_price_us,
            datetime_collected=product_data.datetime_collected
        )
        self.session.add(new_product)
        self.session.commit()

    def update_product(self, product_data: ProductCreate):
        """
        Atualiza os dados de um produto existente no banco de dados.
        """
        existing_product = self.get_product_by_id(product_data.product_id)
        if existing_product:
            if existing_product.price_real != product_data.price_real:
                logger.info(
                    f'Updating product {product_data.name}: new price: {product_data.price_real} - old price: {existing_product.price_real}'
                )
                existing_product.price_real = product_data.price_real
                existing_product.price_us = product_data.price_us
                existing_product.price_real_symbol = (
                    product_data.price_real_symbol
                )
                existing_product.price_us_symbol = product_data.price_us_symbol
                existing_product.discount_price_real = (
                    product_data.discount_price_real
                )
                existing_product.discount_price_us = (
                    product_data.discount_price_us
                )
                existing_product.discount_price_real_symbol = (
                    product_data.discount_price_real_symbol
                )
                existing_product.discount_price_us_symbol = (
                    product_data.discount_price_us_symbol
                )

                product_price = PriceHistoryUpdate(
                    product_id=product_data.product_id,
                    price_real=product_data.price_real,
                    price_real_symbol=product_data.price_real_symbol,
                    price_us_symbol=product_data.price_us_symbol,
                    price_us=product_data.price_us,
                    discount_price_real=product_data.discount_price_real,
                    discount_price_us=product_data.discount_price_us,
                    discount_price_real_symbol=product_data.discount_price_real_symbol,
                    discount_price_us_symbol=product_data.discount_price_us_symbol,
                )

                self.add_price_history(product_price)
                self.session.commit()

    def update_product_price(self, product_price: PriceHistoryUpdate):
        """
        Atualiza o preço de um produto existente no banco de dados.
        """
        product = (
            self.session.query(Product)
            .filter_by(id=product_price.product_id)
            .first()
        )
        if product:
            product.price_real = product_price.price_real
            product.price_real_symbol = product_price.price_real_symbol
            product.price_us = product_price.price_us
            product.price_us_symbol = product_price.price_us_symbol
            product.discount_price_real = (
                product_price.discount_price_real
            )
            product.discount_price_real_symbol = (
                product_price.discount_price_real_symbol
            )
            product.discount_price_us = product_price.discount_price_us
            product.discount_price_us_symbol = (
                product_price.discount_price_us_symbol
            )

            self.session.commit()

    def get_product_by_id(self, product_id: int):
        """
        Retorna um produto do banco de dados com base no ID.
        """
        return self.session.query(Product).filter_by(product_id=product_id).first()

    def get_product_by_title(self, product_read: ProductRead):
        """
        Retorna um produto do banco de dados com base no título.
        """
        return (
            self.session.query(Product)
            .filter_by(data_title=product_read['title'])
            .first()
        )

    def get_price_history_by_id(self, product_read: ProductRead):
        """
        Retorna o histórico de preços de um determinado produto.
        """
        return (
            self.session.query(PriceHistory)
            .filter_by(product_id=product_read['product_id'])
            .all()
        )

    def add_price_history(self, product_price: PriceHistoryUpdate):
        """
        Adiciona um novo histórico de preço para um produto no banco de dados.
        """
        product = self.get_product_by_id(product_price.product_id)
        if product:
            new_price_history = PriceHistoryUpdate(
                product_id=product_price.product_id,
                price_real_symbol=product_price.price_real_symbol,
                price_real=product_price.price_real,
                price_us_symbol=product_price.price_us_symbol,
                price_us=product_price.price_us,
                discount_price_real=product_price.discount_price_real,
                discount_price_real_symbol=product_price.discount_price_real_symbol,
                discount_price_us_symbol=product_price.discount_price_us_symbol,
                discount_price_us=product_price.discount_price_us,
            )
            logger.info(
                f'New price history for product {product.name} : new price : {product_price.price_real}'
            )
            product.price_history.append(
                new_price_history
            )  # Adiciona o novo histórico à lista
            self.session.commit()

    def get_all_products(self):
        return self.session.query(Product).all()

    def get_all_href_products(self):
        return self.session.query(Product.href).all()

    def get_products_with_multiple_price_history(self):
        """
        Retorna todos os produtos que possuem mais de um histórico de preços.
        """
        # Subconsulta para contar o número de registros em PriceHistory para cada produto
        subquery = (
            self.session.query(
                PriceHistory.product_id,
                func.count().label('count_price_history'),
            )
            .group_by(PriceHistory.product_id)
            .subquery()
        )

        # Consulta principal para obter produtos com mais de um histórico de preços
        products_with_multiple_history = (
            self.session.query(Product)
            .join(subquery, Product.product_id == subquery.c.product_id)
            .filter(subquery.c.count_price_history > 1)
            .all()
        )

        return products_with_multiple_history
