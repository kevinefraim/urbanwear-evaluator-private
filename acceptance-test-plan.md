# UrbanWear POC - Plan de Pruebas de Aceptación

## 1. Objetivo

La suite de aceptación constituye el mecanismo independiente utilizado para
evaluar las implementaciones generadas durante la prueba de concepto.

Los tests serán externos al repositorio utilizado por los agentes y evaluarán
únicamente el comportamiento observable de la API.

La suite no evaluará:

- estructura interna del código;
- nombres de clases;
- cantidad de archivos;
- existencia de documentación SDD;
- estilo de implementación;
- tests generados por el agente.

Se evaluará exclusivamente el cumplimiento funcional definido en el
ground truth.

# 2. Principio acumulativo

Las versiones serán evaluadas de manera acumulativa.

V1:

- tests correspondientes a V1.

V2:

- tests correspondientes a V1;
- tests nuevos correspondientes a V2.

V3:

- tests correspondientes a V1;
- tests correspondientes a V2;
- tests nuevos correspondientes a V3.

Esto permite medir dos dimensiones diferentes:

1. incorporación correcta del nuevo cambio;
2. preservación del comportamiento definido en versiones anteriores.

# 3. Resultado del primer intento

La primera ejecución de la suite se realizará inmediatamente después de que
el agente declare terminada una versión.

Este resultado deberá guardarse antes de proporcionar cualquier feedback.

Se registrarán:

- tests aprobados;
- tests totales;
- cumplimiento funcional;
- tests anteriores aprobados;
- preservación del comportamiento previo.

El objetivo es observar qué tan correctamente responde el agente al
requerimiento antes de recibir correcciones externas.

# 4. Resultado final

Luego de cada ciclo de corrección se volverá a ejecutar la suite completa.

Se permitirá un máximo de tres ciclos.

Al finalizar se guardará nuevamente:

- tests aprobados;
- tests totales;
- cumplimiento funcional;
- preservación;
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

Todos los tests V1 deberán continuar pasando.

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

Todos los tests V1 y V2 deberán continuar pasando.

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

# 8. Cantidad esperada de tests activos

V1:

30 tests

V2:

30 V1 + 7 V2 = 37 tests

V3:

30 V1 + 7 V2 + 9 V3 = 46 tests

# 9. Métricas derivadas

## Cumplimiento funcional

Cumplimiento =
tests activos aprobados / tests activos totales

## Preservación

En V2:

Preservación =
tests V1 aprobados / tests V1 totales

En V3:

Preservación =
tests V1 y V2 aprobados / tests V1 y V2 totales

## Cumplimiento del cambio nuevo

También se registrará separadamente:

tests de la versión actual aprobados /
tests de la versión actual totales

Esto permite distinguir entre:

- implementar correctamente el cambio nuevo;
- conservar correctamente el comportamiento anterior.

# 10. Relación con el objetivo experimental

La comparación no se limitará al resultado final.

Se observará la evolución de las métricas entre:

V1 -> V2 -> V3

Especialmente:

- cumplimiento en primer intento;
- preservación en primer intento;
- ciclos de corrección;
- intervenciones humanas;
- tiempo requerido.

Esto permitirá analizar si el contexto estructurado acumulado por SDD aporta
mayor utilidad a medida que aumenta la cantidad de cambios realizados sobre la
funcionalidad.
