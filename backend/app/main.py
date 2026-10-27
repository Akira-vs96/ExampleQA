from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.api.router import api_router


DUMMYJSON_OPENAPI_URL = "https://dummyjson.com/openapi.json"
# FastAPI 0.115 renders a classic script; ReDoc @next now serves a v3 ESM bundle.
REDOC_JS_URL = "https://cdn.jsdelivr.net/npm/redoc@2.5.2/bundles/redoc.standalone.js"


def create_app() -> FastAPI:
    application = FastAPI(
        title="DebugLab KZ API",
        description="7–9 зертханалық жұмыстарға арналған оқу API-і.",
        version="2.1.0",
    )
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

    return application


app = create_app()
