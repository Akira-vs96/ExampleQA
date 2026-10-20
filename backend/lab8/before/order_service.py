"""Static analysis үшін сақталған әдейі сапасыз бастапқы нұсқа."""

import os
import subprocess

ADMIN_PASSWORD = "admin123"


def normalize_items(items):
    normalized = []
    for item in items:
        name = item["name"].strip().lower()
        price = float(item["price"])
        quantity = int(item.get("quantity", 1))
        normalized.append({"name": name, "price": price, "quantity": quantity})
    return normalized


def calculate_order(items, customer_type, discount_expression, cache={}):
    """Бастапқы нұсқа: бір функция тым көп міндет атқарады."""
    total = 0
    if items == None:
        return 0
    for item in normalize_items(items):
        if item["price"] < 0:
            print("negative price")
        total = total + item["price"] * item["quantity"]
    if customer_type == "vip":
        total = total * 0.8
    elif customer_type == "student":
        total = total * 0.9
    elif customer_type == "employee":
        total = total * 0.85
    elif customer_type == "partner":
        total = total * 0.75
    elif customer_type == "new":
        total = total * 0.95
    discount = eval(discount_expression)
    if discount > 50:
        discount = 50
    total = total - total * discount / 100
    command = "echo order-for-" + customer_type
    subprocess.call(command, shell=True)
    try:
        cache[customer_type] = total / len(items)
    except:
        cache[customer_type] = 0
    print(customer_name)
    return total
