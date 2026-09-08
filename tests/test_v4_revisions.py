import uuid

import pytest
import requests


def code(prefix="V4"):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def assert_money(actual, expected):
    assert actual == pytest.approx(expected, abs=0.01)


def create_coupon(server, **changes):
    coupon = {
        "code": code(),
        "type": "percentage",
        "value": 20,
        "validFrom": "2026-09-01",
        "validUntil": "2026-09-30",
        "minimumAmount": 0,
        "categoryIds": [],
        "allowedUserIds": []
    }

    coupon.update(changes)

    response = requests.post(
        f"{server}/coupons",
        json=coupon
    )

    assert response.status_code in (200, 201)

    return coupon


def patch_coupon(server, coupon_code, **changes):
    return requests.patch(
        f"{server}/coupons/{coupon_code}",
        json=changes
    )


def add_product(
    server,
    user_id,
    product_id=1,
    quantity=1
):
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


def use_coupon(
    server,
    user_id,
    coupon_code,
    product_id=1
):
    add_product(
        server,
        user_id,
        product_id
    )

    return checkout(
        server,
        user_id,
        coupon_code
    )


# ---------------------------------------------------------
# V4-01
# PATCH parcial conserva campos anteriores
# ---------------------------------------------------------

def test_v4_01_partial_patch_preserves_previous_fields(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        minimumAmount=100
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=30
    )

    assert response.status_code in (200, 204)

    # Si minimumAmount fue preservado, 89.99 sigue sin alcanzar.
    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1
    )

    assert result.status_code >= 400


# ---------------------------------------------------------
# V4-02
# El código es inmutable
# ---------------------------------------------------------

def test_v4_02_coupon_code_cannot_be_modified(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        code="OTHER-CODE"
    )

    assert response.status_code >= 400


# ---------------------------------------------------------
# V4-03
# Cambio inmediato del descuento
# ---------------------------------------------------------

def test_v4_03_immediate_discount_change(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        value=20
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=50
    )

    assert response.status_code in (200, 204)

    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1
    )

    assert result.status_code in (200, 201)

    data = result.json()

    # Street Runner = 89.99
    assert_money(data["subtotal"], 89.99)
    assert_money(data["discount"], 44.995)
    assert_money(data["total"], 44.995)


# ---------------------------------------------------------
# V4-04
# Cambio inmediato del monto mínimo
# ---------------------------------------------------------

def test_v4_04_immediate_minimum_change(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        minimumAmount=0
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        minimumAmount=100
    )

    assert response.status_code in (200, 204)

    # 89.99 queda por debajo del nuevo mínimo.
    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1
    )

    assert result.status_code >= 400


# ---------------------------------------------------------
# V4-05
# Cambio de categorías
# ---------------------------------------------------------

def test_v4_05_immediate_category_change(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        categoryIds=[]
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        categoryIds=[2]
    )

    assert response.status_code in (200, 204)

    # Producto 1 pertenece a categoría 1.
    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1
    )

    assert result.status_code >= 400


# ---------------------------------------------------------
# V4-06
# Cambio de usuarios autorizados
# ---------------------------------------------------------

def test_v4_06_immediate_allowed_users_change(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        allowedUserIds=[]
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        allowedUserIds=[2]
    )

    assert response.status_code in (200, 204)

    rejected = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert rejected.status_code >= 400

    allowed = use_coupon(
        urbanwear_server,
        2,
        coupon["code"]
    )

    assert allowed.status_code in (200, 201)


# ---------------------------------------------------------
# V4-07
# Revisión futura todavía no aplica
# ---------------------------------------------------------

def test_v4_07_future_revision_not_applied_early(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        value=20
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=50,
        effectiveFrom="2026-09-11T00:00:00.000Z"
    )

    assert response.status_code in (200, 204)

    # TEST_NOW inicial = 2026-09-10.
    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert result.status_code in (200, 201)

    data = result.json()

    # Todavía debe aplicar 20 %.
    assert_money(data["discount"], 17.998)
    assert_money(data["total"], 71.992)


# ---------------------------------------------------------
# V4-08
# Revisión futura aplica al llegar effectiveFrom
# ---------------------------------------------------------

def test_v4_08_future_revision_applies_at_effective_from(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        value=20
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=50,
        effectiveFrom="2026-09-11T00:00:00.000Z"
    )

    assert response.status_code in (200, 204)

    urbanwear_server.restart(
        "2026-09-11T00:00:00.000Z"
    )

    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert result.status_code in (200, 201)

    data = result.json()

    assert_money(data["discount"], 44.995)
    assert_money(data["total"], 44.995)


