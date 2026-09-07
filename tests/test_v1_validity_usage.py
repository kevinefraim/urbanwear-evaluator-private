import uuid
import requests


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


def add_product(server, user_id, product_id=1):
    response = requests.post(
        f"{server}/cart/{user_id}/items",
        json={"productId": product_id, "quantity": 1}
    )

    assert response.status_code in (200, 201)


def checkout(server, user_id, coupon_code):
    return requests.post(
        f"{server}/checkout/{user_id}",
        json={"couponCode": coupon_code}
    )


def test_v1_11_coupon_inside_validity_period(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    add_product(urbanwear_server, 1)

    response = checkout(urbanwear_server, 1, coupon["code"])

    assert response.status_code in (200, 201)


def test_v1_12_reject_coupon_not_started(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        validFrom="2026-09-11",
        validUntil="2026-09-30"
    )

    add_product(urbanwear_server, 1)

    response = checkout(urbanwear_server, 1, coupon["code"])

    assert response.status_code >= 400


def test_v1_13_reject_expired_coupon(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        validFrom="2026-08-01",
        validUntil="2026-09-09"
    )

    add_product(urbanwear_server, 1)

    response = checkout(urbanwear_server, 1, coupon["code"])

    assert response.status_code >= 400


def test_v1_14_start_date_is_inclusive(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        validFrom="2026-09-10",
        validUntil="2026-09-20"
    )

    add_product(urbanwear_server, 1)

    response = checkout(urbanwear_server, 1, coupon["code"])

    assert response.status_code in (200, 201)


def test_v1_15_end_date_is_inclusive(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        validFrom="2026-09-01",
        validUntil="2026-09-10"
    )

    add_product(urbanwear_server, 1)

    response = checkout(urbanwear_server, 1, coupon["code"])

    assert response.status_code in (200, 201)


def test_v1_23_first_use_is_allowed(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    add_product(urbanwear_server, 1)

    response = checkout(urbanwear_server, 1, coupon["code"])

    assert response.status_code in (200, 201)


def test_v1_24_second_use_same_user_is_rejected(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    add_product(urbanwear_server, 1)
    first = checkout(urbanwear_server, 1, coupon["code"])

    assert first.status_code in (200, 201)

    add_product(urbanwear_server, 1)
    second = checkout(urbanwear_server, 1, coupon["code"])

    assert second.status_code >= 400


def test_v1_25_same_coupon_can_be_used_by_another_user(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    add_product(urbanwear_server, 1)
    first = checkout(urbanwear_server, 1, coupon["code"])

    assert first.status_code in (200, 201)

    add_product(urbanwear_server, 2)
    second = checkout(urbanwear_server, 2, coupon["code"])

    assert second.status_code in (200, 201)


def test_v1_26_failed_checkout_does_not_consume_use(urbanwear_server):
    coupon = create_coupon(
        urbanwear_server,
        minimumAmount=100
    )

    # 89.99: no alcanza el mínimo
    add_product(urbanwear_server, 1, 1)

    failed = checkout(urbanwear_server, 1, coupon["code"])

    assert failed.status_code >= 400

    # Agregamos otro producto y ahora supera el mínimo.
    add_product(urbanwear_server, 1, 2)

    successful = checkout(urbanwear_server, 1, coupon["code"])

    assert successful.status_code in (200, 201)