# Ground Truth Privado - UrbanWear

> IMPORTANTE:
>
> Este archivo pertenece exclusivamente al evaluador del experimento.
> No debe ser utilizado como entrada del agente durante ninguna trayectoria.
>
> Los agentes únicamente reciben los briefs públicos correspondientes a cada
> versión.

# 1. Propósito

Este documento define el comportamiento esperado de la funcionalidad de cupones
a lo largo de V1, V2, V3 y V4.

Se utiliza para:

- diseñar tests externos;
- responder aclaraciones;
- resolver ambigüedades previstas;
- mantener condiciones equivalentes entre Prompt-Driven y SDD.

# 2. Principio de evolución

Las versiones son acumulativas.

Una nueva versión modifica únicamente las reglas explícitamente indicadas.

Los requisitos anteriores continúan vigentes salvo que una versión posterior los
reemplace explícitamente.

Ante un conflicto entre versiones, prevalece la definición explícita más
reciente.

# 3. V1 - Cupones de descuento

## 3.1. Identificación

Cada cupón posee un `code`.

El código debe ser único.

No pueden existir dos cupones con el mismo código.

## 3.2. Tipos de descuento

Existen dos tipos:

- `percentage`
- `fixed`

### Percentage

El valor porcentual válido se encuentra entre:

`1 y 100`

inclusive.

### Fixed

Representa un monto fijo a descontar.

El descuento aplicado nunca puede producir un total negativo.

Si el monto fijo supera al monto elegible, el descuento efectivo se limita al
monto correspondiente.

## 3.3. Vigencia

Cada cupón posee:

- `validFrom`
- `validUntil`

Ambos extremos son inclusivos.

Por lo tanto:

- el cupón puede utilizarse exactamente en `validFrom`;
- el cupón puede utilizarse exactamente en `validUntil`.

Fuera del intervalo debe rechazarse.

## 3.4. Monto mínimo

`minimumAmount` se evalúa sobre el subtotal completo del carrito antes de aplicar
el descuento.

Por ejemplo:

- subtotal: 90
- mínimo: 80
- descuento: 50 %

El cupón es válido porque el mínimo se evalúa sobre 90, no sobre el total luego
del descuento.

## 3.5. Restricción por categorías

`categoryIds` representa las categorías elegibles para recibir el descuento.

Si `categoryIds` está vacío, todos los productos son elegibles.

Si posee categorías:

- únicamente los productos pertenecientes a dichas categorías reciben descuento;
- pueden existir productos elegibles y no elegibles en un mismo carrito;
- el checkout sigue siendo válido mientras exista al menos un producto elegible.

Si ningún producto del carrito pertenece a una categoría elegible, el cupón debe
ser rechazado.

## 3.6. Cupón por checkout

Solo puede aplicarse un cupón por checkout.

## 3.7. Uso inicial por usuario

En V1 un mismo usuario puede utilizar un mismo cupón una única vez.

Usuarios distintos pueden utilizar el mismo cupón de manera independiente.

## 3.8. Consumo del uso

Únicamente un checkout exitoso consume una utilización.

Intentos rechazados por cualquier motivo no consumen uso.

## 3.9. Checkout sin cupón

El checkout sin cupón debe conservar el comportamiento existente de V0.

No debe ser necesario proporcionar `couponCode`.

Debe continuar:

- creando una orden;
- calculando correctamente el subtotal;
- manteniendo subtotal igual a total;
- vaciando el carrito después del checkout exitoso.

## 3.10. Respuesta de checkout con cupón

Un checkout exitoso con cupón debe permitir observar:

- subtotal;
- descuento;
- total;
- código del cupón utilizado.

Los importes monetarios pueden utilizar redondeo convencional de moneda.

El evaluador utiliza tolerancia de un centavo para evitar penalizar diferencias
de representación decimal razonables.

# 4. V2 - Evolución del límite de usos

V2 reemplaza la regla de V1 que permitía una única utilización por usuario.

## 4.1. Máximo total

Un usuario puede utilizar un mismo cupón hasta tres veces en total.

## 4.2. Máximo diario

