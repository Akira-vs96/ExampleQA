"""Generate the importable Postman collection and the six required test cases."""

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
PRODUCT = {"name": "Mouse", "price": 2500, "stock": 5}
CASES = [
    ("TC01", "Дұрыс", "GET", "/api/products/1", "—", 200, "valid_get"),
    ("TC02", "Қате", "GET", "/api/products/999999", "Жоқ ID", 404, "missing_product"),
    ("TC03", "Қате", "POST", "/api/products", "price=-1", 422, "negative_price"),
    ("TC04", "Қате", "POST", "/api/products", 'price="2500"', 422, "string_price"),
    ("TC05", "Шекаралық", "POST", "/api/products", "price=0", 201, "minimum_price"),
    ("TC06", "Шекаралық", "POST", "/api/products", "price=1000000", 201, "maximum_price"),
]

PRODUCT_CHECKS = [
    'pm.test("Product fields and types", function () {',
    "  const body = pm.response.json();",
    '  pm.expect(body).to.have.all.keys("id", "name", "price", "stock");',
    "  pm.expect(Number.isInteger(body.id) && body.id > 0).to.eql(true);",
    '  pm.expect(body.name).to.be.a("string");',
    "  pm.expect(body.name.length).to.be.within(1, 100);",
    "  pm.expect(Number.isInteger(body.price)).to.eql(true);",
    "  pm.expect(body.price).to.be.within(0, 1000000);",
    "  pm.expect(Number.isInteger(body.stock)).to.eql(true);",
    "  pm.expect(body.stock).to.be.within(0, 1000);",
    "});",
]


def request(
    name: str,
    method: str,
    path: str,
    status: int,
    body: dict | None = None,
    *,
    checks: list[str] | None = None,
    save: str | None = None,
) -> dict:
    scripts = [
        f'pm.test("Status {status}", () => pm.response.to.have.status({status}));'
    ]
    if status == 204:
        scripts.append('pm.test("Empty response", () => pm.expect(pm.response.text()).to.eql(""));')
    else:
        scripts.extend([
            'pm.test("JSON Content-Type", () => {',
            '  pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");',
            "});",
        ])
        if status < 300:
            scripts.extend(PRODUCT_CHECKS)
        else:
            scripts.extend([
                'pm.test("Error detail", () => {',
                '  pm.expect(pm.response.json()).to.have.property("detail");',
                "});",
            ])
    if checks:
        scripts.extend(checks)
    if save:
        scripts.extend([
            f"if (pm.response.code === {status}) {{",
            f'  pm.collectionVariables.set("{save}", pm.response.json().id);',
            "}",
        ])
    item = {
        "name": name,
        "request": {
            "method": method,
            "header": [{"key": "Accept", "value": "application/json"}],
            "url": "{{base_url}}" + path,
        },
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": scripts}}],
    }
    if body is not None:
        item["request"]["header"].append({"key": "Content-Type", "value": "application/json"})
        item["request"]["body"] = {
            "mode": "raw", "raw": json.dumps(body, ensure_ascii=False),
            "options": {"raw": {"language": "json"}},
        }
    return item


def equal_product(expected: dict) -> list[str]:
    return [
        'pm.test("Expected product values", () => {',
        f"  pm.expect(pm.response.json()).to.deep.eql({json.dumps(expected)});",
        "});",
    ]


