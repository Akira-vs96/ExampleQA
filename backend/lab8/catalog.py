"""8-зертхананың сайтта көрсетілетін Static Analysis есебі."""

BUGGY_CODE = '''def calculate_order(
    items, customer_type, discount_expression, cache={}
):
    total = 0
    if items == None:
        return 0
    for item in normalize_items(items):
        if item["price"] < 0:
            print("negative price")
        total += item["price"] * item["quantity"]
    # бес тармақты customer_type шарттары...
    discount = eval(discount_expression)
    if discount > 50:
        discount = 50
    subprocess.call(
        "echo order-for-" + customer_type, shell=True
    )
    try:
        cache[customer_type] = total / len(items)
    except:
        cache[customer_type] = 0
    print(customer_name)
    return total'''

FIXED_CODE = '''@dataclass(frozen=True, slots=True)
class OrderItem:
    name: str
    unit_price: Decimal
    quantity: int = 1

def calculate_order(
    items: Iterable[OrderItem],
    customer_type: CustomerType = CustomerType.REGULAR,
    promo_percent: Decimal = Decimal(0),
) -> OrderSummary:
    if not MIN_PERCENT <= promo_percent <= MAX_PERCENT:
        raise OrderValidationError(
            "Жеңілдік 0 мен 100 аралығында болуы керек."
        )
    subtotal = calculate_subtotal(items)
    discount = max(
        CUSTOMER_DISCOUNTS[customer_type], promo_percent
    )
    amount = (subtotal * discount / HUNDRED).quantize(
        MONEY_STEP
    )
    return OrderSummary(
        subtotal, discount, amount, subtotal - amount
    )'''

STANDARDS = [
    "PEP 8, import order және жол ұзындығы ≤ 100",
    "Public API үшін type hint және docstring",
    "Ақшалай есептеулер үшін Decimal",
    "Кіріс деректерін есептеуге дейін тексеру",
    "Cyclomatic complexity ≤ 10",
    "DRY: ортақ логиканы көшірмеу",
    "eval, shell=True және hardcoded secret қолданбау",
    "Өзгерістерді regression тесттерімен қорғау",
]

WARNINGS = [
    ("F401 / W0611", 1, "Қолданылмаған os импорты", "Low"),
    ("S105", 1, "Кодқа жазылған құпиясөз", "High"),
    ("C901", 1, "calculate_order complexity = 11", "Medium"),
    ("B006 / W0102", 1, "Mutable default argument cache={}", "High"),
    ("E711 / C0121", 1, "None мәнімен == арқылы салыстыру", "Low"),
    ("S307 / W0123", 1, "Қауіпті eval() қолдану", "Critical"),
    ("PLR1730 / R1730", 1, "Артық if блогы", "Low"),
    ("PLR2004", 1, "50 magic value", "Low"),
    ("S602", 1, "Input мәні бар shell=True", "Critical"),
    ("E722 / W0702", 1, "Bare except", "Medium"),
    ("C0116", 2, "Public функциялардың docstring-і жоқ", "Low"),
    ("R0801", 1, "Екі файлдағы қайталанған код", "Medium"),
]

DEFICIENCIES = [
    (1, "Сенімсіз мәтінді eval() орындауы", "Critical", "Ruff S307, review", "Decimal параметрі"),
    (2, "Input-пен shell=True шақыруы", "Critical", "Ruff S602, review", "subprocess жойылды"),
    (3, "Hardcoded admin password", "High", "Ruff S105", "secret кодтан жойылды"),
    (4, "Анықталмаған customer_name", "High", "F821 / E0602", "жанама output жойылды"),
    (5, "cache={} ортақ күй сақтайды", "High", "B006 / W0102", "cache міндеті жойылды"),
    (6, "Теріс баға есепке қосылады", "High", "Manual review", "validation қосылды"),
    (7, "Bare except қатені жасырады", "Medium", "E722 / W0702", "catch жойылды"),
    (8, "CC=11 және міндеті көп функция", "Medium", "C901, Radon", "функциялар бөлінді"),
    (9, "normalize_items көшірілген", "Medium", "Pylint R0801", "ортақ subtotal"),
    (10, "Қолданылмайтын os импорты", "Low", "F401 / W0611", "импорт жойылды"),
]

