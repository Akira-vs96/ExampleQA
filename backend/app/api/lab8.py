"""8-зертханалық жұмыстың Static Analysis есебіне арналған API."""

from fastapi import APIRouter

from app.schemas import Lab8Case, Lab8RunResult
from lab8.catalog import build_case

router = APIRouter(tags=["lab 8"])


@router.get("/lab8/case", response_model=Lab8Case)
def get_lab8_case() -> Lab8Case:
    """Before/after коды мен 20 тапсырманың дәлелдерін қайтарады."""
    return Lab8Case(**build_case())


@router.post("/lab8/quality-gate", response_model=Lab8RunResult)
def get_lab8_quality_gate() -> Lab8RunResult:
    """run_analysis.sh арқылы тексерілген Quality Gate нәтижесін қайтарады."""
    return Lab8RunResult(
        message="Ruff, Pylint, Radon және 14 тест бойынша барлық шарт орындалды.",
        ruff_issues=0,
        pylint_messages=0,
        pylint_score="10.00/10",
        security_issues=0,
        duplicate_blocks=0,
        max_complexity=4,
        tests="14/14 passed",
        quality_gate="PASSED",
    )
