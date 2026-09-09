# UrbanWear POC - Plan de Pruebas de Aceptación

# 1. Objetivo

La suite externa evalúa el comportamiento funcional producido por los agentes.

Los tests se encuentran fuera del repositorio utilizado durante el desarrollo.

No evalúan:

- arquitectura interna;
- nombres de clases;
- cantidad de archivos;
- estilo;
- documentación;
- artefactos SDD;
- tests internos.

Evalúan exclusivamente comportamiento observable.

# 2. Tickets y ground truth

Los tickets representan requerimientos de desarrollo y no especificaciones
exhaustivas.

El ground truth contiene las decisiones funcionales utilizadas para construir la
suite.

Cuando una decisión no resulte evidente a partir del ticket, ambos enfoques
pueden solicitar aclaraciones.

Esto permite observar también la capacidad del proceso para detectar requisitos
que necesitan definición.

# 3. Evaluación acumulativa

V1:

tests V1.

V2:

tests V1 + V2.

V3:

tests V1 + V2 + V3.

V4:

tests V1 + V2 + V3 + V4.

# 4. First attempt

La primera ejecución se realiza inmediatamente después de que el agente declara
terminada una versión.

Se registra antes de entregar feedback:

- tests aprobados;
- tests activos;
- preservación;
- cumplimiento del nuevo cambio.

# 5. Resultado final

Después de cada corrección se ejecuta nuevamente la suite.

Máximo:

3 ciclos.

Se registra:

- cumplimiento final;
- preservación;
- cumplimiento del nuevo cambio;
- ciclos;
- intervenciones.

# 6. V1

## Creación y consulta

### TEST-V1-01

Crear cupón porcentual válido.

### TEST-V1-02

Crear cupón fijo válido.

### TEST-V1-03

Rechazar código duplicado.

### TEST-V1-04

Consultar cupón existente.

### TEST-V1-05

Cupón inexistente responde como recurso no encontrado.

## Porcentaje

### TEST-V1-06

Aplicar descuento porcentual.

### TEST-V1-07

Aceptar porcentaje 100.

### TEST-V1-08

Rechazar porcentaje inválido.

## Monto fijo

### TEST-V1-09

Aplicar descuento fijo.

### TEST-V1-10

Evitar total negativo.

## Vigencia

### TEST-V1-11

Aceptar dentro de vigencia.

### TEST-V1-12

Rechazar antes del inicio.

### TEST-V1-13

Rechazar luego del vencimiento.

### TEST-V1-14

Fecha inicial inclusiva.

### TEST-V1-15

Fecha final inclusiva.

## Monto mínimo

### TEST-V1-16

Rechazar subtotal inferior al mínimo.

### TEST-V1-17

Aceptar subtotal igual al mínimo.

### TEST-V1-18

Evaluar mínimo antes del descuento.

## Categorías

### TEST-V1-19

Aplicar descuento a categoría permitida.

### TEST-V1-20

Carrito mixto descuenta solo productos elegibles.

### TEST-V1-21

Rechazar si no existe producto elegible.

### TEST-V1-22

Sin restricciones aplica a todo el carrito.

## Uso

### TEST-V1-23

Permitir primer uso.

### TEST-V1-24

Rechazar segundo uso en V1.

### TEST-V1-25

Usuarios independientes.

### TEST-V1-26

Intento fallido no consume uso.

## Compatibilidad

### TEST-V1-27

Checkout sin cupón funciona.

### TEST-V1-28

Subtotal y total iguales sin cupón.

### TEST-V1-29

Checkout crea orden.

### TEST-V1-30

Checkout vacía carrito.

# 7. V2

Todos los tests V1 deben continuar pasando.

### TEST-V2-01

Rechazar dos usos el mismo día.

### TEST-V2-02

Permitir segundo uso en día posterior.

### TEST-V2-03

Permitir tercer uso.

### TEST-V2-04

Rechazar cuarto uso.

### TEST-V2-05

Mantener contador independiente entre usuarios.

### TEST-V2-06

Intento fallido no incrementa total.

### TEST-V2-07

Intento fallido no bloquea posterior uso válido del mismo día.

# 8. V3

Todos los tests V1 y V2 deben continuar pasando.

### TEST-V3-01

Cupón sin segmentación continúa siendo general.

### TEST-V3-02

Usuario permitido puede utilizarlo.

### TEST-V3-03

Usuario no permitido es rechazado.

### TEST-V3-04

Rechazo por autorización no consume uso.

### TEST-V3-05

Usuario permitido sigue sujeto a vigencia.

### TEST-V3-06

Usuario permitido sigue sujeto a mínimo.

### TEST-V3-07

Usuario permitido sigue sujeto a categorías.

### TEST-V3-08

Usuario permitido sigue sujeto a límite diario.

### TEST-V3-09

Usuario permitido sigue sujeto a límite total.

# 9. V4

Todos los tests V1-V3 deben continuar pasando.

## Actualización parcial

### TEST-V4-01

PATCH parcial conserva campos omitidos.

### TEST-V4-02

Código inmutable.

### TEST-V4-03

Cambio inmediato de descuento.

### TEST-V4-04

Cambio inmediato de mínimo.

### TEST-V4-05

Cambio inmediato de categorías.

### TEST-V4-06

Cambio inmediato de usuarios.

## Revisiones temporales

### TEST-V4-07

Cambio futuro no se aplica antes de effectiveFrom.

### TEST-V4-08

Cambio se aplica exactamente en effectiveFrom.

## Activación

### TEST-V4-09

active=false bloquea uso.

### TEST-V4-10

Reactivación permite uso.

### TEST-V4-11

Desactivar y reactivar conserva historial.

## Límite configurable

### TEST-V4-12

maxUsesPerUser modifica máximo.

### TEST-V4-13

Reducir máximo considera historial.

## Historial y compatibilidad

### TEST-V4-14

Nueva revisión no reinicia límite diario.

### TEST-V4-15

Cupón sin revisiones continúa siendo compatible.

## Línea temporal compleja

### TEST-V4-16

Revisiones parciales futuras acumulan cambios.

### TEST-V4-17

Orden cronológico prevalece sobre orden de creación.

### TEST-V4-18

Inserción de revisión intermedia conserva herencia temporal.

### TEST-V4-19

Reglas originadas en diferentes versiones se combinan.

### TEST-V4-20

Historial permanece intacto entre múltiples revisiones.

# 10. Cantidad de tests

V1:

30

V2:

37 acumulativos.

V3:

46 acumulativos.

V4:

66 acumulativos.

Infraestructura:

2.

Colección completa:

68.

# 11. Métricas

## Cumplimiento

`tests aprobados / tests activos`

## Preservación V2

`tests V1 aprobados / 30`

## Preservación V3

`tests V1-V2 aprobados / 37`

## Preservación V4

`tests V1-V3 aprobados / 46`

## Cambio V2

`tests V2 aprobados / 7`

## Cambio V3

`tests V3 aprobados / 9`

## Cambio V4

`tests V4 aprobados / 20`

# 12. Interpretación

La suite permite distinguir entre:

- implementación del nuevo requerimiento;
- preservación del comportamiento previo.

Los resultados se combinan con:

- aclaraciones;
- intervenciones;
- correcciones;
- tiempo.

Los artefactos SDD no son evaluados directamente por esta suite.
