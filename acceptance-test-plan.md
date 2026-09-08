# UrbanWear POC - Plan de Pruebas de Aceptación

## 1. Objetivo

La suite de aceptación constituye el mecanismo independiente utilizado para
evaluar las implementaciones generadas durante la prueba de concepto.

Los tests son externos al repositorio utilizado por los agentes y evalúan
únicamente el comportamiento observable de la API.

La suite no evalúa:

- estructura interna del código;
- nombres de clases;
- cantidad de archivos;
- existencia de documentación SDD;
- estilo de implementación;
- tests generados por el agente.

Se evalúa exclusivamente el cumplimiento funcional definido en el ground truth.

## 2. Principio acumulativo

Las versiones se evalúan de manera acumulativa.

### V1

- tests correspondientes a V1.

### V2

- tests correspondientes a V1;
- tests nuevos correspondientes a V2.

### V3

- tests correspondientes a V1;
- tests correspondientes a V2;
- tests nuevos correspondientes a V3.

### V4

- tests correspondientes a V1;
- tests correspondientes a V2;
- tests correspondientes a V3;
- tests nuevos correspondientes a V4.

Esto permite medir dos dimensiones diferentes:

1. incorporación correcta del nuevo cambio;
2. preservación del comportamiento definido en versiones anteriores.

## 3. Resultado del primer intento

La primera ejecución de la suite se realiza inmediatamente después de que el
agente declara terminada una versión.

Este resultado debe guardarse antes de proporcionar cualquier feedback.

Se registran:

- tests aprobados;
- tests totales;
- cumplimiento funcional;
- tests anteriores aprobados;
- preservación del comportamiento previo;
- tests correspondientes al cambio actual aprobados.

El objetivo es observar qué tan correctamente responde el agente al
requerimiento antes de recibir correcciones externas.

## 4. Resultado final

Luego de cada ciclo de corrección se vuelve a ejecutar la suite completa.

Se permite un máximo de tres ciclos.

Al finalizar se registra nuevamente:

- tests aprobados;
- tests totales;
- cumplimiento funcional;
- preservación;
- cumplimiento del cambio nuevo;
- cantidad de ciclos necesarios.

# 5. Tests de V1

## Creación y consulta

### TEST-V1-01

Crear correctamente un cupón porcentual válido.

### TEST-V1-02

Crear correctamente un cupón de monto fijo válido.

### TEST-V1-03

Rechazar la creación de dos cupones con el mismo código.

### TEST-V1-04

Consultar correctamente un cupón existente.

### TEST-V1-05

Responder correctamente ante un código inexistente.

## Descuento porcentual

### TEST-V1-06

Aplicar correctamente un descuento porcentual.

### TEST-V1-07

Aceptar un porcentaje del 100 % sin producir un total negativo.

### TEST-V1-08

Rechazar valores porcentuales inválidos.

## Descuento fijo

### TEST-V1-09

Aplicar correctamente un descuento fijo.

### TEST-V1-10

Limitar el descuento cuando el monto fijo supera el monto elegible.

## Vigencia

### TEST-V1-11

Permitir utilizar un cupón dentro de su período de vigencia.

### TEST-V1-12

Rechazar un cupón cuya fecha de inicio todavía no ocurrió.

### TEST-V1-13

Rechazar un cupón vencido.

### TEST-V1-14

Aceptar exactamente la fecha inicial de vigencia.

### TEST-V1-15

Aceptar exactamente la fecha final de vigencia.

## Monto mínimo

### TEST-V1-16

Rechazar un cupón cuando el subtotal es inferior al mínimo requerido.

### TEST-V1-17

Aceptar un cupón cuando el subtotal es exactamente igual al monto mínimo.

### TEST-V1-18

Verificar que el mínimo se calcule antes de aplicar el descuento.

## Categorías

### TEST-V1-19

Aplicar descuento a un carrito compuesto únicamente por categorías permitidas.

### TEST-V1-20

Aplicar descuento únicamente a productos elegibles cuando el carrito contiene
categorías permitidas y no permitidas.

### TEST-V1-21

Rechazar el cupón cuando ningún producto pertenece a una categoría permitida.