# ---------------------------------------------------------
# V4-09
# active=false bloquea el cupón
# ---------------------------------------------------------

def test_v4_09_inactive_coupon_is_rejected(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        active=False
    )

    assert response.status_code in (200, 204)

    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert result.status_code >= 400


# ---------------------------------------------------------
# V4-10
# Reactivar vuelve a permitir el uso
# ---------------------------------------------------------

def test_v4_10_reactivated_coupon_can_be_used(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    inactive = patch_coupon(
        urbanwear_server,
        coupon["code"],
        active=False
    )

    assert inactive.status_code in (200, 204)

    rejected = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert rejected.status_code >= 400

    # Mismo día, pero una hora más tarde.
    urbanwear_server.restart(
        "2026-09-10T13:00:00.000Z"
    )

    active = patch_coupon(
        urbanwear_server,
        coupon["code"],
        active=True
    )

    assert active.status_code in (200, 204)

    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert result.status_code in (200, 201)


# ---------------------------------------------------------
# V4-11
# Desactivar/reactivar no borra el historial
# ---------------------------------------------------------

def test_v4_11_reactivation_preserves_usage_history(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    # Uso 1 - 10 de septiembre
    first = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert first.status_code in (200, 201)

    # Día 11: desactivar.
    urbanwear_server.restart(
        "2026-09-11T12:00:00.000Z"
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        active=False
    )

    assert response.status_code in (200, 204)

    # Día 12: reactivar y hacer uso 2.
    urbanwear_server.restart(
        "2026-09-12T12:00:00.000Z"
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        active=True
    )

    assert response.status_code in (200, 204)

    second = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert second.status_code in (200, 201)

    # Día 13: uso 3.
    urbanwear_server.restart(
        "2026-09-13T12:00:00.000Z"
    )

    third = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert third.status_code in (200, 201)

    # Día 14: debería ser uso 4 y ser rechazado.
    urbanwear_server.restart(
        "2026-09-14T12:00:00.000Z"
    )

    fourth = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert fourth.status_code >= 400


# ---------------------------------------------------------
# V4-12
# maxUsesPerUser modifica el límite total
# ---------------------------------------------------------

def test_v4_12_configurable_max_uses(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        maxUsesPerUser=1
    )

    assert response.status_code in (200, 204)

    first = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert first.status_code in (200, 201)

    urbanwear_server.restart(
        "2026-09-11T12:00:00.000Z"
    )

    second = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert second.status_code >= 400


# ---------------------------------------------------------
# V4-13
# Bajar límite considera el historial anterior
# ---------------------------------------------------------

def test_v4_13_lowering_max_uses_considers_history(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    # Uso 1.
    first = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert first.status_code in (200, 201)

    # Uso 2.
    urbanwear_server.restart(
        "2026-09-11T12:00:00.000Z"
    )

    second = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert second.status_code in (200, 201)

    # Reducimos el máximo a 2.
    urbanwear_server.restart(
        "2026-09-12T12:00:00.000Z"
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        maxUsesPerUser=2
    )

    assert response.status_code in (200, 204)

    # El usuario ya tiene dos usos históricos.
    third = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert third.status_code >= 400


# ---------------------------------------------------------
# V4-14
# Cambiar de revisión no evita el límite diario
# ---------------------------------------------------------

def test_v4_14_new_revision_does_not_reset_daily_limit(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    first = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert first.status_code in (200, 201)

    # Sigue siendo 10 de septiembre.
    urbanwear_server.restart(
        "2026-09-10T13:00:00.000Z"
    )

    response = patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=30
    )

    assert response.status_code in (200, 204)

    second = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    # Aunque cambió la revisión, ya usó el cupón hoy.
    assert second.status_code >= 400


# ---------------------------------------------------------
# V4-15
# Cupón creado con contrato anterior sigue funcionando
# ---------------------------------------------------------

def test_v4_15_legacy_coupon_remains_compatible(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        type="percentage",
        value=20,
        minimumAmount=80,
        categoryIds=[1],
        allowedUserIds=[1]
    )

    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1
    )

    assert result.status_code in (200, 201)

    data = result.json()

    assert_money(data["subtotal"], 89.99)
    assert_money(data["discount"], 17.998)
    assert_money(data["total"], 71.992)