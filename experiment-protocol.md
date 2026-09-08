# Protocolo Experimental

## 1. Objetivo

El objetivo del experimento es comparar dos formas de desarrollar y evolucionar
una misma funcionalidad de software con asistencia de un agente basado en
inteligencia artificial:

1. desarrollo mediante interacciones sucesivas;
2. desarrollo basado en Spec-Driven Development (SDD).

El interés principal no consiste únicamente en evaluar si una primera
implementación funciona correctamente, sino en analizar qué ocurre cuando la
funcionalidad evoluciona a través de múltiples versiones y acumula reglas de
negocio relacionadas entre sí.

La comparación busca observar si el contexto estructurado y persistente generado
mediante SDD aporta beneficios durante la evolución de la funcionalidad frente a
un enfoque donde el agente trabaja principalmente a partir del código existente
y del requerimiento correspondiente a cada nueva versión.

## 2. Caso de estudio

El experimento utiliza UrbanWear, una tienda online ficticia dedicada a la venta
de calzado urbano.

El backend inicial, denominado V0, incluye:

- productos;
- categorías;
- usuarios;
- carrito;
- checkout simulado;
- persistencia mediante SQLite.

V0 no posee funcionalidad de cupones.

El experimento parte siempre del mismo estado identificado mediante el tag:

`urbanwear-v0`

## 3. Enfoques comparados

### 3.1. Enfoque Prompt-Driven

En este enfoque el agente recibe:

- el repositorio correspondiente al estado actual de la funcionalidad;
- el requerimiento correspondiente a la nueva versión.

Cada versión comienza en una sesión nueva del agente.

No se conserva el historial de conversación de versiones anteriores.

El agente puede inspeccionar libremente el código existente para comprender el
comportamiento previamente implementado.

No se mantiene deliberadamente una especificación estructurada y persistente de
la funcionalidad entre versiones.

### 3.2. Enfoque basado en SDD

En este enfoque se utiliza el mismo agente, modelo y configuración.

El agente recibe:

- el repositorio correspondiente al estado actual;
- exactamente el mismo requerimiento entregado al enfoque Prompt-Driven;
- los artefactos SDD persistentes generados en versiones anteriores.

El proceso se organiza mediante artefactos como:

- especificación;
- plan;
- tareas;
- implementación;
- validación.

Las nuevas versiones actualizan o extienden los artefactos existentes.

Los artefactos SDD deben representar explícitamente qué requisitos:

- se agregan;
- se modifican;
- se eliminan;
- continúan vigentes.

El objetivo es que la información acumulada sobre la evolución de la
funcionalidad permanezca disponible de manera estructurada.

## 4. Trayectorias experimentales

Se utiliza una trayectoria independiente por enfoque.

### Prompt-Driven

`V0 -> V1 -> V2 -> V3 -> V4`

### SDD

`V0 -> V1 -> V2 -> V3 -> V4`

Ambas trayectorias comienzan exactamente desde `urbanwear-v0`.

Dentro de cada trayectoria, el código producido por una versión constituye el
punto de partida de la siguiente.

Por ejemplo:

`V1 -> V2 -> V3 -> V4`

no representa cuatro implementaciones independientes, sino una única
funcionalidad que evoluciona sucesivamente.

Cada versión utiliza una nueva sesión del agente.

## 5. Ajuste del diseño experimental

Durante la ejecución inicial del enfoque Prompt-Driven se observó cumplimiento
completo de los requisitos externos correspondientes a V1, V2 y V3, sin
regresiones funcionales y sin necesidad de ciclos de corrección.

Este comportamiento produjo un efecto techo en las primeras evoluciones, dado
que las modificaciones eran suficientemente acotadas como para ser resueltas a
partir del requerimiento actual y del código existente.

Antes de ejecutar V4 en cualquiera de los dos enfoques se decidió incorporar una
evolución adicional de mayor complejidad e interacción con requisitos
anteriores.