### TEST-V1-22

Aplicar el descuento a todo el carrito cuando el cupón no posee restricciones
de categoría.

## Uso por usuario

### TEST-V1-23

Permitir el primer uso del cupón.

### TEST-V1-24

Rechazar el segundo uso del mismo cupón por el mismo usuario.

### TEST-V1-25

Permitir que otro usuario utilice el mismo cupón.

### TEST-V1-26

Comprobar que un intento de checkout rechazado no consuma un uso.

## Compatibilidad con comportamiento previo

### TEST-V1-27

Permitir checkout sin cupón.

### TEST-V1-28

Verificar que subtotal y total sean iguales cuando no existe cupón.

### TEST-V1-29

Verificar que un checkout exitoso continúe generando una orden.

### TEST-V1-30

Verificar que el carrito continúe vaciándose después de un checkout exitoso.

# 6. Tests nuevos de V2

Todos los tests V1 deben continuar pasando.

### TEST-V2-01

Rechazar dos usos del mismo cupón por el mismo usuario durante el mismo día.

### TEST-V2-02

Permitir un segundo uso en un día calendario posterior.

### TEST-V2-03

Permitir un tercer uso en otro día posterior.

### TEST-V2-04

Rechazar un cuarto uso aunque corresponda a un día diferente.

### TEST-V2-05

Mantener el contador de usos independiente entre usuarios.

### TEST-V2-06

Verificar que un intento fallido no incremente el contador total.

### TEST-V2-07

Verificar que un intento fallido no bloquee un uso válido posterior durante
el mismo día.

# 7. Tests nuevos de V3

Todos los tests V1 y V2 deben continuar pasando.

### TEST-V3-01

Permitir utilizar un cupón que no posee restricción de usuarios.

### TEST-V3-02

Permitir utilizar un cupón por un usuario incluido en la lista permitida.

### TEST-V3-03

Rechazar el uso por un usuario no incluido en la lista.

### TEST-V3-04

Verificar que un rechazo por usuario no autorizado no consuma un uso.

### TEST-V3-05

Verificar que un usuario autorizado deba igualmente cumplir la vigencia.

### TEST-V3-06

Verificar que un usuario autorizado deba igualmente cumplir el monto mínimo.

### TEST-V3-07

Verificar que un usuario autorizado deba igualmente cumplir las restricciones
por categoría.

### TEST-V3-08

Verificar que un usuario autorizado continúe sujeto al máximo de un uso diario.

### TEST-V3-09

Verificar que un usuario autorizado continúe sujeto al límite total de tres usos.

# 8. Tests nuevos de V4

Todos los tests V1, V2 y V3 deben continuar pasando.

V4 incorpora evolución temporal y revisiones parciales de la configuración de
un mismo cupón.

## Actualizaciones parciales

### TEST-V4-01

Verificar que un PATCH parcial conserve los campos que no fueron modificados.

### TEST-V4-02

Rechazar un intento de modificar el código del cupón.

### TEST-V4-03

Aplicar inmediatamente una modificación del descuento.

### TEST-V4-04

Aplicar inmediatamente una modificación del monto mínimo.

### TEST-V4-05

Aplicar inmediatamente una modificación de las categorías permitidas.

### TEST-V4-06

Aplicar inmediatamente una modificación de los usuarios permitidos.

## Revisiones futuras

### TEST-V4-07

Verificar que una revisión futura no afecte el comportamiento antes de su
`effectiveFrom`.

### TEST-V4-08

Verificar que una revisión comience a aplicarse exactamente al alcanzar su
`effectiveFrom`.

## Activación

### TEST-V4-09

Rechazar el uso de un cupón cuya configuración efectiva posea `active=false`.

### TEST-V4-10

Permitir nuevamente el uso después de una revisión que reactive el cupón.

### TEST-V4-11

Verificar que desactivar y posteriormente reactivar un cupón no elimine su
historial de usos.

## Límite configurable

### TEST-V4-12

Verificar que `maxUsesPerUser` modifique el límite total de utilizaciones.

### TEST-V4-13

Verificar que reducir `maxUsesPerUser` considere las utilizaciones históricas
realizadas antes del cambio.

