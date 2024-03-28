from pydantic import BaseModel, Field, root_validator, validator, field_validator


class ProductItem(BaseModel):
    product_id: int
    name: str
    sn: str
    url: str
    imgs: str
    category: str  # Campo privado para armazenar a categoria
    store_code: int = 0
    is_on_sale: bool
    price_real_symbol: str
    price_real: float
    price_us_symbol: str
    price_us: float
    discount_price_real_symbol: str
    discount_price_real: float
    discount_price_us_symbol: str
    discount_price_us: float
    datetime_collected: str

    @validator('store_code', pre=True)
    # pylint: disable=no-self-argument
    def convert_to_integer(cls, value):
        """Converte para int."""
        if value is None or value == '':
            return 0
        return int(value)

    @field_validator('imgs', mode='before')
    def convert_imgs_to_string(cls, value):
        """Converte uma lista de imgs em uma string."""
        if value is None or value == '':
            return ''
        return ','.join(value)

    @field_validator('is_on_sale', mode='before')
    def convert_is_on_sale(cls, value):
        """Converte para booleano."""
        if isinstance(value, bool):
            return value
        if str(value).lower() in ['1', 'true', 1, 'True']:
            return True
        else:
            return False

    @field_validator('price_real', 'discount_price_real')
    def convert_price(cls, value):
        """Converte para float."""
        if value is None or value == '':
            return 0
        return float(value)  # Converte para float após a substituição

    @field_validator('name')
    def truncate_name(cls, v):
        # Trunca o nome para o tamanho máximo permitido
        return v[:350]

    @validator('category', always=True)
    def validate_category(cls, v):
        # Trunca a categoria para o tamanho máximo permitido
        return v[:350]

    @property
    def category(self, value):
        # Método para definir o valor do campo category e validar
        self.category = self.validate_category(value)