V4 fue definida y congelada antes de ser ejecutada por cualquiera de los dos
enfoques.

Asimismo, se decidió concentrar el experimento en una trayectoria longitudinal
por enfoque en lugar de realizar múltiples repeticiones independientes.

Esta decisión permite profundizar el análisis sobre la acumulación de contexto y
la evolución de una misma funcionalidad, aunque limita la posibilidad de
realizar inferencias estadísticas sobre la variabilidad entre ejecuciones.

Esta limitación deberá ser considerada al interpretar los resultados.

## 6. Versiones de la funcionalidad

### V1 - Cupones de descuento

Se incorpora la funcionalidad inicial de cupones.

Incluye:

- descuentos porcentuales;
- descuentos de monto fijo;
- vigencia;
- monto mínimo;
- restricciones por categoría;
- límite inicial de utilización por usuario;
- compatibilidad con checkout sin cupón.

### V2 - Evolución de las restricciones de uso

Se modifica la política de utilización.

Un usuario puede utilizar un mismo cupón:

- hasta tres veces en total;
- como máximo una vez por día calendario.

Los intentos rechazados no consumen una utilización.

Las utilizaciones son independientes entre usuarios.

### V3 - Restricción por usuarios habilitados

Se incorpora una lista opcional de usuarios autorizados.

Si un cupón posee `allowedUserIds`, únicamente dichos usuarios pueden utilizarlo.

Si la restricción no está presente, el cupón puede ser utilizado por cualquier
usuario que cumpla el resto de las reglas.

Esta autorización no reemplaza ni evita las validaciones anteriores.

### V4 - Evolución temporal de la configuración

Se incorpora la posibilidad de modificar cupones existentes mediante revisiones
de configuración.

V4 introduce:

- actualización parcial mediante `PATCH`;
- cambios inmediatos;
- cambios programados mediante `effectiveFrom`;
- activación y desactivación;
- límite total de usos configurable;
- conservación del historial entre configuraciones;
- interacción de las nuevas reglas con V1, V2 y V3.

V4 representa la evolución de mayor complejidad del experimento.
La complejidad de V4 incluye la existencia de múltiples revisiones futuras,
la creación de revisiones fuera de orden cronológico y la herencia parcial de
configuración según la línea temporal efectiva del cupón.

## 7. Condiciones controladas

Ambos enfoques deberán utilizar:

- el mismo proyecto V0;
- el mismo modelo;
- la misma configuración de razonamiento;
- la misma herramienta/agente;
- los mismos briefs;
- las mismas dependencias iniciales;
- la misma información disponible sobre UrbanWear;
- la misma suite externa de aceptación;
- las mismas reglas de intervención humana;
- el mismo límite de ciclos de corrección.

El modo de aprobación de acciones utilizado por el agente deberá mantenerse
igual durante toda la experiencia.

La suite externa no deberá ser visible para el agente.

## 8. Entrega de requerimientos

Existen cuatro archivos de entrada comunes:

- `input-briefs/v1.md`
- `input-briefs/v2.md`
- `input-briefs/v3.md`
- `input-briefs/v4.md`

El contenido correspondiente a cada versión debe entregarse de forma idéntica a
ambos enfoques.

Los briefs representan los requerimientos conocidos por el agente.

No deben incluir:

- casos de prueba externos;
- ground truth privado;
- resultados de ejecuciones anteriores;
- información sobre el desempeño del otro enfoque.

## 9. Sesiones del agente

Cada nueva versión comienza en una conversación nueva.

Por lo tanto:

- V1 usa una sesión nueva;
- V2 usa otra sesión nueva;
- V3 usa otra sesión nueva;
- V4 usa otra sesión nueva.

El historial conversacional de una versión anterior no se reutiliza.

En Prompt-Driven, la continuidad se produce principalmente a través del código.

En SDD, la continuidad se produce a través del código y de los artefactos SDD
persistentes.

