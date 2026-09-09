# Ground Truth Privado - UrbanWear

> IMPORTANTE:
>
> Este archivo pertenece exclusivamente al evaluador.
> No debe ser visible para ninguno de los agentes.
>
> Los agentes reciben únicamente el ticket correspondiente a cada versión
> y pueden solicitar aclaraciones.

# 1. Propósito

Este documento define el comportamiento funcional esperado de UrbanWear para
las versiones V1, V2, V3 y V4.

Se utiliza para:

- construir la suite externa;
- responder aclaraciones;
- resolver ambigüedades;
- mantener el mismo criterio entre Prompt-Driven y SDD.

El ground truth no constituye entrada del agente.

# 2. Política de aclaraciones

Los tickets no pretenden funcionar como especificaciones exhaustivas.

Cuando exista una decisión de negocio que pueda interpretarse de más de una
forma razonable, cualquiera de los dos enfoques puede solicitar una aclaración.

Las aclaraciones:

- se responden exclusivamente utilizando este documento;
- proporcionan únicamente la información consultada;
- cuentan como intervención humana;
- se registran como aclaraciones de requisitos.

No se proporciona información de este archivo de forma proactiva.

Si el agente no pregunta y adopta una interpretación diferente de la definida
aquí, la diferencia será detectada por la evaluación externa.

# 3. Principio de evolución

Las versiones son acumulativas.

Una nueva versión modifica únicamente las reglas que modifica explícitamente.

Las reglas anteriores continúan vigentes mientras no sean reemplazadas.

Ante conflicto entre versiones prevalece la definición explícita más reciente.

# 4. V1 - Cupones

## 4.1. Identificación

Cada cupón posee un `code`.

El código debe ser único.

Crear un cupón con un código ya existente debe ser rechazado.

## 4.2. Tipos de descuento

Tipos válidos:

- `percentage`
- `fixed`

Para `percentage`:

- mínimo: 1;
- máximo: 100;
- ambos extremos inclusive.

Para `fixed`:

- representa un monto fijo;
- el total final nunca puede ser negativo;
- si el descuento supera el monto elegible, se limita al monto elegible.

## 4.3. Vigencia

Cada cupón posee:

- `validFrom`;
- `validUntil`.

Ambos límites son inclusivos.

Un cupón puede utilizarse exactamente en `validFrom` y `validUntil`.

Fuera del intervalo debe rechazarse.

## 4.4. Monto mínimo

`minimumAmount` se evalúa sobre el subtotal completo del carrito antes de aplicar
el descuento.

Ejemplo:

- subtotal = 90;
- minimumAmount = 80;
- descuento = 50 %.

El cupón cumple el mínimo porque se evalúa sobre 90.

## 4.5. Categorías

`categoryIds` representa las categorías elegibles para recibir descuento.

Si la lista está vacía:

- todos los productos son elegibles.

Si contiene categorías:

- únicamente los productos pertenecientes a esas categorías reciben descuento.

Un carrito mixto con productos elegibles y no elegibles puede realizar checkout.

El descuento se aplica solamente sobre los productos elegibles.

Si ningún producto es elegible, el cupón debe rechazarse.

## 4.6. Uso por usuario

En V1 un usuario puede utilizar exitosamente un mismo cupón una única vez.

Usuarios diferentes poseen historiales independientes.

## 4.7. Consumo de utilización

Solo un checkout exitoso consume una utilización.

Un intento rechazado no consume uso.

## 4.8. Checkout

Se admite un único cupón por checkout.

El checkout sin cupón debe continuar funcionando como en V0.

Debe continuar:

- creando una orden;
- calculando subtotal y total;
- vaciando el carrito luego del checkout exitoso.

## 4.9. Respuesta

Un checkout exitoso con cupón debe incluir:

- `subtotal`;
- `discount`;
- `total`;
- `couponCode`.

Los importes monetarios pueden utilizar redondeo convencional.

El evaluador acepta una diferencia máxima de un centavo.

## 4.10. Consulta

Consultar un cupón inexistente mediante su código debe responder como recurso
no encontrado.

# 5. V2 - Reutilización controlada

V2 reemplaza la regla de V1 de una única utilización total.

## 5.1. Máximo total

Un usuario puede utilizar exitosamente un mismo cupón hasta tres veces.

## 5.2. Máximo diario

Existe un máximo de una utilización exitosa por:

