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


class Lab8Task(BaseModel):
    id: int
    title: str
    evidence: str
    status: str


class Lab8Diagnostic(BaseModel):
    code: str
    count: int
    description: str
    severity: str


class Lab8Metric(BaseModel):
    metric: str
    before: str
    after: str
    change: str


class Lab8QualityCheck(BaseModel):
    condition: str
    threshold: str
    result: str
    status: str


class Lab8Deficiency(BaseModel):
    id: int
    problem: str
    severity: str
    detection: str
    fix: str


class Lab8Case(BaseModel):
    id: str
    title: str
    summary: str
    source_files: list[str]
    fixed_files: list[str]
    buggy_code: str
    fixed_code: str
    standards: list[str]
    tools: list[dict[str, str]]
    warnings: list[Lab8Diagnostic]
    errors: list[Lab8Diagnostic]
    code_smells: list[str]
    duplicate_evidence: str
    complexity: list[dict[str, str]]
    security_issues: list[Lab8Diagnostic]
    checklist: list[str]
    deficiencies: list[Lab8Deficiency]
    metrics: list[Lab8Metric]
    quality_gate: list[Lab8QualityCheck]
    tasks: list[Lab8Task]
    conclusion: str


class Lab8RunResult(BaseModel):
    message: str
    ruff_issues: int
    pylint_messages: int
    pylint_score: str
    security_issues: int
    duplicate_blocks: int
    max_complexity: int
    tests: str
    quality_gate: str
