from pydantic import BaseModel, Field


class DebugRequest(BaseModel):
    example_id: str = Field(min_length=1)
    breakpoint_line: int | None = Field(default=None, ge=1)


class LectureTopic(BaseModel):
    id: int
    question: str
    short_answer: str
    details: list[str]
    key_terms: list[str]
    practical_tip: str


class LessonStep(BaseModel):
    id: int
    title: str
    description: str
    action: str


class DebugExample(BaseModel):
    id: str
    title: str
    error_type: str
    difficulty: str
    summary: str
    buggy_code: str
    fixed_code: str
    breakpoint_line: int
    variables: dict[str, str]
    buggy_result: str
    fixed_result: str
    tests: list[dict[str, str]]
    report: dict[str, str]


class DebugResult(BaseModel):
    example_id: str
    breakpoint_line: int
    message: str
    variables: dict[str, str]
    buggy_result: str
    fixed_result: str
    next_action: str
