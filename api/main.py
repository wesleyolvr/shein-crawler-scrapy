from fastapi import FastAPI, HTTPException

from api.schemas.product import ProductCreate, ProductRead
from db.manager import DatabaseManager

from config import DATABASE_URL

app = FastAPI()


@app.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate):
    db_manager = DatabaseManager(database_url=DATABASE_URL)
    db_manager.create_product(product)
    return product


@app.get("/products/{product_id}", response_model=ProductRead)
def read_product(product_id: int):
    db_manager = DatabaseManager(database_url=DATABASE_URL)
    product = db_manager.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/some_products/", response_model=list[ProductRead])
def read_products(limit):
    db_manager = DatabaseManager(database_url=DATABASE_URL)
    products = db_manager.get_some_products(limit=limit)
    return products


@app.get("/")
def home():
    return {"Ola": "Mundo"}


if __name__ == "__main__":
    pass