TASKS = [
    (1, "Код жобасын таңдау", "Order және refund есептеу модульдері таңдалды."),
    (2, "Coding Standards анықтау", "PEP 8, typing, Decimal, DRY және CC≤10 бекітілді."),
    (3, "Pylint/Ruff орнату", "requirements-dev.txt ішінде нақты нұсқалар бекітілді."),
    (4, "Static Analysis жүргізу", "Ruff, Pylint және Radon іске қосылды."),
    (5, "Warning тізімін алу", "12 санаттағы warning/issue құжатталды."),
    (6, "Error тізімін алу", "F821/E0602 undefined customer_name табылды."),
    (7, "Code Smell анықтау", "Long Method, primitives, magic values және dead code табылды."),
    (8, "Duplicate Code анықтау", "Pylint R0801 normalize_items көшірмесін тапты."),
    (9, "Complexity талдау", "Max CC 11 және орташа CC 4.25 өлшенді."),
    (10, "Security issue іздеу", "S307, S602 және S105 табылды."),
    (11, "Code Review Checklist жасау", "11 тармақтық checklist дайындалды."),
    (12, "Кодты қолмен тексеру", "Теріс бағаны есептеу бизнес қатесі табылды."),
    (13, "10 кемшілікті анықтау", "Дәл 10 негізгі кемшілік кестеге енгізілді."),
    (14, "Severity бойынша жіктеу", "Critical 2, High 4, Medium 3, Low 1."),
    (15, "Кодты түзету", "Models, validation, Decimal және ортақ subtotal енгізілді."),
    (16, "Анализді қайта жүргізу", "Түзетілген scope барлық тексеруден өтті."),
    (17, "Нәтижелерді салыстыру", "Before/after метрикалары салыстырылды."),
    (18, "Quality Gate анықтау", "Алты шарттың барлығы PASS."),
    (19, "Метрикаларды кестеге енгізу", "10 негізгі сапа метрикасы берілді."),
    (20, "Қорытынды есеп дайындау", "REPORT.md және веб-бөлім дайындалды."),
]


def _diagnostic(row: tuple[str, int, str, str]) -> dict[str, object]:
    code, count, description, severity = row
    return {"code": code, "count": count, "description": description, "severity": severity}