## Preservación del historial

### TEST-V4-14

Verificar que crear una nueva revisión no reinicie el límite de una utilización
por día.

### TEST-V4-15

Verificar que un cupón creado con el contrato anterior continúe funcionando sin
necesidad de revisiones.

## Línea temporal compleja

### TEST-V4-16

Verificar que dos revisiones futuras parciales acumulen correctamente sus
modificaciones.

### TEST-V4-17

Verificar que el resultado de las revisiones dependa de su orden cronológico y
no del orden en que fueron creadas.

### TEST-V4-18

Verificar que insertar posteriormente una revisión entre dos revisiones futuras
ya existentes mantenga correctamente la herencia de configuración a lo largo de
la línea temporal.

### TEST-V4-19

Verificar que reglas originadas en diferentes versiones de la funcionalidad
puedan combinarse correctamente después de varias revisiones temporales.

La configuración efectiva debe poder combinar, entre otras reglas:

- descuento;
- monto mínimo;
- categorías;
- usuarios permitidos.

### TEST-V4-20

Verificar que el historial total de utilización del cupón permanezca intacto a
través de múltiples revisiones sucesivas.

# 9. Cantidad esperada de tests activos

### V1

30 tests funcionales.

### V2

30 V1 + 7 V2 = **37 tests funcionales acumulativos**.

### V3

30 V1 + 7 V2 + 9 V3 = **46 tests funcionales acumulativos**.

### V4

30 V1 + 7 V2 + 9 V3 + 20 V4 =
**66 tests funcionales acumulativos**.

Además existen 2 tests correspondientes a V0/infraestructura.

Por lo tanto, la colección completa del evaluador contiene:

**68 tests totales**

de los cuales:

- 2 corresponden a V0/infraestructura;
- 66 corresponden a la evaluación funcional acumulativa V1-V4.

# 10. Métricas derivadas

## Cumplimiento funcional

Cumplimiento:

`tests activos aprobados / tests activos totales`

## Preservación

### V2

Preservación:

`tests V1 aprobados / 30`

### V3

Preservación:

`tests V1 y V2 aprobados / 37`

### V4

Preservación:

`tests V1, V2 y V3 aprobados / 46`

## Cumplimiento del cambio nuevo

También se registra separadamente:

`tests de la versión actual aprobados / tests de la versión actual totales`

Por lo tanto:

- V2: tests nuevos aprobados / 7;
- V3: tests nuevos aprobados / 9;
- V4: tests nuevos aprobados / 20.

Esto permite distinguir entre:

- implementar correctamente el cambio nuevo;
- conservar correctamente el comportamiento anterior.

# 11. Evaluación específica de V4

V4 constituye la evolución de mayor complejidad del experimento.

Además de incorporar nuevas capacidades, obliga a preservar y combinar reglas
introducidas en versiones anteriores.

Se analizará especialmente:

- preservación de los 46 tests V1-V3;
- cumplimiento de los 20 tests nuevos;
- comportamiento ante revisiones creadas fuera de orden;
- acumulación de modificaciones parciales;
- conservación del historial;
- interacción entre reglas provenientes de diferentes versiones.

Esto permite evaluar si el contexto acumulado durante la evolución de la
funcionalidad adquiere mayor importancia cuando aumenta la cantidad de reglas e
interacciones que deben mantenerse simultáneamente.

# 12. Relación con el objetivo experimental

La comparación no se limita al resultado final.

Se observa la evolución de las métricas entre:

`V1 -> V2 -> V3 -> V4`

Especialmente:

- cumplimiento en primer intento;
- preservación en primer intento;
- cumplimiento del cambio nuevo;
- ciclos de corrección;
- intervenciones humanas;
- tiempo requerido.

V1, V2 y V3 permiten observar evoluciones progresivas relativamente acotadas.

V4 introduce una evolución transversal que requiere interpretar y mantener
simultáneamente reglas originadas en distintas etapas anteriores.

Esto permite analizar si el contexto estructurado y persistente utilizado por
SDD aporta mayor utilidad a medida que aumenta la complejidad evolutiva de la
funcionalidad.
