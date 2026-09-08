import uuid

import pytest
import requests


def code(prefix="V4-TIMELINE"):
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
    response = requests.patch(
        f"{server}/coupons/{coupon_code}",
        json=changes
    )

    assert response.status_code in (200, 204)

    return response


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
    product_id=1,
    quantity=1
):
    add_product(
        server,
        user_id,
        product_id,
        quantity
    )

    return checkout(
        server,
        user_id,
        coupon_code
    )


# ---------------------------------------------------------
# V4-16
# Dos revisiones futuras acumulan cambios parciales
# ---------------------------------------------------------

def test_v4_16_future_revisions_accumulate_partial_changes(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        value=20,
        minimumAmount=0
    )

    patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=30,
        effectiveFrom="2026-09-15T00:00:00.000Z"
    )

    patch_coupon(
        urbanwear_server,
        coupon["code"],
        minimumAmount=100,
        effectiveFrom="2026-09-20T00:00:00.000Z"
    )

    urbanwear_server.restart(
        "2026-09-21T12:00:00.000Z"
    )

    # 2 x 89.99 = 179.98.
    # Debe conservar el descuento 30 % de la revisión del día 15
    # y aplicar mínimo 100 de la revisión del día 20.
    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1,
        quantity=2
    )

    assert result.status_code in (200, 201)

    data = result.json()

    assert_money(data["subtotal"], 179.98)
    assert_money(data["discount"], 53.994)
    assert_money(data["total"], 125.986)


# ---------------------------------------------------------
# V4-17
# Crear revisiones fuera de orden no cambia la línea temporal
# ---------------------------------------------------------

def test_v4_17_out_of_order_creation_uses_chronological_timeline(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        value=20,
        minimumAmount=0
    )

    # Primero programamos una revisión más lejana.
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        minimumAmount=100,
        effectiveFrom="2026-09-20T00:00:00.000Z"
    )

    # Después insertamos una revisión cronológicamente anterior.
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=30,
        effectiveFrom="2026-09-15T00:00:00.000Z"
    )

    urbanwear_server.restart(
        "2026-09-21T12:00:00.000Z"
    )

    result = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1,
        quantity=2
    )

    assert result.status_code in (200, 201)

    data = result.json()

    # Deben coexistir:
    # - value=30 heredado desde el 15
    # - minimumAmount=100 aplicado desde el 20
    assert_money(data["subtotal"], 179.98)
    assert_money(data["discount"], 53.994)
    assert_money(data["total"], 125.986)


# ---------------------------------------------------------
# V4-18
# Insertar una revisión entre otras dos mantiene herencia temporal
# ---------------------------------------------------------

def test_v4_18_insert_intermediate_revision_preserves_timeline_inheritance(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        value=20,
        minimumAmount=0,
        allowedUserIds=[]
    )

    # Revisión día 20.
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        minimumAmount=100,
        effectiveFrom="2026-09-20T00:00:00.000Z"
    )

    # Revisión día 25.
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=40,
        effectiveFrom="2026-09-25T00:00:00.000Z"
    )

    # Luego insertamos una revisión entre ambas.
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        allowedUserIds=[2],
        effectiveFrom="2026-09-22T00:00:00.000Z"
    )

    # Día 23:
    # min=100, value todavía=20, usuario permitido=2.
    urbanwear_server.restart(
        "2026-09-23T12:00:00.000Z"
    )

    rejected = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=1,
        quantity=2
    )

    assert rejected.status_code >= 400

    allowed = use_coupon(
        urbanwear_server,
        2,
        coupon["code"],
        product_id=1,
        quantity=2
    )

    assert allowed.status_code in (200, 201)

    data = allowed.json()

    assert_money(data["subtotal"], 179.98)
    assert_money(data["discount"], 35.996)
    assert_money(data["total"], 143.984)

    # Día 26:
    # siguen vigentes mínimo=100 y allowedUserIds=[2],
    # pero ahora value=40.
    urbanwear_server.restart(
        "2026-09-26T12:00:00.000Z"
    )

    result = use_coupon(
        urbanwear_server,
        2,
        coupon["code"],
        product_id=1,
        quantity=2
    )

    assert result.status_code in (200, 201)

    data = result.json()

    assert_money(data["subtotal"], 179.98)
    assert_money(data["discount"], 71.992)
    assert_money(data["total"], 107.988)


# ---------------------------------------------------------
# V4-19
# Reglas de distintas versiones se combinan
# ---------------------------------------------------------

def test_v4_19_rules_from_multiple_versions_combine(
    urbanwear_server
):
    coupon = create_coupon(
        urbanwear_server,
        value=20,
        minimumAmount=0,
        categoryIds=[],
        allowedUserIds=[]
    )

    # V1: categorías
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        categoryIds=[2],
        effectiveFrom="2026-09-11T00:00:00.000Z"
    )

    # V3: usuarios permitidos
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        allowedUserIds=[2],
        effectiveFrom="2026-09-12T00:00:00.000Z"
    )

    # V1: mínimo
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        minimumAmount=100,
        effectiveFrom="2026-09-13T00:00:00.000Z"
    )

    # V1: descuento
    patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=50,
        effectiveFrom="2026-09-14T00:00:00.000Z"
    )

    urbanwear_server.restart(
        "2026-09-14T12:00:00.000Z"
    )

    # Usuario 1 no está permitido.
    rejected_user = use_coupon(
        urbanwear_server,
        1,
        coupon["code"],
        product_id=4
    )

    assert rejected_user.status_code >= 400

    # Usuario 2 sí está permitido.
    # Producto 4 cuesta 129.99 y pertenece a categoría 2.
    result = use_coupon(
        urbanwear_server,
        2,
        coupon["code"],
        product_id=4
    )

    assert result.status_code in (200, 201)

    data = result.json()

    assert_money(data["subtotal"], 129.99)
    assert_money(data["discount"], 64.995)
    assert_money(data["total"], 64.995)


# ---------------------------------------------------------
# V4-20
# Historial sobrevive múltiples revisiones
# ---------------------------------------------------------

def test_v4_20_usage_history_survives_multiple_revisions(
    urbanwear_server
):
    coupon = create_coupon(urbanwear_server)

    # Uso 1 con configuración original.
    first = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert first.status_code in (200, 201)

    # Día 11: nueva revisión y uso 2.
    urbanwear_server.restart(
        "2026-09-11T12:00:00.000Z"
    )

    patch_coupon(
        urbanwear_server,
        coupon["code"],
        value=30
    )

    second = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert second.status_code in (200, 201)

    # Día 12: otra revisión y uso 3.
    urbanwear_server.restart(
        "2026-09-12T12:00:00.000Z"
    )

    patch_coupon(
        urbanwear_server,
        coupon["code"],
        allowedUserIds=[1]
    )

    third = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert third.status_code in (200, 201)

    # Día 13: otra revisión.
    # El historial anterior debe seguir siendo 3 usos.
    urbanwear_server.restart(
        "2026-09-13T12:00:00.000Z"
    )

    patch_coupon(
        urbanwear_server,
        coupon["code"],
        active=False
    )

    # Día 14: reactivamos.
    urbanwear_server.restart(
        "2026-09-14T12:00:00.000Z"
    )

    patch_coupon(
        urbanwear_server,
        coupon["code"],
        active=True
    )

    # El cuarto uso debe seguir rechazándose:
    # las revisiones no reinician el historial.
    fourth = use_coupon(
        urbanwear_server,
        1,
        coupon["code"]
    )

    assert fourth.status_code >= 400