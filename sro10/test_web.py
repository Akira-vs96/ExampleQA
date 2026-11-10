"""Positive, negative, boundary, interface and controlled network scenarios."""

import re

import pytest
from playwright.sync_api import expect


def search(page, query):
    page.get_by_label("Тауарды іздеу").fill(query)
    page.get_by_role("button", name="Іздеу", exact=True).click()


def account(page, credentials, button):
    page.get_by_label("Логин", exact=True).fill(credentials["username"])
    page.get_by_label("Пароль", exact=True).fill(credentials["password"])
    page.get_by_role("button", name=button, exact=True).click()


def test_web01_open_page(web_page):
    response = web_page.goto("/shop.html")
    assert response.status == 200
    expect(web_page).to_have_title("QA Shop · DebugLab KZ")
    expect(web_page.get_by_role("heading", name="QA Shop", exact=True)).to_be_visible()


def test_web01_main_elements_visible(web_page):
    for heading in ("Жеке кабинет", "Тауарлар", "Тапсырысты есептеу"):
        expect(web_page.get_by_role("heading", name=heading, exact=True)).to_be_visible()
    expect(web_page.get_by_label("Логин", exact=True)).to_be_visible()
    expect(web_page.get_by_label("Тауарды іздеу")).to_be_visible()
    expect(web_page.locator("#products li")).to_have_count(3)


def test_web02_registration_and_login(web_page, web_credentials, record_property):
    with web_page.expect_response("**/api/shop/register") as pending:
        account(web_page, web_credentials, "Тіркелу")
    assert pending.value.status == 201
    expect(web_page.locator("#status")).to_have_text("Тіркелу сәтті. Енді жүйеге кіріңіз.")
    with web_page.expect_response("**/api/shop/login") as pending:
        account(web_page, web_credentials, "Кіру")
    assert pending.value.status == 200
    expect(web_page.locator("#status")).to_have_text(
        f"Қош келдіңіз, {web_credentials['username']}!"
    )
    response = web_page.request.get("/api/shop/me")
    assert response.status == 200
    assert response.json()["username"] == web_credentials["username"]
    record_property("HTTP", "POST register 201; POST login 200; GET me 200")


def test_web03_wrong_password(web_page, web_credentials):
    assert web_page.request.post("/api/shop/register", data=web_credentials).status == 201
    with web_page.expect_response("**/api/shop/login") as pending:
        account(web_page, {**web_credentials, "password": "Wrong_pass_2026"}, "Кіру")
    assert pending.value.status == 401
    expect(web_page.locator("#status")).to_have_text("Логин немесе пароль қате.")
    assert web_page.request.get("/api/shop/me").status == 401


def test_web04_empty_username(web_page):
    account(web_page, {"username": "", "password": "Sro10_Test_2026"}, "Кіру")
    assert web_page.get_by_label("Логин", exact=True).evaluate(
        "el => el.validity.valueMissing && !el.checkValidity()"
    )
    expect(web_page.locator("#status")).to_be_empty()


def test_web05_short_password(web_page, web_credentials):
    account(web_page, {**web_credentials, "password": "1234567"}, "Тіркелу")
    assert web_page.get_by_label("Пароль", exact=True).evaluate(
        "el => el.validity.tooShort && !el.checkValidity()"
    )
    expect(web_page.locator("#status")).to_be_empty()


def test_web06_minimum_credentials(web_page):
    with web_page.expect_response("**/api/shop/register") as pending:
        account(web_page, {"username": "min", "password": "12345678"}, "Тіркелу")
    assert pending.value.status == 201
    expect(web_page.locator("#status")).to_contain_text("Тіркелу сәтті")


def test_web07_case_insensitive_search(web_page):
    search(web_page, "KEYBOARD")
    expect(web_page.locator("#products li")).to_have_count(1)
    expect(web_page.locator("#products")).to_have_text("Keyboard · 5000.00 ₸")


def test_web08_no_search_results(web_page):
    search(web_page, "nonexistent_sro10_999")
    expect(web_page.locator("#products")).to_have_text("Тауар табылмады.")


def test_web09_empty_search(web_page):
    search(web_page, "Mouse")
    expect(web_page.locator("#products li")).to_have_count(1)
    search(web_page, "")
    expect(web_page.locator("#products li")).to_have_count(3)


@pytest.mark.parametrize("width", [375, 768, 1440])
def test_web10_responsive_layout(web_page, width):
    web_page.set_viewport_size({"width": width, "height": 900})
    assert web_page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    for field in ("Логин", "Пароль", "Тауарды іздеу", "Саны", "Жеңілдік %"):
        control = web_page.get_by_label(field, exact=True)
        expect(control).to_be_visible()
        box = control.bounding_box()
        assert box and box["x"] >= 0 and box["x"] + box["width"] <= width


def test_web11_keyboard_navigation(web_page):
    web_page.get_by_label("Логин", exact=True).focus()
    for element in ("username", "password", "login", "register", "logout", "query"):
        expect(web_page.locator(f"#{element}")).to_be_focused()
        web_page.keyboard.press("Tab")


def test_web12_unauthenticated_access(web_page):
    assert web_page.request.get("/api/shop/me").status == 401
    with web_page.expect_response("**/api/shop/quote") as pending:
        web_page.get_by_role("button", name="Есептеу", exact=True).click()
    assert pending.value.status == 401
    expect(web_page.locator("#status")).to_have_text("Алдымен жүйеге кіріңіз.")
    expect(web_page.locator("#quote-result")).to_be_empty()


