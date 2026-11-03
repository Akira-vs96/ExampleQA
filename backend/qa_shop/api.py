"""HTTP adapter for the local QA shop; dependencies can be replaced in tests."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, Request, Response
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator

from qa_shop.pricing import discounted_total, line_total, order_total, shipping_cost
from qa_shop.store import Store

router = APIRouter(prefix="/shop", tags=["QA shop"])
PRODUCTS = (
    {"id": 1, "name": "Keyboard", "price": "5000.00"},
    {"id": 2, "name": "Mouse", "price": "2500.00"},
    {"id": 3, "name": "Monitor", "price": "45000.00"},
)


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=3, max_length=40, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)


class QuoteItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    product_id: StrictInt = Field(ge=1)
    quantity: StrictInt = Field(ge=1, le=100)


class QuoteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    items: list[QuoteItem] = Field(min_length=1, max_length=50)
    percent: StrictInt = Field(default=0, ge=0, le=100)

    @field_validator("items")
    @classmethod
    def unique_products(cls, items: list[QuoteItem]) -> list[QuoteItem]:
        if len({item.product_id for item in items}) != len(items):
            raise ValueError("Тауарды бір рет қана қосыңыз.")
        return items


def get_store(request: Request) -> Store:
    return request.app.state.shop_store


def get_user(
    store: Annotated[Store, Depends(get_store)],
    qa_session: Annotated[str | None, Cookie()] = None,
) -> dict:
    user = store.user_for_token(qa_session) if qa_session else None
    if user is None:
        raise HTTPException(status_code=401, detail="Алдымен жүйеге кіріңіз.")
    return user


@router.post("/register", status_code=201)
def register(credentials: Credentials, store: Annotated[Store, Depends(get_store)]) -> dict:
    try:
        return store.register(credentials.username, credentials.password)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.post("/login")
def login(
    credentials: Credentials,
    request: Request,
    response: Response,
    store: Annotated[Store, Depends(get_store)],
) -> dict:
    token = store.login(credentials.username, credentials.password)
    if token is None:
        raise HTTPException(status_code=401, detail="Логин немесе пароль қате.")
    response.set_cookie(
        "qa_session",
        token,
        httponly=True,
        samesite="strict",
        secure=request.url.scheme == "https",
        max_age=3600,
        path="/api/shop",
    )
    return {"message": "Жүйеге кірдіңіз."}


@router.get("/me")
def me(user: Annotated[dict, Depends(get_user)]) -> dict:
    return user


@router.delete("/session", status_code=204)
def logout(
    response: Response,
    store: Annotated[Store, Depends(get_store)],
    qa_session: Annotated[str | None, Cookie()] = None,
) -> None:
    if qa_session:
        store.logout(qa_session)
    response.delete_cookie("qa_session", path="/api/shop", samesite="strict")


@router.get("/products")
def products(q: Annotated[str, Query(max_length=80)] = "") -> list[dict]:
    return [item for item in PRODUCTS if q.casefold() in item["name"].casefold()]


@router.get("/products/{product_id}")
def product(product_id: int) -> dict:
    result = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if result is None:
        raise HTTPException(status_code=404, detail="Тауар табылмады.")
    return result


@router.post("/quote")
def quote(data: QuoteRequest, user: Annotated[dict, Depends(get_user)]) -> dict:
    lines = [(product(item.product_id)["price"], item.quantity) for item in data.items]
    subtotal = sum(line_total(price, count) for price, count in lines)
    discounted = discounted_total(subtotal, data.percent)
    return {
        "user_id": user["id"],
        "subtotal": str(subtotal),
        "discounted": str(discounted),
        "shipping": str(shipping_cost(discounted)),
        "total": str(order_total(lines, data.percent)),
        "currency": "KZT",
    }
