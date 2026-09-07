import uuid
import requests


def code(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_coupon(server, **changes):
    coupon = {
        "code": code("V2"),
        "type": "percentage",
        "value": 20,
        "validFrom": "2026-09-01",
        "validUntil": "2026-09-30",
        "minimumAmount": 0,
        "categoryIds": []
    }

    coupon.update(changes)

    response = requests.post(
        f"{server}/coupons",
        json=coupon
    )

    assert response.status_code in (200, 201)

    return coupon


def add_product(server, user_id, product_id=1):
    response = requests.post(
        f"{server}/cart/{user_id}/items",
        json={
            "productId": product_id,
            "quantity": 1
        }
    )

    assert response.status_code in (200, 201)


def checkout(server, user_id, coupon_code):
    return requests.post(
        f"{server}/checkout/{user_id}",
        json={"couponCode": coupon_code}
    )


def use_coupon(server, user_id, coupon_code):
    add_product(server, user_id)
    return checkout(server, user_id, coupon_code)


def test_v2_01_reject_second_use_same_day(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    first = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )
    assert first.status_code in (200, 201)

    add_product(urbanwear_server, 1)

    second = checkout(
        urbanwear_server, 1, coupon["code"]
    )

    assert second.status_code >= 400


def test_v2_02_allow_second_use_next_day(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    first = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )
    assert first.status_code in (200, 201)

    urbanwear_server.restart(
        "2026-09-11T12:00:00.000Z"
    )

    second = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert second.status_code in (200, 201)


def test_v2_03_allow_third_use_third_day(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    assert use_coupon(
        urbanwear_server, 1, coupon["code"]
    ).status_code in (200, 201)

    urbanwear_server.restart(
        "2026-09-11T12:00:00.000Z"
    )

    assert use_coupon(
        urbanwear_server, 1, coupon["code"]
    ).status_code in (200, 201)

    urbanwear_server.restart(
        "2026-09-12T12:00:00.000Z"
    )

    third = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert third.status_code in (200, 201)


def test_v2_04_reject_fourth_use(urbanwear_server):
    coupon = create_coupon(urbanwear_server)

    for day in [10, 11, 12]:
        if day != 10:
            urbanwear_server.restart(
                f"2026-09-{day:02d}T12:00:00.000Z"
            )

        response = use_coupon(
            urbanwear_server, 1, coupon["code"]
        )

        assert response.status_code in (200, 201)

    urbanwear_server.restart(
        "2026-09-13T12:00:00.000Z"
    )

    fourth = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert fourth.status_code >= 400


def test_v2_05_usage_is_independent_between_users(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    first_user = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    second_user = use_coupon(
        urbanwear_server, 2, coupon["code"]
    )

    assert first_user.status_code in (200, 201)
    assert second_user.status_code in (200, 201)


def test_v2_06_failed_attempt_does_not_count_total(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        minimumAmount=100
    )

    # 89.99: intento inválido.
    add_product(urbanwear_server, 1)

    failed = checkout(
        urbanwear_server, 1, coupon["code"]
    )

    assert failed.status_code >= 400

    # Sumamos otro producto al carrito.
    add_product(
        urbanwear_server, 1, product_id=2
    )

    successful = checkout(
        urbanwear_server, 1, coupon["code"]
    )

    assert successful.status_code in (200, 201)


def test_v2_07_failed_attempt_does_not_block_same_day(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        minimumAmount=100
    )

    add_product(urbanwear_server, 1)

    failed = checkout(
        urbanwear_server, 1, coupon["code"]
    )

    assert failed.status_code >= 400

    # Sigue siendo el mismo día.
    add_product(
        urbanwear_server, 1, product_id=2
    )

    successful = checkout(
        urbanwear_server, 1, coupon["code"]
    )

    assert successful.status_code in (200, 201)