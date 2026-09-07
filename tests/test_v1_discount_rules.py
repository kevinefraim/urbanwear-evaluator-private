import uuid
import requests
import pytest


def code(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_coupon(server, **changes):
    coupon = {
        "code": code("COUPON"),
        "type": "percentage",
        "value": 20,
        "validFrom": "2026-09-01",
        "validUntil": "2026-09-30",
        "minimumAmount": 0,
        "categoryIds": []
    }

    coupon.update(changes)

    response = requests.post(f"{server}/coupons", json=coupon)
    assert response.status_code in (200, 201)

    return coupon


def add_product(server, user_id, product_id, quantity=1):
    response = requests.post(
        f"{server}/cart/{user_id}/items",
        json={
            "productId": product_id,
            "quantity": quantity
        }
    )

    assert response.status_code in (200, 201)


def checkout(server, user_id, coupon_code):
    return requests.post(
        f"{server}/checkout/{user_id}",
        json={"couponCode": coupon_code}
    )


def test_v1_06_percentage_discount(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="percentage",
        value=20
    )

    add_product(urbanwear_server, 1, 1)  # 89.99

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["subtotal"] == pytest.approx(89.99)
    assert data["discount"] == pytest.approx(17.998)
    assert data["total"] == pytest.approx(71.992)


def test_v1_07_percentage_100_percent(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="percentage",
        value=100
    )

    add_product(urbanwear_server, 1, 1)

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)
    assert response.json()["total"] == pytest.approx(0)


def test_v1_08_reject_invalid_percentage(urbanwear_server):
    coupon = {
        "code": code("INVALID"),
        "type": "percentage",
        "value": 101,
        "validFrom": "2026-09-01",
        "validUntil": "2026-09-30",
        "minimumAmount": 0,
        "categoryIds": []
    }

    response = requests.post(
        f"{urbanwear_server}/coupons",
        json=coupon
    )

    assert response.status_code >= 400


def test_v1_09_fixed_discount(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="fixed",
        value=20
    )

    add_product(urbanwear_server, 1, 1)

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["subtotal"] == pytest.approx(89.99)
    assert data["discount"] == pytest.approx(20)
    assert data["total"] == pytest.approx(69.99)


def test_v1_10_fixed_discount_never_negative(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="fixed",
        value=500
    )

    add_product(urbanwear_server, 1, 1)

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)
    assert response.json()["total"] == pytest.approx(0)


def test_v1_16_reject_below_minimum(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        minimumAmount=100
    )

    add_product(urbanwear_server, 1, 1)  # 89.99

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code >= 400


def test_v1_17_accept_exact_minimum(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        minimumAmount=89.99
    )

    add_product(urbanwear_server, 1, 1)

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)

def test_v1_18_minimum_is_checked_before_discount(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="percentage",
        value=50,
        minimumAmount=80
    )

    # Subtotal = 89.99, por lo tanto supera el mínimo de 80.
    # Después del descuento quedaría en 44.995.
    # Esto comprueba que el mínimo se evalúa ANTES del descuento.
    add_product(urbanwear_server, 1, 1)

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)


def test_v1_19_discount_on_allowed_category(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="percentage",
        value=20,
        categoryIds=[1]
    )

    # Street Runner pertenece a categoría 1.
    add_product(urbanwear_server, 1, 1)

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["subtotal"] == pytest.approx(89.99)
    assert data["discount"] == pytest.approx(17.998)
    assert data["total"] == pytest.approx(71.992)

def test_v1_20_discount_only_allowed_categories(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="percentage",
        value=20,
        categoryIds=[1]
    )

    # Categoría 1
    add_product(urbanwear_server, 1, 1)  # 89.99

    # Categoría 2
    add_product(urbanwear_server, 1, 4)  # 129.99

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["subtotal"] == pytest.approx(219.98)

    # Solo 89.99 recibe 20 %
    assert data["discount"] == pytest.approx(17.998)
    assert data["total"] == pytest.approx(201.982)


def test_v1_21_reject_when_no_product_is_eligible(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        categoryIds=[1]
    )

    # Urban Boot pertenece a categoría 2
    add_product(urbanwear_server, 1, 4)

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code >= 400


def test_v1_22_coupon_without_category_restriction(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        type="percentage",
        value=10,
        categoryIds=[]
    )

    add_product(urbanwear_server, 1, 1)  # categoría 1
    add_product(urbanwear_server, 1, 4)  # categoría 2

    response = checkout(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["subtotal"] == pytest.approx(219.98)
    assert data["discount"] == pytest.approx(21.998)