@pytest.mark.xfail(
    strict=True, raises=AssertionError,
    reason="BUG-10-01: a network failure exposes the browser's English TypeError",
)
def test_web13_network_error_message(web_page, record_property):
    expect(web_page.locator("#products li")).to_have_count(3)
    web_page.route("**/api/shop/products?*", lambda route: route.abort("internetdisconnected"))
    search(web_page, "Mouse")
    expect(web_page.locator("#status")).not_to_be_empty()
    record_property("actual", web_page.locator("#status").inner_text())
    expect(web_page.locator("#status")).to_have_text(
        "Желіге қосылу мүмкін болмады. Интернет байланысын тексеріп, қайталап көріңіз.",
        timeout=1000,
    )


def test_web14_order_quote(web_signed_page, record_property):
    page = web_signed_page
    with page.expect_response("**/api/shop/quote") as pending:
        page.get_by_role("button", name="Есептеу", exact=True).click()
    response = pending.value
    assert response.status == 200
    assert response.json()["subtotal"] == "10000.00"
    assert response.json()["discounted"] == "8000.00"
    assert response.json()["shipping"] == "1000.00"
    assert response.json()["total"] == "9000.00"
    record_property("quote_response", response.text())
    expect(page.locator("#quote-result")).to_have_text(
        "Барлығы: 9000.00 ₸ · жеткізу: 1000.00 ₸"
    )


@pytest.mark.parametrize("quantity,valid,total", [
    (0, False, None), (1, True, "5000.00"),
    (100, True, "400000.00"), (101, False, None),
])
def test_web15_quantity_boundaries(web_signed_page, quantity, valid, total):
    page = web_signed_page
    field = page.get_by_label("Саны", exact=True)
    field.fill(str(quantity))
    assert field.evaluate("el => el.checkValidity()") is valid
    if valid:
        with page.expect_response("**/api/shop/quote") as pending:
            page.get_by_role("button", name="Есептеу", exact=True).click()
        assert pending.value.status == 200
        assert pending.value.json()["total"] == total
        expect(page.locator("#quote-result")).to_contain_text(f"Барлығы: {total}")
    else:
        page.get_by_role("button", name="Есептеу", exact=True).click()
        expect(page.locator("#quote-result")).to_be_empty()


def test_web16_logout_revokes_session(web_signed_page):
    page = web_signed_page
    page.get_by_role("button", name="Есептеу", exact=True).click()
    expect(page.locator("#quote-result")).not_to_be_empty()
    with page.expect_response("**/api/shop/session") as pending:
        page.get_by_role("button", name="Шығу", exact=True).click()
    assert pending.value.status == 204
    expect(page.locator("#status")).to_have_text("Жүйеден шықтыңыз.")
    expect(page.locator("#quote-result")).to_be_empty()
    expect(page.get_by_label("Пароль", exact=True)).to_have_value("")
    assert page.request.get("/api/shop/me").status == 401


@pytest.mark.parametrize("length,status", [(80, 200), (81, 422)])
def test_web17_search_length_boundary(web_page, length, status):
    expect(web_page.get_by_label("Тауарды іздеу")).to_have_attribute("maxlength", "80")
    response = web_page.request.get("/api/shop/products", params={"q": "a" * length})
    assert response.status == status
    if status == 422:
        assert response.json()["detail"][0]["loc"] == ["query", "q"]


@pytest.mark.xfail(
    strict=True, raises=AssertionError,
    reason="BUG-10-02: a delayed earlier search overwrites the latest search result",
)
def test_web18_latest_search_wins(web_page, record_property):
    expect(web_page.locator("#products li")).to_have_count(3)
    held = []
    web_page.route("**/api/shop/products?q=Keyboard", lambda route: held.append(route))
    with web_page.expect_request("**/api/shop/products?q=Keyboard"):
        search(web_page, "Keyboard")
    search(web_page, "Mouse")
    expect(web_page.locator("#products")).to_have_text("Mouse · 2500.00 ₸")
    if len(held) != 1:
        raise RuntimeError("The controlled request was not intercepted")
    with web_page.expect_event(
        "requestfinished", predicate=lambda request: request.url.endswith("q=Keyboard")
    ):
        held[0].continue_()
    # Let fetch's DOM update reach the next rendered frame before checking the result.
    web_page.evaluate(
        "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
    )
    record_property("actual", web_page.locator("#products").inner_text())
    expect(web_page.get_by_label("Тауарды іздеу")).to_have_value("Mouse")
    expect(web_page.locator("#products")).to_have_text("Mouse · 2500.00 ₸", timeout=1000)


def test_web19_navigation(web_page):
    web_page.get_by_role("link", name="← Зертханалар").click()
    expect(web_page).to_have_url(re.compile(r"/index\.html$"))
    expect(web_page).to_have_title(re.compile("DebugLab KZ"))


@pytest.mark.parametrize("percent,status,total", [
    (-1, 422, None), (0, 200, "10000.00"),
    (100, 200, "1000.00"), (101, 422, None),
])
def test_web20_discount_boundaries(web_signed_page, percent, status, total):
    response = web_signed_page.request.post("/api/shop/quote", data={
        "items": [{"product_id": 1, "quantity": 2}], "percent": percent,
    })
    assert response.status == status
    if status == 200:
        assert response.json()["total"] == total
    else:
        assert response.json()["detail"][0]["loc"] == ["body", "percent"]
