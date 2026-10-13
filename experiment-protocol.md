# UrbanWear POC - Protocolo Experimental

# 1. Objetivo

El experimento compara dos formas de desarrollar y evolucionar una misma
funcionalidad utilizando un agente de inteligencia artificial:

1. Prompt-Driven;
2. Desarrollo guiado por especificaciones (SDD).

El objetivo es analizar si disponer de contexto estructurado y persistente
mediante SDD aporta valor a medida que una funcionalidad acumula cambios y reglas
de negocio relacionadas.

No se presupone que alguno de los enfoques deba obtener mejores resultados.

# 2. Caso de estudio

El caso de estudio es UrbanWear, una tienda ficticia de calzado urbano.

V0 posee:

- productos;
- categorías;
- usuarios;
- carrito;
- checkout;
- SQLite.

V0 no posee cupones.

Ambas trayectorias comienzan exactamente desde:

`urbanwear-v0`

# 3. Trayectorias

Se utiliza una trayectoria por enfoque.

Prompt-Driven:

`V0 -> V1 -> V2 -> V3 -> V4`

SDD:

`V0 -> V1 -> V2 -> V3 -> V4`

Cada versión continúa sobre el código producido por la versión anterior de la
misma trayectoria.

# 4. Tickets

Los agentes reciben requerimientos redactados como tickets de desarrollo.

Los tickets describen:

- necesidad de negocio;
- alcance principal;
- contrato técnico mínimo cuando es necesario;
- cambios solicitados.

No constituyen especificaciones exhaustivas.

No incluyen todos los casos límite utilizados por la evaluación externa.

# 5. Enfoque Prompt-Driven

Para cada versión el agente dispone de:

- código actual;
- ticket actual.

Cada versión comienza en una sesión nueva.

No se conserva historial conversacional.

No se mantienen deliberadamente documentos estructurados de requisitos entre
versiones.

La principal fuente persistente de contexto es el repositorio.

# 6. Enfoque SDD

Para cada versión el agente dispone de:

- código actual;
- exactamente el mismo ticket que Prompt-Driven;
- artefactos SDD persistentes de versiones anteriores.

Los artefactos deben incluir al menos:

- especificación;
- plan;
- tareas.

Cada versión comienza en una sesión nueva.

El agente debe consultar y evolucionar los artefactos existentes.

# 7. Variable experimental

La diferencia entre enfoques es:

Prompt-Driven:

`código + ticket`

SDD:

`código + ticket + contexto SDD estructurado acumulado`

SDD no recibe reglas de negocio adicionales que no estén disponibles para el
otro enfoque mediante ticket, código o aclaraciones.

# 8. Condiciones controladas

Ambos enfoques utilizan:

- mismo V0;
- mismo agente;
- mismo modelo;
- misma configuración de razonamiento;
- mismo modo de aprobación;
- mismos tickets;
- misma referencia de evaluación;
- misma suite externa;
- mismas dependencias;
- misma posibilidad de solicitar aclaraciones;
- máximo de tres ciclos de corrección.

# 9. Sesiones

Cada versión utiliza una conversación nueva.

No se conserva historial conversacional entre versiones.

La persistencia entre versiones ocurre mediante:

Prompt-Driven:

- código.

SDD:

- código;
- especificaciones;
- planes;
- tareas.

# 10. Aclaraciones

Ambos enfoques pueden realizar preguntas cuando detecten una ambigüedad que
pueda modificar materialmente el comportamiento esperado.

Cuando se recibe una pregunta:

1. se consulta `ground-truth.md`;
2. se responde únicamente la información solicitada;
3. se registra la respuesta;
4. aumenta el contador de intervenciones;
5. aumenta el contador de aclaraciones.

No se proporcionan aclaraciones proactivamente.

# 11. Ambigüedad no prevista

Si aparece una decisión no definida en la referencia de evaluación:

1. se detiene la ejecución;
2. se define una regla neutral;
3. se documenta antes de continuar;
4. la misma regla pasa a ser válida para ambos enfoques.

No se crean reglas diferentes según el resultado de un enfoque.

# 12. Intervenciones humanas

Cada mensaje del desarrollador posterior al ticket inicial cuenta como
intervención.

Incluye:

- aclaraciones;
- respuestas a preguntas;
- comentarios del evaluador;
- solicitudes de corrección.

Las aprobaciones automáticas de herramientas no cuentan.

# 13. Edición manual

El desarrollador no modifica manualmente:

- código;
- tests internos del agente;
- artefactos SDD.