`usuario + cupón + día calendario`

## 5.3. Días diferentes

Un usuario puede realizar el segundo y tercer uso en días calendario
posteriores.

## 5.4. Cuarto uso

El cuarto uso debe rechazarse aunque ocurra en un día diferente.

## 5.5. Historial

Los usos deben persistir.

Reiniciar la aplicación utilizando la misma base no reinicia el historial.

## 5.6. Intentos fallidos

Un intento rechazado:

- no incrementa el contador total;
- no consume el uso diario.

Por lo tanto, un intento inválido no impide otro intento válido durante el
mismo día.

## 5.7. Usuarios independientes

El historial pertenece conceptualmente a:

`usuario + cupón`

El comportamiento de un usuario no modifica el contador de otro.

# 6. V3 - Segmentación de usuarios

## 6.1. Campo

El campo utilizado es:

`allowedUserIds`

## 6.2. Cupón general

Si `allowedUserIds`:

- no se encuentra presente; o
- contiene una lista vacía;

el cupón no posee restricción adicional por usuario.

## 6.3. Cupón segmentado

Cuando la lista contiene IDs, solo esos usuarios pueden utilizar el cupón.

## 6.4. Usuario no permitido

El intento debe rechazarse.

El rechazo no consume una utilización.

## 6.5. Composición

Estar autorizado mediante `allowedUserIds` no evita ninguna otra regla.

Continúan aplicándose:

- vigencia;
- monto mínimo;
- categorías;
- límite diario;
- límite total.

# 7. V4 - Evolución temporal del cupón

V4 permite modificar la configuración de un cupón sin cambiar su identidad ni
perder su historial.

Todas las configuraciones pertenecen al mismo cupón identificado por `code`.

# 8. PATCH

Se incorpora:

`PATCH /coupons/:code`

La operación es parcial.

Solo deben modificarse los campos enviados.

Los campos omitidos conservan su valor según la línea temporal de revisiones.

## 8.1. Código

`code` es inmutable.

Un PATCH no puede cambiarlo.

## 8.2. Cupón inexistente

PATCH sobre un cupón inexistente debe responder como recurso no encontrado.

# 9. effectiveFrom

Una modificación puede contener:

`effectiveFrom`

Si se omite:

- el cambio entra en vigencia inmediatamente;
- se utiliza el instante proporcionado por `TEST_NOW`.

Si corresponde a un instante futuro:

- la revisión debe persistirse;
- no debe alterar el comportamiento antes de ese instante.

## 9.1. Frontera temporal

Cuando:

`effectiveFrom == instante actual`

la revisión ya se considera vigente.

# 10. Configuración efectiva

Para determinar la configuración correspondiente a un instante:

1. se parte de la configuración original del cupón;
2. se ordenan las revisiones por `effectiveFrom`;
3. se seleccionan las revisiones cuyo `effectiveFrom` sea menor o igual al
   instante actual;
4. se aplican cronológicamente;
5. cada revisión modifica únicamente los campos que declara.

El resultado acumulado constituye la configuración efectiva.

# 11. Herencia parcial

Ejemplo:

Configuración inicial:

- descuento 20 %;
- mínimo 50.

Revisión del 15/09:

- descuento 30 %.

Revisión del 20/09:

- mínimo 100.

A partir del 20/09:

- descuento 30 %;
- mínimo 100.

# 12. Revisiones creadas fuera de orden

El orden de creación no determina la configuración.

La semántica depende de `effectiveFrom`.

Por ejemplo, si se crea primero:

- 20/09: mínimo = 100

y posteriormente:

- 15/09: descuento = 30 %

desde el 20/09 deben coexistir ambos cambios.

# 13. Inserción de revisiones

Puede crearse posteriormente una revisión cuya fecha se encuentre entre dos
revisiones ya existentes.

Las configuraciones posteriores deben reconstruirse de acuerdo con la secuencia
temporal resultante.

Una revisión no puede conservar valores heredados incorrectos únicamente por el
orden en que fue creada.

# 14. Múltiples revisiones futuras

Un cupón puede contener varias revisiones futuras simultáneamente.

Pueden afectar campos diferentes.

Una revisión futura no modifica ningún checkout anterior a su `effectiveFrom`.

# 15. Campos modificables

V4 permite modificar mediante revisiones:

- `type`;
- `value`;
- `validFrom`;
- `validUntil`;
- `minimumAmount`;
- `categoryIds`;
- `allowedUserIds`;
- `active`;
- `maxUsesPerUser`.

# 16. active

Valor predeterminado:

`true`

Cuando la configuración efectiva posee:

`active = false`

el cupón no puede utilizarse.

Una revisión posterior puede reactivarlo.

Desactivar o reactivar no modifica el historial.

# 17. maxUsesPerUser

Si nunca se configura:

`maxUsesPerUser = 3`

manteniendo la política introducida en V2.

Puede modificarse mediante una revisión.

## 17.1. Historial

El límite utiliza todas las utilizaciones exitosas históricas del usuario para
ese cupón.

Las revisiones no crean contadores independientes.

## 17.2. Reducción

Si un usuario posee dos usos y el máximo se cambia a 2, no puede realizar un
nuevo uso.

## 17.3. Aumento

Aumentar el límite permite nuevos usos hasta alcanzar el nuevo máximo, pero los
usos anteriores continúan contando.

# 18. Límite diario

Una nueva revisión no reinicia el límite diario.

Si el usuario utilizó el cupón y posteriormente ese mismo día existe un PATCH,
no puede volver a utilizarlo únicamente por haberse creado una revisión.

# 19. Historial global

El historial pertenece conceptualmente a:

`coupon code + user`

No pertenece a una revisión.

Debe sobrevivir:

- cambios de descuento;
- cambios de elegibilidad;
- desactivaciones;
- reactivaciones;
- modificaciones del límite;
- múltiples revisiones.

# 20. Categorías en V4

La configuración efectiva determina `categoryIds`.

Continúan las reglas de V1:

- vacío = todos los productos;
- carrito mixto permitido;
- descuento solo sobre productos elegibles;
- ningún producto elegible = rechazo.

# 21. Usuarios permitidos en V4

La configuración efectiva determina `allowedUserIds`.

Una lista vacía significa cupón general.

Modificar la lista no elimina ni altera el historial anterior.

# 22. Monto mínimo en V4

La configuración efectiva determina `minimumAmount`.

Continúa evaluándose sobre el subtotal completo previo al descuento.

# 23. Vigencia en V4

`effectiveFrom` y la vigencia comercial son conceptos diferentes.

`effectiveFrom` determina desde cuándo una configuración resulta efectiva.

`validFrom` y `validUntil` determinan si el cupón puede utilizarse bajo esa
configuración.

# 24. Descuentos en V4

La configuración efectiva determina:

- `type`;
- `value`.

Modificar únicamente `value` no modifica `type`.

Continúan aplicándose las reglas de V1.

# 25. Composición

Las reglas introducidas en diferentes versiones pueden encontrarse activas
simultáneamente.

Una nueva revisión no elimina automáticamente reglas anteriores.

Debe utilizarse la configuración efectiva completa.

# 26. Compatibilidad

Un cupón que nunca recibió PATCH debe continuar comportándose igual que antes
de V4.

Deben seguir funcionando:

- creación;
- consulta;
- carrito;
- checkout con cupón;
- checkout sin cupón.

# 27. Consumo de uso

Únicamente un checkout exitoso registra utilización.

No consumen uso los rechazos provocados por:

- inexistencia;
- inactividad;
- vigencia;
- autorización;
- mínimo;
- categoría;
- límite diario;
- límite total.

# 28. Tiempo controlado

El evaluador utiliza:

`TEST_NOW`

Debe ser utilizado por el reloj centralizado para:

- vigencia;
- días de utilización;
- revisiones `effectiveFrom`.

El evaluador puede reiniciar la aplicación modificando `TEST_NOW` y conservando
la misma base de datos.

# 29. Principio de evaluación

Los tests externos evalúan comportamiento observable.

No se exige una arquitectura concreta.

El agente puede elegir libremente:

- tablas;
- modelos;
- helpers;
- servicios;
- representación de revisiones;
- estrategia de reconstrucción temporal.

# 30. Cantidad de tests

V1:

30 tests.

V2:

37 acumulativos.

V3:

46 acumulativos.

V4:

66 acumulativos.

Además:

2 tests de infraestructura V0.

Total:

68 tests.

## Día calendario

Para aplicar el límite diario se utiliza el día calendario en UTC.

El instante controlado mediante `TEST_NOW` determina el día correspondiente.