## 10. Intervención humana

El desarrollador no puede editar manualmente el código durante una ejecución.

Puede:

- responder preguntas del agente;
- aclarar requerimientos;
- indicar errores detectados por el evaluador externo;
- solicitar una nueva corrección.

Cada mensaje enviado por el desarrollador después del requerimiento inicial se
considera una intervención humana.

Las aprobaciones automáticas de comandos o herramientas no cuentan como
intervención humana.

## 11. Resolución de ambigüedades

Las aclaraciones deberán basarse exclusivamente en el ground truth privado.

Si el agente realiza una pregunta cuyo comportamiento ya se encuentra definido
en el ground truth, se deberá responder utilizando esa definición.

La respuesta se registra como intervención humana.

Si aparece una ambigüedad no prevista en el ground truth, el experimento deberá
detenerse temporalmente.

Se deberá establecer una regla neutral antes de continuar y dicha regla deberá
aplicarse de igual manera a ambos enfoques.

No se deberá crear una regla diferente luego de observar el resultado de alguno
de los enfoques.

## 12. Evaluación externa

La evaluación oficial se realiza mediante una suite de tests independiente del
repositorio que modifica el agente.

El agente no tiene acceso a esta suite.

Los tests se ejecutan contra la API pública de UrbanWear.

Se evalúa el comportamiento como caja negra.

Los tests internos creados por el agente pueden utilizarse como herramienta de
desarrollo, pero no forman parte de la medición oficial.

## 13. Evaluación acumulativa

Cada versión debe preservar los requisitos todavía vigentes de versiones
anteriores.

Por este motivo, la suite es acumulativa.

Cantidad de tests funcionales:

- V1: 30
- V2: 30 anteriores + 7 nuevos = 37
- V3: 37 anteriores + 9 nuevos = 46
- V4: 46 anteriores + 20 nuevos = 66

Además existen tests de infraestructura asociados a V0 que no forman parte de la
métrica funcional principal.

## 14. Primer intento

Cuando el agente informa que considera terminada una implementación, se registra
el estado del repositorio antes de proporcionar cualquier resultado del
evaluador.

Sobre ese estado se ejecuta la suite externa.

Este resultado constituye el `first attempt`.

Debe preservarse mediante un commit y un tag específico.

## 15. Ciclos de corrección

Si existen tests fallidos, el agente puede recibir feedback y realizar hasta tres
ciclos de corrección.

Un ciclo de corrección comienza cuando se proporciona feedback al agente después
de una ejecución del evaluador externo.

Después de cada corrección se vuelve a ejecutar la suite.

El máximo permitido es:

`3 ciclos de corrección`

Si luego del tercer ciclo siguen existiendo fallos, la versión se considera
incompleta.

La siguiente versión continúa a partir del estado real alcanzado.

No se realizan reparaciones manuales para llevar el código artificialmente a un
estado correcto.

## 16. Correcciones del instrumento de evaluación

Si durante una ejecución se detecta un defecto en la propia suite externa que
penaliza un comportamiento válido no restringido por el requerimiento, la suite
puede ser corregida únicamente si:

- el problema pertenece al instrumento de evaluación;
- el agente todavía no recibió feedback basado en dicho fallo;
- la corrección se aplica posteriormente de manera idéntica a ambos enfoques;
- la modificación queda documentada.

Una corrección del evaluador no se considera ciclo de corrección del agente.

## 17. Métricas

### 17.1. Cumplimiento en primer intento

Se calcula antes de entregar feedback externo al agente.

`tests activos aprobados / total de tests activos`

### 17.2. Cumplimiento final

Se calcula después de finalizar la versión.

`tests activos aprobados / total de tests activos`

### 17.3. Preservación

Para V2, V3 y V4 se mide cuántos tests correspondientes a versiones anteriores
continúan funcionando.

Ejemplos:

V2:

`tests V1 aprobados / 30`

V3:

`tests V1 + V2 aprobados / 37`

V4:

`tests V1 + V2 + V3 aprobados / 46`

### 17.4. Cumplimiento del nuevo cambio

Se mide únicamente sobre los tests introducidos por la versión actual.

V2:

`tests nuevos aprobados / 7`

V3:

`tests nuevos aprobados / 9`

V4:

`tests nuevos aprobados / 20`

### 17.5. Ciclos de corrección

Cantidad de ciclos adicionales requeridos luego del primer intento.

### 17.6. Intervenciones humanas

Cantidad de mensajes enviados por el desarrollador luego del requerimiento
inicial.

### 17.7. Tiempo

Se registra el tiempo desde el envío del requerimiento de una versión hasta que:

- la implementación satisface la suite externa; o
- se alcanza el máximo de correcciones.

El tiempo de generación y mantenimiento de artefactos SDD forma parte del tiempo
del enfoque SDD.

### 17.8. Consumo del agente

El consumo de tokens, créditos u otra métrica equivalente únicamente se registra
si la herramienta utilizada expone dicha información de forma confiable y
comparable.

No se realizan estimaciones manuales.

## 18. Artefactos SDD

En la trayectoria SDD deben conservarse de manera persistente los artefactos
generados durante cada versión.

La estructura exacta puede depender de la herramienta utilizada, pero deberá
permitir identificar como mínimo:

- especificación vigente;
- modificaciones introducidas;
- plan de implementación;
- tareas;
- relación entre versiones.

Las especificaciones deberán evolucionar de manera incremental.

Los requisitos no modificados explícitamente continúan activos.

Cuando dos definiciones entren en conflicto, prevalece la modificación explícita
más reciente.

## 19. Registro de resultados

Cada versión deberá contar con un archivo privado de resultados.

Ejemplos:

- `results/prompt-run-1-v1.md`
- `results/prompt-run-1-v2.md`
- `results/prompt-run-1-v3.md`
- `results/prompt-run-1-v4.md`
- `results/sdd-run-1-v1.md`
- `results/sdd-run-1-v2.md`
- `results/sdd-run-1-v3.md`
- `results/sdd-run-1-v4.md`

Cada archivo deberá registrar como mínimo:

- enfoque;
- versión;
- hora de inicio;
- hora del primer intento;
- tiempo;
- tests anteriores aprobados;
- tests nuevos aprobados;
- cumplimiento acumulativo;
- intervenciones;
- ciclos de corrección;
- observaciones relevantes.

## 20. Versionado

El estado del código deberá registrarse mediante Git.

Se utilizarán tags para identificar:

- baseline V0;
- primer intento de cada versión;
- estado final de cada versión.

Ejemplo:

`prompt-run-1-v4-first`

`prompt-run-1-v4-final`

Si una versión pasa completamente en el primer intento, ambos tags pueden apuntar
al mismo commit.

## 21. Interpretación de resultados

El experimento no presupone que SDD deba obtener mejores resultados.

Son resultados válidos, entre otros:

- SDD obtiene mejor preservación;
- SDD necesita menos correcciones;
- SDD mejora su ventaja a medida que aumentan las evoluciones;
- ambos enfoques alcanzan la misma calidad funcional;
- Prompt-Driven resulta más rápido;
- el costo adicional de SDD no produce una mejora observable;
- las ventajas de SDD aparecen principalmente en trazabilidad y mantenimiento
  del contexto.

La conclusión deberá basarse exclusivamente en los resultados observados.

## 22. Limitaciones

El experimento utiliza:

- un único caso de estudio;
- una única funcionalidad;
- una trayectoria por enfoque;
- un agente/modelo determinado;
- un número limitado de evoluciones.

Por lo tanto, los resultados no pretenden constituir evidencia estadística
generalizable a todos los proyectos de software.

El experimento debe interpretarse como un estudio experimental controlado dentro
del contexto específico de UrbanWear.