Un usuario puede utilizar un mismo cupón como máximo una vez por día calendario.

## 4.3. Días distintos

El mismo usuario puede utilizar nuevamente el cupón en días calendario
posteriores mientras no haya alcanzado el máximo total de tres usos.

## 4.4. Cuarto uso

Una cuarta utilización exitosa debe ser rechazada aunque ocurra en un día
distinto.

## 4.5. Independencia entre usuarios

El historial de un usuario no afecta el de otro usuario.

## 4.6. Intentos fallidos

Un intento rechazado:

- no incrementa el contador total;
- no consume la utilización correspondiente al día.

Por lo tanto, un usuario puede realizar un intento inválido y posteriormente
realizar uno válido durante el mismo día.

## 4.7. Persistencia

El historial debe persistir entre reinicios de la aplicación cuando se utiliza
la misma base de datos.

## 4.8. Reglas heredadas

Continúan vigentes todas las reglas de:

- descuentos;
- vigencia;
- mínimo;
- categorías;
- compatibilidad;
- checkout.

La única regla reemplazada explícitamente es el límite de una utilización total
de V1.

# 5. V3 - Restricciones por usuario

V3 incorpora autorización opcional por usuario.

## 5.1. Campo

El campo utilizado es:

`allowedUserIds`

## 5.2. Sin restricción

Si `allowedUserIds`:

- no está presente; o
- está vacío;

el cupón no posee una restricción adicional por usuario.

## 5.3. Con restricción

Si contiene IDs, únicamente los usuarios incluidos pueden utilizar el cupón.

## 5.4. Usuario no autorizado

Un usuario no incluido debe ser rechazado.

## 5.5. Historial

Un intento rechazado por falta de autorización no consume una utilización.

## 5.6. Combinación con otras reglas

Estar autorizado no permite evitar ninguna otra validación.

Un usuario habilitado debe igualmente cumplir:

- vigencia;
- mínimo;
- categorías;
- límite diario;
- límite total.

## 5.7. Reglas heredadas

Todas las reglas anteriores continúan vigentes salvo modificación explícita.

# 6. V4 - Evolución temporal de configuración

V4 permite que un mismo cupón posea diferentes configuraciones a lo largo del
tiempo.

El cupón mantiene una única identidad lógica identificada por `code`.

Las distintas configuraciones representan revisiones parciales de ese mismo
cupón.

Una revisión no constituye un cupón nuevo.

# 7. PATCH de cupones

Se incorpora:

`PATCH /coupons/:code`

El endpoint permite modificar parcialmente la configuración del cupón.

## 7.1. Actualización parcial

Únicamente los campos enviados deben ser modificados.

Los campos omitidos no se reemplazan por valores por defecto ni se eliminan.

Su valor efectivo debe obtenerse mediante la herencia temporal definida para las
revisiones.

## 7.2. Código inmutable

`code` es el identificador estable del cupón.

No puede modificarse mediante PATCH.

Un intento de modificarlo debe ser rechazado.

## 7.3. Cupón inexistente

Intentar modificar un cupón inexistente debe producir una respuesta de error de
recurso no encontrado.

# 8. effectiveFrom

Una actualización puede incluir:

`effectiveFrom`

## 8.1. Ausencia de effectiveFrom

Si no se especifica, la nueva revisión entra en vigencia inmediatamente.

Para el experimento, "inmediatamente" significa el instante actual proporcionado
por el reloj controlable de la aplicación:

`TEST_NOW`

## 8.2. Revisión futura

Si `effectiveFrom` está en el futuro:

- la revisión debe almacenarse;
- no debe modificar el comportamiento actual;
- las revisiones anteriores continúan determinando la configuración efectiva
  hasta alcanzar dicho instante.

## 8.3. Revisión efectiva

Para determinar la configuración de un cupón en un instante determinado no
alcanza con seleccionar de forma aislada una única revisión.

Debe reconstruirse la configuración aplicando secuencialmente las revisiones
correspondientes.

El procedimiento conceptual es:

1. partir de la configuración inicial del cupón;
2. ordenar las revisiones por `effectiveFrom` de menor a mayor;
3. considerar únicamente las revisiones cuyo `effectiveFrom` sea menor o igual
   al instante evaluado;
4. aplicar cada revisión en orden cronológico;
5. cada revisión reemplaza únicamente los campos que declara explícitamente;
6. los demás campos mantienen el valor resultante de la configuración anterior.

El resultado de este proceso constituye la configuración efectiva del cupón.

## 8.4. Llegada del instante

Cuando el reloj alcanza exactamente el valor de `effectiveFrom`, la revisión ya
debe considerarse vigente.

Es decir:

`effectiveFrom <= instante actual`

# 9. Herencia temporal entre revisiones

La herencia de campos se determina por la posición cronológica de las revisiones
y no por el orden en que fueron creadas mediante PATCH.

Cada revisión representa un conjunto parcial de cambios.

Los campos omitidos deben mantener el último valor definido cronológicamente
antes de esa revisión.

## 9.1. Acumulación de cambios parciales

Ejemplo:

Configuración inicial:

- descuento: 20 %
- mínimo: 50

Revisión del 15/09:

- descuento: 30 %

Revisión del 20/09:

- mínimo: 100

La configuración efectiva desde el 20/09 es:

- descuento: 30 %
- mínimo: 100

La revisión del día 20 no debe restaurar el descuento al 20 % por el hecho de no
haberlo declarado.

## 9.2. Revisiones creadas fuera de orden

Las revisiones pueden crearse en cualquier orden.

Por ejemplo, puede crearse primero:

- 20/09: mínimo = 100

y después:

- 15/09: descuento = 30 %

La configuración efectiva a partir del 20/09 debe continuar siendo:

- descuento: 30 %
- mínimo: 100

aunque la revisión correspondiente al día 20 haya sido almacenada antes que la
del día 15.

El orden de creación no forma parte de la semántica funcional.

## 9.3. Inserción de una revisión intermedia

Puede agregarse posteriormente una revisión cuya fecha se encuentre entre dos
revisiones ya existentes.

Ejemplo:

Configuración inicial:

- descuento: 20 %
- mínimo: 50
- usuarios: sin restricción

Se crean inicialmente:

- 20/09: mínimo = 100
- 25/09: descuento = 40 %

Luego se agrega:

- 22/09: `allowedUserIds = [2]`

La configuración resultante debe ser:

### Antes del 20/09

- descuento: 20 %
- mínimo: 50
- usuarios: sin restricción

### Desde el 20/09 hasta antes del 22/09

- descuento: 20 %
- mínimo: 100
- usuarios: sin restricción

### Desde el 22/09 hasta antes del 25/09

- descuento: 20 %
- mínimo: 100
- usuarios permitidos: [2]

### Desde el 25/09

- descuento: 40 %
- mínimo: 100
- usuarios permitidos: [2]

Una revisión posterior no puede conservar una copia incorrecta de la
configuración simplemente porque fue creada antes de una revisión
cronológicamente anterior.

# 10. Múltiples revisiones futuras

Un mismo cupón puede poseer varias revisiones futuras simultáneamente.

Las revisiones pueden afectar campos diferentes.

Cuando cada una entra en vigencia, sus cambios deben integrarse con los valores
heredados de revisiones cronológicamente anteriores.

Una revisión futura nunca debe modificar el comportamiento observable antes de
su `effectiveFrom`.

# 11. Campos configurables en V4

Una revisión puede modificar los campos previamente existentes:

- `type`
- `value`
- `validFrom`
- `validUntil`
- `minimumAmount`
- `categoryIds`
- `allowedUserIds`

Además introduce:

- `active`
- `maxUsesPerUser`

Todos estos campos participan de la misma lógica de revisiones parciales.

# 12. active

## 12.1. Valor por defecto

Un cupón se considera activo por defecto:

`active = true`

## 12.2. Cupón inactivo

Cuando la configuración efectiva posee:

`active = false`

un checkout que intenta aplicar el cupón debe ser rechazado.

## 12.3. Reactivación

Una revisión posterior puede establecer:

`active = true`

permitiendo nuevamente el uso del cupón si se cumplen todas las demás reglas.

## 12.4. Historial

Desactivar o reactivar un cupón no elimina ni reinicia su historial de usos.

# 13. maxUsesPerUser

## 13.1. Comportamiento heredado

V2 estableció un máximo total predeterminado de:

`3 usos por usuario y cupón`

V4 permite configurar dicho límite.

## 13.2. Valor por defecto

Si nunca se especifica `maxUsesPerUser`, el comportamiento efectivo continúa
siendo:

`3`

## 13.3. Evaluación

El límite se compara contra todas las utilizaciones exitosas históricas del
usuario para ese cupón.

No importa bajo qué revisión fueron realizadas.

## 13.4. Reducción del límite

Si un usuario realizó dos usos y posteriormente:

`maxUsesPerUser = 2`

no puede realizar una nueva utilización.

## 13.5. Aumento del límite

Si el límite aumenta, los usos históricos siguen contando.

El usuario puede continuar utilizando el cupón únicamente hasta alcanzar el
nuevo máximo.

# 14. Límite diario y revisiones

El límite de una utilización exitosa por día calendario introducido en V2
continúa vigente.

Cambiar de revisión:

- no reinicia el límite diario;
- no permite reutilizar el cupón durante el mismo día;
- no crea un historial independiente.

Una utilización realizada antes de un PATCH continúa contando para el límite
diario después del PATCH.

# 15. Historial global del cupón

El historial pertenece conceptualmente a:

`coupon code + user`

y no a una revisión concreta.

Crear una revisión nueva no debe:

- borrar usos;
- reiniciar el contador total;
- reiniciar el contador diario;
- crear un cupón lógico diferente.

El historial debe sobrevivir a cualquier cantidad de revisiones.

# 16. Interacción entre revisiones e historial

Los cambios de configuración y el historial son conceptos independientes.

Las revisiones determinan qué reglas son efectivas en un momento.

El historial registra qué utilizaciones exitosas ocurrieron durante toda la vida
del cupón.

Para evaluar límites debe combinarse:

- la configuración efectiva actual;
- todo el historial previo del usuario para ese cupón.

Por ejemplo:

si un usuario utilizó un cupón tres veces bajo tres configuraciones distintas,
su historial sigue conteniendo tres utilizaciones.

# 17. Interacción con categorías

La configuración efectiva determina `categoryIds`.

Las mismas reglas de V1 siguen aplicándose:

- lista vacía: todos los productos;
- lista con categorías: solo esos productos reciben descuento;
- carrito mixto permitido;
- ningún producto elegible: cupón rechazado.

Modificar categorías mediante una revisión no afecta usos históricos.

# 18. Interacción con usuarios permitidos

La configuración efectiva determina `allowedUserIds`.

Las mismas reglas de V3 siguen aplicándose.

Una actualización puede:

- agregar usuarios;
- eliminar usuarios;
- reemplazar la lista;
- establecer una lista vacía y eliminar la restricción.

Cambiar la autorización de un usuario no modifica su historial previo.

# 19. Interacción con monto mínimo

La configuración efectiva determina `minimumAmount`.

El mínimo continúa evaluándose sobre el subtotal completo antes del descuento.

# 20. Interacción con vigencia

La configuración efectiva determina:

- `validFrom`;
- `validUntil`.

La vigencia de una revisión y la vigencia comercial del cupón son conceptos
diferentes.

`effectiveFrom` determina cuándo una configuración comienza a formar parte de la
línea temporal.

`validFrom` y `validUntil` determinan si el cupón puede utilizarse bajo esa
configuración.

Por ejemplo:

una revisión puede ser efectiva desde el 10/09 y contener:

`validFrom = 15/09`

En ese caso la configuración ya es efectiva desde el 10/09, pero el cupón no
puede utilizarse hasta el 15/09.

# 21. Interacción con descuentos

La configuración efectiva determina:

- `type`;
- `value`.

Continúan aplicándose las reglas originales:

- porcentaje entre 1 y 100;
- descuento fijo;
- total nunca negativo.