def generate() -> None:
    normal = {"id": 1, "name": "Keyboard", "price": 5000, "stock": 10}
    core = [
        request("TC01 valid GET", "GET", "/api/products/1", 200, checks=equal_product(normal)),
        request("TC02 missing ID", "GET", "/api/products/999999", 404),
        request("TC03 negative price", "POST", "/api/products", 422,
                PRODUCT | {"price": -1}),
        request("TC04 string price", "POST", "/api/products", 422,
                PRODUCT | {"price": "2500"}),
        request("TC05 minimum price", "POST", "/api/products", 201,
                PRODUCT | {"price": 0}, save="minimum_id", checks=[
                    'pm.test("Minimum is accepted", () => pm.expect(pm.response.json().price)'
                    '.to.eql(0));',
                ]),
        request("TC06 maximum price", "POST", "/api/products", 201,
                PRODUCT | {"price": 1_000_000}, save="maximum_id", checks=[
                    'pm.test("Maximum is accepted", () => pm.expect(pm.response.json().price)'
                    '.to.eql(1000000));',
                ]),
        request("TC05 cleanup", "DELETE", "/api/products/{{minimum_id}}", 204),
        request("TC06 cleanup", "DELETE", "/api/products/{{maximum_id}}", 204),
    ]
    core[0]["event"].insert(0, {
        "listen": "prerequest", "script": {"type": "text/javascript", "exec": [
            '["minimum_id", "maximum_id", "lifecycle_id", "patch_id"].forEach(',
            "  key => pm.collectionVariables.unset(key));",
        ]},
    })
    replacement = {"name": "Monitor", "price": 45000, "stock": 3}
    lifecycle = [
        request("IT01 1 POST", "POST", "/api/products", 201, PRODUCT, save="lifecycle_id"),
        request("IT01 2 GET", "GET", "/api/products/{{lifecycle_id}}", 200, checks=[
            'pm.test("Created values persisted", () => {',
            '  const id = Number(pm.collectionVariables.get("lifecycle_id"));',
            f"  pm.expect(pm.response.json()).to.deep.eql({{id, ...{json.dumps(PRODUCT)}}});",
            "});",
        ]),
        request("IT01 3 PUT", "PUT", "/api/products/{{lifecycle_id}}", 200, replacement),
        request("IT01 4 GET replaced", "GET", "/api/products/{{lifecycle_id}}", 200, checks=[
            'pm.test("Full replacement persisted", () => {',
            '  const id = Number(pm.collectionVariables.get("lifecycle_id"));',
            f"  pm.expect(pm.response.json()).to.deep.eql({{id, ...{json.dumps(replacement)}}});",
            "});",
        ]),
        request("IT01 5 DELETE", "DELETE", "/api/products/{{lifecycle_id}}", 204),
        request("IT01 6 GET deleted", "GET", "/api/products/{{lifecycle_id}}", 404),
    ]
    expected_patch = [
        'pm.test("Only stock changed", () => {',
        '  const id = Number(pm.collectionVariables.get("patch_id"));',
        f"  pm.expect(pm.response.json()).to.deep.eql({{id, ...{json.dumps(PRODUCT)}, stock: 0}});",
        "});",
    ]
    patch_flow = [
        request("IT02 1 POST", "POST", "/api/products", 201, PRODUCT, save="patch_id"),
        request("IT02 2 PATCH", "PATCH", "/api/products/{{patch_id}}", 200,
                {"stock": 0}, checks=expected_patch),
        request("IT02 3 GET", "GET", "/api/products/{{patch_id}}", 200, checks=expected_patch),
        request("IT02 4 invalid PATCH", "PATCH", "/api/products/{{patch_id}}", 422,
                {"stock": -1}),
        request("IT02 5 GET unchanged", "GET", "/api/products/{{patch_id}}", 200,
                checks=expected_patch),
        request("IT02 6 DELETE", "DELETE", "/api/products/{{patch_id}}", 204),
        request("IT02 7 GET deleted", "GET", "/api/products/{{patch_id}}", 404),
    ]
    collection = {
        "info": {
            "name": "СРО 9 — REST API", "schema": SCHEMA,
            "description": (
                "6 test cases and 2 stateful integration scenarios. Run folders in order."
            ),
        },
        "variable": [{"key": "base_url", "value": "http://127.0.0.1:8009", "type": "string"}],
        "item": [
            {"name": "1 Six required cases", "item": core},
            {"name": "2 IT01 CRUD lifecycle", "item": lifecycle},
            {"name": "3 IT02 PATCH and validation", "item": patch_flow},
        ],
    }
    environment = {
        "name": "СРО 9 — localhost",
        "values": [{"key": "base_url", "value": "http://127.0.0.1:8009", "enabled": True}],
        "_postman_variable_scope": "environment",
    }
    for filename, data in [
        ("SRO9.postman_collection.json", collection),
        ("SRO9.postman_environment.json", environment),
    ]:
        (HERE / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    with (HERE / "test_cases.csv").open("w", newline="", encoding="utf-8-sig") as output:
        writer = csv.writer(output)
        writer.writerow(["ID", "Түрі", "Әдіс", "URL", "Кіріс", "Күтілетін HTTP", "pytest"])
        for case_id, kind, method, path, data, status, test in CASES:
            writer.writerow([case_id, kind, method, path, data, status,
                             f"test_{case_id.lower()}_{test}"])


if __name__ == "__main__":
    generate()
