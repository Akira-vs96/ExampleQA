from fastapi import APIRouter, HTTPException

from app.schemas import DebugExample, DebugRequest, DebugResult
from lab7.catalog import EXAMPLES


router = APIRouter(tags=["lab 7"])


def _find_example(example_id: str) -> DebugExample:
    example = EXAMPLES.get(example_id)
    if example is None:
        raise HTTPException(status_code=404, detail="Мұндай практикалық мысал табылмады.")
    return DebugExample(**example)


@router.get("/lab7/examples", response_model=list[DebugExample])
def list_examples() -> list[DebugExample]:
    return [DebugExample(**example) for example in EXAMPLES.values()]


@router.get("/lab7/examples/{example_id}", response_model=DebugExample)
def get_example(example_id: str) -> DebugExample:
    return _find_example(example_id)


@router.post("/lab7/debug/run", response_model=DebugResult)
def run_debug(request: DebugRequest) -> DebugResult:
    example = _find_example(request.example_id)
    line = request.breakpoint_line or example.breakpoint_line
    return DebugResult(
        example_id=example.id,
        breakpoint_line=line,
        message=f"Debug режимі іске қосылды. {line}-жолда орындалу тоқтады.",
        variables=example.variables,
        buggy_result=example.buggy_result,
        fixed_result=example.fixed_result,
        next_action="Айнымалыларды тексеріп, Step Over арқылы келесі жолға өтіңіз.",
    )


# Бұрынғы frontend build және сілтемелер үшін ескі URL-дер сақталады.
@router.get("/examples", response_model=list[DebugExample], deprecated=True)
def list_examples_legacy() -> list[DebugExample]:
    return list_examples()


@router.get("/examples/{example_id}", response_model=DebugExample, deprecated=True)
def get_example_legacy(example_id: str) -> DebugExample:
    return get_example(example_id)


@router.post("/debug/run", response_model=DebugResult, deprecated=True)
def run_debug_legacy(request: DebugRequest) -> DebugResult:
    return run_debug(request)
