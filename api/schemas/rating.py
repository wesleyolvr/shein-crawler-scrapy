from pydantic import BaseModel


class ProductRatingBase(BaseModel):

    rating: float


class ProductRatingCreate(ProductRatingBase):
    pass


class ProductRatingRead(ProductRatingBase):
    id: int

    class Config:
        from_attributes = True
