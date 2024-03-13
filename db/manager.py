from sqlalchemy import create_engine, func, inspect
from sqlalchemy.orm import configure_mappers, sessionmaker
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

        configure_mappers()

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        insp = inspect(self.engine)
        if not insp.has_table('products'):
            # Criar a tabela 'products' se ela não existir
            Base.metadata.create_all(self.engine)

    def create_product(self, product_data: ProductCreate):
        try:
            """
            Cria um novo produto no banco de dados.
            """
            new_product = Product(**product_data.dict())

            self.session.add(new_product)
            self.session.commit()
            logger.info(f'New product {new_product.name}')
        except Exception as e:
            logger.error(f'Error creating product: {e}')

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
                existing_product.price_real_symbol = product_data.price_real_symbol
                existing_product.price_us_symbol = product_data.price_us_symbol
                existing_product.discountPrice_price_real = product_data.discountPrice_price_real
                existing_product.discountPrice_us = product_data.discountPrice_us
                existing_product.discountPrice_real_symbol = product_data.discountPrice_real_symbol
                existing_product.discountPrice_us_symbol = product_data.discountPrice_us_symbol
                

                product_price = PriceHistoryUpdate(
                    product_id=product_data.product_id,
                    new_price=product_data.price_real,
                    price_real_symbol=product_data.price_real_symbol,
                    price_real=product_data.price_real,
                    price_us_symbol=product_data.price_us_symbol,
                    price_us=product_data.price_us,
                    discountPrice_price_real=product_data.discountPrice_price_real,
                    discountPrice_us=product_data.discountPrice_us,
                    discountPrice_real_symbol=product_data.discountPrice_real_symbol,
                    discountPrice_us_symbol=product_data.discountPrice_us_symbol
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
            product.price_real = product_price.new_price
            product.price_real_symbol = product_price.price_real_symbol
            product.price_us = product_price.price_us
            product.price_us_symbol = product_price.price_us_symbol
            product.discountPrice_price_real = product_price.discountPrice_price_real
            product.discountPrice_real_symbol = product_price.discountPrice_real_symbol
            product.discountPrice_us = product_price.discountPrice_us
            product.discountPrice_price_us_symbol = product_price.discountPrice_price_us_symbol
            
            self.session.commit()

    def get_product_by_id(self, product_id: int):
        """
        Retorna um produto do banco de dados com base no ID.
        """
        return (
            self.session.query(Product)
            .filter_by(id=product_id)
            .first()
        )

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
                new_price=product_price.new_price,
                price_real_symbol=product_price.price_real_symbol,
                price_real=product_price.price_real,
                price_us_symbol=product_price.price_us_symbol,
                price_us=product_price.price_us,
                discountPrice_price_real=product_price.discountPrice_price_real,
                discountPrice_us=product_price.discountPrice_us,
                discountPrice_real_symbol=product_price.discountPrice_real_symbol,
                discountPrice_us_symbol=product_price.discountPrice_us_symbol
            )
            logger.info(
                f'New price history for product {product.data_title} : new price : {product_price.new_price}'
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

    