Las modificaciones durante la ejecución deben ser realizadas por el agente.

# 14. Evaluador externo

La suite de aceptación reside fuera del repositorio utilizado por el agente.

El agente no conoce:

- tests;
- referencia de evaluación;
- resultados esperados;
- resultados del otro enfoque.

La evaluación se realiza contra la API pública.

# 15. Suite acumulativa

V1:

30 tests.

V2:

37 tests acumulativos.

V3:

46 tests acumulativos.

V4:

66 tests acumulativos.

Existen además 2 tests de infraestructura V0.

La colección completa contiene:

68 tests.

# 16. Primer intento

Cuando el agente declara terminada la versión:

1. no se le proporcionan comentarios;
2. se registra la hora;
3. se crea un commit;
4. se crea un tag `first`;
5. se ejecuta la suite externa.

Ese resultado constituye el primer intento.

# 17. Ciclos de corrección

Si existen fallos, se permiten hasta tres ciclos de corrección.

Cada ciclo consiste en:

1. proporcionar comentarios;
2. permitir al agente modificar su solución;
3. ejecutar nuevamente el evaluador.

Cada ciclo cuenta como intervención humana.

# 18. Versión incompleta

Si luego del tercer ciclo continúan existiendo tests fallidos:

- la versión se considera incompleta;
- se registra el estado obtenido;
- la versión siguiente continúa desde ese estado.

No se realizan reparaciones humanas.

# 19. Métricas

## 19.1. Cumplimiento de primer intento

`tests aprobados / tests activos`

## 19.2. Cumplimiento final

`tests aprobados luego de correcciones / tests activos`

## 19.3. Preservación

V2:

`tests V1 aprobados / 30`

V3:

`tests V1-V2 aprobados / 37`

V4:

`tests V1-V3 aprobados / 46`

## 19.4. Cumplimiento del cambio nuevo

V2:

`tests V2 aprobados / 7`

V3:

`tests V3 aprobados / 9`

V4:

`tests V4 aprobados / 20`

## 19.5. Aclaraciones

Cantidad de preguntas de requisitos realizadas por el agente y respondidas por
el desarrollador.

## 19.6. Intervenciones

Cantidad total de mensajes posteriores al requerimiento inicial.

## 19.7. Ciclos de corrección

Cantidad de ciclos necesarios luego del primer intento.

## 19.8. Tiempo

Se mide desde el envío del ticket hasta:

- aprobación completa del evaluador; o
- finalización del tercer ciclo.

Para SDD se incluye el tiempo empleado en:

- análisis;
- especificación;
- planificación;
- tareas;
- implementación;
- validación.

## 19.9. Consumo

Tokens, créditos u otra medida solo se registra si la herramienta la expone de
forma confiable y comparable.

# 20. Artefactos SDD

Los artefactos SDD deben persistir en el repositorio.

Como mínimo:

`sdd/specs/`

`sdd/plans/`

`sdd/tasks/`

Cada nueva versión debe analizar el contexto anterior y reflejar:

- requisitos nuevos;
- requisitos modificados;
- requisitos que continúan vigentes;
- requisitos reemplazados.

No se evalúa SDD por cantidad de documentación.

El valor de sus artefactos se analiza en relación con los resultados de
evolución.

# 21. Correcciones del evaluador

Si se detecta un defecto en la suite:

puede corregirse únicamente antes de entregar comentarios al agente y siempre que:

- el test penalice un comportamiento válido;
- la referencia de evaluación no exija el comportamiento;
- la corrección se aplique a ambos enfoques.

Debe documentarse.

No cuenta como ciclo de corrección del agente.

# 22. Versionado

Se utilizan commits y tags para registrar:

- V0;
- primer intento;
- estado final.

Ejemplo:

`prompt-final-v2-first`

`prompt-final-v2-final`

Si no existen correcciones, ambos tags pueden apuntar al mismo commit.

# 23. Interpretación

La comparación considera conjuntamente:

- cumplimiento funcional;
- preservación;
- cumplimiento del cambio nuevo;
- aclaraciones;
- intervenciones;
- correcciones;
- tiempo.

Un enfoque puede presentar ventajas en determinadas métricas y costos en otras.

No se requiere que un único enfoque resulte superior en todas las dimensiones.

# 24. Limitaciones

La POC utiliza:

- un caso de estudio;
- una funcionalidad;
- cuatro evoluciones;
- una trayectoria por enfoque;
- un agente/modelo.

Los resultados describen este contexto experimental y no constituyen evidencia
estadística generalizable.