Una revisión que modifica únicamente `value` no debe modificar `type`, salvo que
también lo declare explícitamente.

# 22. Combinación de reglas provenientes de distintas versiones

Las revisiones pueden modificar reglas incorporadas originalmente en diferentes
versiones del experimento.

Por ejemplo, una misma línea temporal puede contener:

- modificación de categorías de V1;
- modificación de usuarios permitidos de V3;
- modificación del límite total derivado de V2;
- modificación del descuento de V1;
- activación de V4.

Todas las reglas efectivas deben combinarse simultáneamente.

La aparición de una nueva revisión no desactiva automáticamente otras reglas.

# 23. Compatibilidad

V4 no debe romper las APIs existentes.

Deben seguir funcionando:

- creación de cupones;
- consulta de cupones;
- checkout con cupón;
- checkout sin cupón;
- carrito;
- productos.

Un cupón creado mediante la API anterior y que nunca recibió un PATCH debe
comportarse exactamente como antes de V4.

# 24. Prioridad conceptual de evaluación

Para un checkout con cupón se debe:

1. reconstruir la configuración efectiva correspondiente al instante actual;
2. evaluar las reglas vigentes de esa configuración;
3. consultar el historial global del cupón cuando corresponda.

Luego se aplican conjuntamente las reglas:

1. `active`;
2. vigencia;
3. autorización por usuario;
4. monto mínimo;
5. categorías;
6. límite diario;
7. límite total;
8. cálculo del descuento.

El orden interno de implementación puede variar siempre que el comportamiento
observable sea equivalente.

# 25. Consumo de utilización

Una utilización se registra únicamente cuando el checkout finaliza exitosamente.

No deben consumir uso los rechazos por:

- cupón inexistente;
- cupón inactivo;
- fuera de vigencia;
- usuario no autorizado;
- monto mínimo;
- categoría;
- límite diario;
- límite total;
- cualquier otra validación previa al checkout exitoso.

# 26. Control temporal

Los tests externos utilizan `TEST_NOW` para controlar el instante actual.

Las reglas temporales deberán utilizar el reloj centralizado de la aplicación.

Esto incluye:

- vigencia de cupón;
- límite por día calendario;
- `effectiveFrom` de revisiones.

El evaluador puede reiniciar la aplicación con diferentes valores de `TEST_NOW`
manteniendo la misma base de datos para simular el paso del tiempo.

El reinicio de la aplicación no debe modificar:

- revisiones;
- historial;
- configuración persistida.

# 27. Reglas de aclaración

Si el agente solicita una aclaración durante el experimento, únicamente se podrá
responder utilizando información definida en este archivo.

La respuesta debe proporcionar solo la información necesaria para resolver la
pregunta.

No se debe revelar:

- la estructura de los tests;
- nombres de tests;
- resultados esperados completos;
- información sobre el otro enfoque;
- contenido adicional del ground truth no relacionado con la pregunta.

# 28. Principio de evaluación

Los tests externos validan comportamiento observable.

No se exige una arquitectura interna específica.

El agente es libre de utilizar:

- nuevas tablas;
- columnas;
- tablas de revisiones;
- tablas de historial;
- servicios;
- helpers;
- reconstrucción dinámica de configuración;
- cualquier estructura razonable.

La evaluación no debe favorecer una implementación interna particular mientras
el comportamiento observable cumpla este ground truth.

# 29. Evaluación acumulativa de V4

V4 se evalúa manteniendo activos todos los comportamientos anteriores.

La suite funcional acumulativa contiene:

- V1: 30 tests;
- V2: 7 tests nuevos;
- V3: 9 tests nuevos;
- V4: 20 tests nuevos.

Total funcional acumulativo en V4:

`66 tests`

Además existen:

`2 tests de infraestructura de V0`

Por lo tanto, la colección completa del evaluador contiene:

`68 tests`

La evaluación específica de V4 debe permitir distinguir:

- preservación V1-V3: 46 tests;
- cumplimiento nuevo V4: 20 tests;
- cumplimiento acumulativo: 66 tests.