def build_case() -> dict[str, object]:
    """Static Analysis есебінің UI-ға арналған құрылымын қайтарады."""
    return {
        "id": "order-quality-analysis",
        "title": "Тапсырыс модулінің код сапасын талдау",
        "summary": (
            "Ruff, Pylint, Radon және қолмен Code Review арқылы бастапқы кодтағы "
            "ақаулар табылып, қауіпсіз әрі типтелген нұсқаға refactoring жасалды."
        ),
        "source_files": [
            "backend/lab8/before/order_service.py",
            "backend/lab8/before/refund_service.py",
        ],
        "fixed_files": [
            "backend/lab8/order_service.py",
            "backend/lab8/refund_service.py",
        ],
        "buggy_code": BUGGY_CODE,
        "fixed_code": FIXED_CODE,
        "standards": STANDARDS,
        "tools": [
            {"name": "Ruff", "version": "0.17.1", "purpose": "Style, error, complexity, security"},
            {"name": "Pylint", "version": "4.1.3", "purpose": "Code smell, error, duplicate"},
            {"name": "Radon", "version": "6.0.1", "purpose": "Cyclomatic complexity, SLOC"},
        ],
        "warnings": [_diagnostic(row) for row in WARNINGS],
        "errors": [
            {
                "code": "F821 / E0602",
                "count": 1,
                "description": "customer_name анықталмаған; орындалса NameError болады",
                "severity": "High",
            }
        ],
        "code_smells": [
            "Long Method / God Function",
            "Primitive Obsession",
            "Magic Numbers",
            "Mutable Default Argument",
            "Exception Swallowing",
            "Dead Code",
        ],
        "duplicate_evidence": (
            "Pylint R0801 екі файлдағы normalize_items блоктарын duplicate деп тапты. "
            "Түзетуде логика ортақ calculate_subtotal() функциясына шығарылды."
        ),
        "complexity": [
            {
                "stage": "Бастапқы",
                "block": "calculate_order",
                "max_cc": "11 (C)",
                "average": "4.25 (A)",
            },
            {
                "stage": "Түзетілген",
                "block": "_validate_item / calculate_subtotal",
                "max_cc": "4 (A)",
                "average": "2.00 (A)",
            },
        ],
        "security_issues": [
            _diagnostic(("S307", 1, "eval(): arbitrary code execution", "Critical")),
            _diagnostic(("S602", 1, "shell=True: command injection", "Critical")),
            _diagnostic(("S105", 1, "Hardcoded admin password", "High")),
        ],
        "checklist": [
            "PEP 8 және import order сақталған",
            "Public API-де type hint және docstring бар",
            "Input validation boundary мәндерді қамтиды",
            "Ақша Decimal арқылы есептеледі",
            "Secret, eval және shell command жоқ",
            "Exception нақты және мағыналы",
            "Функциялардың міндеттері бөлінген",
            "Duplicate code жоқ",
            "Cyclomatic complexity threshold-тан аспайды",
            "Positive, negative және boundary тесттері бар",
            "Ruff, Pylint және тесттер Quality Gate-тен өтеді",
        ],
        "deficiencies": [
            {
                "id": item_id,
                "problem": problem,
                "severity": severity,
                "detection": detection,
                "fix": fix,
            }
            for item_id, problem, severity, detection, fix in DEFICIENCIES
        ],
        "metrics": [
            {"metric": "Ruff issue", "before": "11", "after": "0", "change": "−11"},
            {"metric": "Pylint message", "before": "10", "after": "0", "change": "−10"},
            {"metric": "Pylint score", "before": "7.41/10", "after": "10.00/10", "change": "+2.59"},
            {"metric": "Pylint Error", "before": "1", "after": "0", "change": "−1"},
            {"metric": "Security issue", "before": "3", "after": "0", "change": "−3"},
            {"metric": "Duplicate block", "before": "1", "after": "0", "change": "−1"},
            {"metric": "Max complexity", "before": "11 (C)", "after": "4 (A)", "change": "−7"},
            {"metric": "Average complexity", "before": "4.25", "after": "2.00", "change": "−2.25"},
            {"metric": "Source SLOC", "before": "54", "after": "72", "change": "+18"},
            {"metric": "Автоматты тесттер", "before": "жоқ", "after": "14/14", "change": "+14"},
        ],
        "quality_gate": [
            {"condition": "Ruff", "threshold": "0 issue", "result": "0", "status": "PASS"},
            {"condition": "Pylint", "threshold": "≥ 9.0/10", "result": "10.00", "status": "PASS"},
            {"condition": "Security", "threshold": "0 issue", "result": "0", "status": "PASS"},
            {
                "condition": "Duplicate code",
                "threshold": "0 block",
                "result": "0",
                "status": "PASS",
            },
            {"condition": "Max complexity", "threshold": "≤ 10", "result": "4", "status": "PASS"},
            {"condition": "Tests", "threshold": "100% pass", "result": "14/14", "status": "PASS"},
        ],
        "tasks": [
            {"id": task_id, "title": title, "evidence": evidence, "status": "done"}
            for task_id, title, evidence in TASKS
        ],
        "conclusion": (
            "11 Ruff issue және 10 Pylint message жойылды, max complexity 11-ден "
            "4-ке түсті, Pylint 10.00/10 болды, 14 тест өтті. Quality Gate — PASSED."
        ),
    }
