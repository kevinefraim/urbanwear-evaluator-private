import uuid
import requests


def unique_code(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def valid_coupon(code):
    return {
        "code": code,
        "type": "percentage",
        "value": 20,
        "validFrom": "2026-09-01",
        "validUntil": "2026-09-30",
        "minimumAmount": 50,
        "categoryIds": []
    }


def test_v1_01_create_percentage_coupon(urbanwear_server):
    coupon = valid_coupon(unique_code("PERCENT"))

    response = requests.post(
        f"{urbanwear_server}/coupons",
        json=coupon
    )

    assert response.status_code in (200, 201)


def test_v1_02_create_fixed_coupon(urbanwear_server):
    coupon = valid_coupon(unique_code("FIXED"))
    coupon["type"] = "fixed"
    coupon["value"] = 20

    response = requests.post(
        f"{urbanwear_server}/coupons",
        json=coupon
    )

    assert response.status_code in (200, 201)


def test_v1_03_reject_duplicate_code(urbanwear_server):
    code = unique_code("DUPLICATE")
    coupon = valid_coupon(code)

    first = requests.post(
        f"{urbanwear_server}/coupons",
        json=coupon
    )

    second = requests.post(
        f"{urbanwear_server}/coupons",
        json=coupon
    )

    assert first.status_code in (200, 201)
    assert second.status_code >= 400


def test_v1_04_get_existing_coupon(urbanwear_server):
    code = unique_code("GET")
    coupon = valid_coupon(code)

    create_response = requests.post(
        f"{urbanwear_server}/coupons",
        json=coupon
    )

    assert create_response.status_code in (200, 201)

    response = requests.get(
        f"{urbanwear_server}/coupons/{code}"
    )

    assert response.status_code == 200
    assert response.json()["code"] == code


def test_v1_05_get_nonexistent_coupon(urbanwear_server):
    response = requests.get(
        f"{urbanwear_server}/coupons/DOES-NOT-EXIST"
    )

    assert response.status_code == 404