"""Loopback-only scan target for demonstrating missing response headers."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/shop.html", response_class=HTMLResponse)
def index():
    return '<!doctype html><html lang="en"><title>Before</title><body><h1>QA Shop</h1></body></html>'


@app.get("/api/shop/products")
def products():
    return [{"id": 1, "name": "Keyboard", "price": "5000.00"}]
