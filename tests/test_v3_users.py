import uuid
import requests


def code(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_coupon(server, **changes):
    coupon = {
        "code": code("V3"),
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


def use_coupon(server, user_id, coupon_code, product_id=1):
    add_product(server, user_id, product_id)

    return checkout(
        server,
        user_id,
        coupon_code
    )


def test_v3_01_coupon_without_user_restriction(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    response = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert response.status_code in (200, 201)


def test_v3_02_allowed_user_can_use_coupon(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[1]
    )

    response = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert response.status_code in (200, 201)


def test_v3_03_disallowed_user_is_rejected(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[2]
    )

    response = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert response.status_code >= 400


def test_v3_04_rejected_user_does_not_consume_use(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[2]
    )

    rejected = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert rejected.status_code >= 400

    allowed = use_coupon(
        urbanwear_server, 2, coupon["code"]
    )

    assert allowed.status_code in (200, 201)


def test_v3_05_allowed_user_must_respect_validity(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[1],
        validFrom="2026-09-11",
        validUntil="2026-09-30"
    )

    response = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert response.status_code >= 400


def test_v3_06_allowed_user_must_respect_minimum(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[1],
        minimumAmount=100
    )

    # Producto 1 cuesta 89.99
    response = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert response.status_code >= 400


def test_v3_07_allowed_user_must_respect_categories(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[1],
        categoryIds=[2]
    )

    # Producto 1 pertenece a categoría 1.
    response = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1
    )

    assert response.status_code >= 400


def test_v3_08_allowed_user_still_has_daily_limit(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[1]
    )

    first = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert first.status_code in (200, 201)

    second = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert second.status_code >= 400


def test_v3_09_allowed_user_still_has_total_limit(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[1]
    )

    for day in [10, 11, 12]:
        if day != 10:
            urbanwear_server.restart(
                f"2026-09-{day:02d}T12:00:00.000Z"
            )

        result = use_coupon(
            urbanwear_server, 1, coupon["code"]
        )

        assert result.status_code in (200, 201)

    urbanwear_server.restart(
        "2026-09-13T12:00:00.000Z"
    )

    fourth = use_coupon(
        urbanwear_server, 1, coupon["code"]
    )

    assert fourth.status_code >= 400