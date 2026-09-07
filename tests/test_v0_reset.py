import requests


def test_seed_starts_with_expected_products(urbanwear_server):
    response = requests.get(f"{urbanwear_server}/products")

    assert response.status_code == 200
    assert len(response.json()) == 5


def test_cart_starts_empty(urbanwear_server):
    response = requests.get(f"{urbanwear_server}/cart/1")

    assert response.status_code == 200
    assert response.json()["items"] == []