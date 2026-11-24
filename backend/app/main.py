import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from qa_shop.store import Store

DUMMYJSON_OPENAPI_URL = "https://dummyjson.com/openapi.json"
# FastAPI 0.115 renders a classic script; ReDoc @next now serves a v3 ESM bundle.
REDOC_JS_URL = "https://cdn.jsdelivr.net/npm/redoc@2.5.2/bundles/redoc.standalone.js"


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LAB12_EVIDENCE_FILES = frozenset(
    {
        "security-tests.log",
        "before_after.json",
        "zap-summary.json",
        "zap-before.json",
        "zap-after.json",
        "before-server.log",
        "before-zap.log",
        "after-server.log",
        "after-zap.log",
    }
)
LAB13_EVIDENCE_FILES = frozenset(
    {
        "before-pricing.py",
        "after-pricing.py",
        "test_regression.py",
        "before.txt",
        "after.txt",
        "before.xml",
        "after.xml",
        "comparison.json",
        "stability.json",
        "repeat-1.txt",
        "repeat-2.txt",
        "repeat-3.txt",
    }
)
LAB14_EVIDENCE_FILES = {
    "before-pricing.py": "backend/lab6/before/pricing.py",
    "after-pricing.py": "backend/qa_shop/pricing.py",
    "test_regression.py": "backend/lab13/tests/test_regression.py",
    "workflow.yml": ".github/workflows/labs.yml",
    "requirements-dev.txt": "requirements-dev.txt",
    "before.txt": "backend/lab14/results/before.txt",
    "after.txt": "backend/lab14/results/after.txt",
    "before.xml": "backend/lab14/results/before.xml",
    "after.xml": "backend/lab14/results/after.xml",
    "comparison.json": "backend/lab14/results/comparison.json",
    "pipeline-demo.log": "backend/lab15/results/pipeline-demo.log",
}
LAB15_EVIDENCE_FILES = {
    "before-pricing.py": "backend/lab6/before/pricing.py",
    "after-pricing.py": "backend/qa_shop/pricing.py",
    "before-security.py": "backend/lab12/before/security.py",
    "after-security.py": "backend/qa_shop/store.py",
    "safe-ui.js": "frontend/shop.js",
    "test-regression.py": "backend/lab13/tests/test_regression.py",
    "test-security.py": "backend/lab12/tests/test_security.py",
    "workflow.yml": ".github/workflows/labs.yml",
    "summary.md": "backend/lab15/results/SUMMARY.md",
    "summary.json": "backend/lab15/results/summary.json",
    "checks.json": "backend/lab15/results/checks.json",
    "full-checks.json": "backend/lab15/results/full-checks.json",
    "pytest.xml": "backend/lab15/results/pytest.xml",
    "coverage.json": "backend/lab15/results/coverage.json",
    "coverage.xml": "backend/lab15/results/coverage.xml",
    "before-after.log": "backend/lab15/results/before-after.log",
    "pipeline-demo.log": "backend/lab15/results/pipeline-demo.log",
    "tests.log": "backend/lab15/results/tests.log",
    "build.log": "backend/lab15/results/build.log",
    "analysis.log": "backend/lab15/results/analysis.log",
    "cases.log": "backend/lab15/results/cases.log",
    "debugger.log": "backend/lab15/results/debugger.log",
    "stability.log": "backend/lab15/results/stability.log",
    "browser.log": "backend/lab15/results/browser.log",
    "load.log": "backend/lab15/results/load.log",
    "security-demo.log": "backend/lab15/results/security-demo.log",
    "zap.log": "backend/lab15/results/zap.log",
    "lab8.log": "backend/lab15/results/lab8.log",
    "zap-summary.json": "backend/lab12/results/zap-summary.json",
    "performance.svg": "backend/lab11/results/performance.svg",
}


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

    @application.get("/lab12-results/{filename}", include_in_schema=False)
    def lab12_result(filename: str) -> FileResponse:
        if filename not in LAB12_EVIDENCE_FILES:
            raise HTTPException(status_code=404, detail="Evidence file not found")
        result_file = PROJECT_ROOT / "backend/lab12/results" / filename
        if not result_file.is_file():
            raise HTTPException(status_code=404, detail="Evidence file not found")
        return FileResponse(result_file)

    @application.get("/lab13-results/{filename}", include_in_schema=False)
    def lab13_result(filename: str) -> FileResponse:
        if filename not in LAB13_EVIDENCE_FILES:
            raise HTTPException(status_code=404, detail="Evidence file not found")
        if filename == "before-pricing.py":
            result_file = PROJECT_ROOT / "backend/lab6/before/pricing.py"
        elif filename == "after-pricing.py":
            result_file = PROJECT_ROOT / "backend/qa_shop/pricing.py"
        elif filename == "test_regression.py":
            result_file = PROJECT_ROOT / "backend/lab13/tests/test_regression.py"
        else:
            result_file = PROJECT_ROOT / "backend/lab13/results" / filename
        if not result_file.is_file():
            raise HTTPException(status_code=404, detail="Evidence file not found")
        return FileResponse(result_file)

    def evidence_response(files: dict[str, str], filename: str) -> FileResponse:
        relative_path = files.get(filename)
        if relative_path is None:
            raise HTTPException(status_code=404, detail="Evidence file not found")
        result_file = PROJECT_ROOT / relative_path
        if not result_file.is_file():
            raise HTTPException(status_code=404, detail="Evidence file not found")
        return FileResponse(result_file)

    @application.get("/lab14-results/{filename}", include_in_schema=False)
    def lab14_result(filename: str) -> FileResponse:
        return evidence_response(LAB14_EVIDENCE_FILES, filename)

    @application.get("/lab15-results/{filename}", include_in_schema=False)
    def lab15_result(filename: str) -> FileResponse:
        return evidence_response(LAB15_EVIDENCE_FILES, filename)

    application.mount("/", StaticFiles(directory=PROJECT_ROOT / "frontend", html=True))
    return application


app = create_app()
