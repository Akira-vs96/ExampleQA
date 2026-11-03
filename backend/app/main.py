import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from qa_shop.store import Store

DUMMYJSON_OPENAPI_URL = "https://dummyjson.com/openapi.json"
# FastAPI 0.115 renders a classic script; ReDoc @next now serves a v3 ESM bundle.
REDOC_JS_URL = "https://cdn.jsdelivr.net/npm/redoc@2.5.2/bundles/redoc.standalone.js"


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def create_app(database_path: str | Path | None = None) -> FastAPI:
    application = FastAPI(
        title="DebugLab KZ API",
        description="1–15 зертханалық жұмыс және жергілікті QA Shop оқу API-і.",
        version="3.0.0",
    )
    application.state.shop_store = Store(
        database_path or os.getenv("QA_DATABASE", str(PROJECT_ROOT / "backend/.data/shop.sqlite3"))
    )

    @application.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "img-src 'self' data:; font-src 'self'; frame-ancestors 'none'; "
                "base-uri 'self'; form-action 'self'"
            )
            if not request.url.path.endswith(("/docs", "/redoc"))
            else (
                "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
                "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "connect-src 'self' https://dummyjson.com; "
            "img-src 'self' https://fastapi.tiangolo.com; "
                "worker-src blob:; frame-ancestors 'none'"
            )
        )
        if request.url.path.startswith("/api/shop"):
            response.headers["Cache-Control"] = "no-store"
        return response

    application.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router)

    @application.get("/lab9/docs", include_in_schema=False)
    def lab9_swagger() -> HTMLResponse:
        return get_swagger_ui_html(
            openapi_url=DUMMYJSON_OPENAPI_URL,
            title="Lab 9 — DummyJSON Swagger UI",
        )

    @application.get("/lab9/redoc", include_in_schema=False)
    def lab9_redoc() -> HTMLResponse:
        return get_redoc_html(
            openapi_url=DUMMYJSON_OPENAPI_URL,
            title="Lab 9 — DummyJSON ReDoc",
            redoc_js_url=REDOC_JS_URL,
        )

    @application.get("/labs.json", include_in_schema=False)
    def lab_catalogue() -> list[dict]:
        from app.lab_catalogue import catalogue

        return catalogue(PROJECT_ROOT)

    application.mount("/", StaticFiles(directory=PROJECT_ROOT / "frontend", html=True))
    return application


app = create_app()
