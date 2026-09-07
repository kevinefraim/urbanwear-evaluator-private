import requests
import pytest


def add_product(server, user_id, product_id=1, quantity=1):
    response = requests.post(
        f"{server}/cart/{user_id}/items",
        json={
            "productId": product_id,
            "quantity": quantity
        }
    )

    assert response.status_code in (200, 201)


def test_v1_27_checkout_without_coupon_still_works(urbanwear_server):
    add_product(urbanwear_server, 1, 1)

    response = requests.post(
        f"{urbanwear_server}/checkout/1",
        json={}
    )

    assert response.status_code in (200, 201)


def test_v1_28_checkout_without_coupon_keeps_subtotal_equal_total(urbanwear_server):
    add_product(urbanwear_server, 1, 1, 2)

    response = requests.post(
        f"{urbanwear_server}/checkout/1",
        json={}
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["subtotal"] == pytest.approx(179.98)
    assert data["total"] == pytest.approx(179.98)


def test_v1_29_successful_checkout_creates_order(urbanwear_server):
    add_product(urbanwear_server, 1, 1)

    response = requests.post(
        f"{urbanwear_server}/checkout/1",
        json={}
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert "id" in data
    assert data["userId"] == 1


def test_v1_30_successful_checkout_clears_cart(urbanwear_server):
    add_product(urbanwear_server, 1, 1)

    checkout = requests.post(
        f"{urbanwear_server}/checkout/1",
        json={}
    )

    assert checkout.status_code in (200, 201)

    cart = requests.get(
        f"{urbanwear_server}/cart/1"
    )

    assert cart.status_code == 200
    assert cart.json()["items"] == []