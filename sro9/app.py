"""Stateful local REST API for the SRO 9 assignment. Prices are integer KZT."""

from typing import Annotated, Self

from fastapi import FastAPI, HTTPException, Path, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator

ProductId = Annotated[int, Path(ge=1)]


class ProductInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    price: int = Field(ge=0, le=1_000_000)
    stock: int = Field(ge=0, le=1000)


class Product(ProductInput):
    id: int


class ProductPatch(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: int | None = Field(default=None, ge=0, le=1_000_000)
    stock: int | None = Field(default=None, ge=0, le=1000)

    @model_validator(mode="after")
    def nonempty_changes(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Кемінде бір өрісті жіберіңіз.")
        if any(getattr(self, name) is None for name in self.model_fields_set):
            raise ValueError("Өріс мәні null болмауы керек.")
        return self


def create_app() -> FastAPI:
    """Create fresh storage per app, so tests and demonstrations are repeatable."""
    application = FastAPI(title="СРО 9 — Products REST API", version="1.0.0")
    products = {1: Product(id=1, name="Keyboard", price=5000, stock=10)}
    next_id = 2

    def find_product(product_id: int) -> Product:
        if product_id not in products:
            raise HTTPException(status_code=404, detail="Тауар табылмады.")
        return products[product_id]

    @application.get("/api/products", response_model=list[Product])
    def list_products() -> list[Product]:
        return list(products.values())

    @application.get("/api/products/{product_id}", response_model=Product)
    def get_product(product_id: ProductId) -> Product:
        return find_product(product_id)

    @application.post("/api/products", response_model=Product, status_code=201)
    def create_product(data: ProductInput, response: Response) -> Product:
        nonlocal next_id
        product = Product(id=next_id, **data.model_dump())
        products[next_id] = product
        next_id += 1
        response.headers["Location"] = f"/api/products/{product.id}"
        return product

    @application.put("/api/products/{product_id}", response_model=Product)
    def replace_product(product_id: ProductId, data: ProductInput) -> Product:
        find_product(product_id)
        products[product_id] = Product(id=product_id, **data.model_dump())
        return products[product_id]

    @application.patch("/api/products/{product_id}", response_model=Product)
    def update_product(product_id: ProductId, data: ProductPatch) -> Product:
        original = find_product(product_id)
        products[product_id] = Product(
            **(original.model_dump() | data.model_dump(exclude_unset=True))
        )
        return products[product_id]

    @application.delete("/api/products/{product_id}", status_code=204)
    def delete_product(product_id: ProductId) -> Response:
        find_product(product_id)
        del products[product_id]
        return Response(status_code=204)

    return application


app = create_app()
