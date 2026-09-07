# UrbanWear SDD POC - Protocolo Experimental

## 1. Objetivo

El objetivo del experimento es comparar dos formas de desarrollar y evolucionar
una misma funcionalidad asistida por un agente de inteligencia artificial:

1. desarrollo mediante interacciones sucesivas con prompts;
2. desarrollo basado en Spec-Driven Development.

La comparación se centrará en observar si conservar contexto estructurado y
persistente mediante SDD produce diferencias medibles cuando una funcionalidad
evoluciona a través de cambios sucesivos.

El experimento no parte de la suposición de que SDD debe obtener mejores
resultados.

# 2. Caso de estudio

Se utilizará UrbanWear, un backend ficticio de una tienda de calzado urbano.

El estado inicial del sistema se encuentra congelado mediante el tag:

urbanwear-v0

Este estado no contiene soporte para cupones.

Todas las ejecuciones del experimento deben comenzar a partir de este mismo
baseline.

# 3. Enfoques evaluados

## 3.1 Prompt-driven

El agente podrá:

- inspeccionar el repositorio;
- modificar código;
- crear archivos;
- ejecutar comandos;
- ejecutar tests internos;
- solicitar aclaraciones;
- recibir pedidos de corrección.

No se utilizará una especificación estructurada y persistente de la
funcionalidad.

Cada nueva versión comenzará en una sesión nueva con el agente.

El agente dispondrá de:

- el código correspondiente a la versión anterior;
- el requerimiento correspondiente a la nueva versión.

No dispondrá del historial de conversación de las versiones anteriores.

## 3.2 Spec-Driven Development

El agente tendrá las mismas capacidades que en el enfoque Prompt-driven.

La diferencia será la utilización de los siguientes artefactos persistentes:

- especificación;
- plan de implementación;
- tareas.

El proceso esperado será:

requerimiento
-> especificación
-> plan
-> tareas
-> implementación
-> validación

Cada nueva versión comenzará también en una sesión nueva.

Además del código y del nuevo requerimiento, el agente tendrá acceso a los
artefactos SDD generados durante las versiones anteriores.

# 4. Evolución de la funcionalidad

Cada trayectoria debe evolucionar de manera secuencial:

V1 -> V2 -> V3

## V1

Implementación inicial de cupones.

Incluye:

- descuento porcentual;
- descuento fijo;
- período de vigencia;
- monto mínimo;
- restricción por categoría;
- límite de uso por usuario.

## V2

Modifica la política de uso.

Cada usuario podrá utilizar un mismo cupón:

- hasta tres veces en total;
- como máximo una vez por día calendario.

Todos los demás requerimientos continúan vigentes.

## V3

Agrega la posibilidad de restringir un cupón a determinados usuarios.

Todos los requerimientos anteriores no modificados continúan vigentes.

# 5. Trayectorias experimentales

Se realizarán cuatro trayectorias completas:

- prompt-run-1;
- prompt-run-2;
- sdd-run-1;
- sdd-run-2.

Cada trayectoria comenzará desde urbanwear-v0.

Cada trayectoria conservará únicamente el código producido por sus propias
versiones anteriores.

No se copiarán soluciones entre trayectorias.

# 6. Condiciones controladas

Las siguientes condiciones deben mantenerse iguales entre ambos enfoques:

- mismo código inicial;
- mismo agente;
- mismo modelo;
- mismo nivel de razonamiento;
- mismos requerimientos funcionales;
- mismas dependencias iniciales;
- mismo conjunto de datos iniciales;
- mismas reglas de interacción humana;
- misma suite externa de evaluación;
- mismo máximo de ciclos de corrección.

El modelo y la configuración seleccionados al iniciar el experimento no deben
modificarse hasta finalizar las cuatro trayectorias.

# 7. Interacción humana

El desarrollador podrá:

- enviar el requerimiento inicial;
- responder preguntas del agente;
- solicitar correcciones;
- informar fallas funcionales detectadas por la evaluación externa.

El desarrollador no podrá:

- modificar manualmente el código;
- resolver errores directamente;
- mostrar el código de los tests externos;
- mostrar el ground truth;
- entregar una implementación de referencia.

Cada mensaje enviado después del requerimiento inicial se contabilizará como
una intervención humana.

# 8. Aclaraciones

Las aclaraciones deberán responderse utilizando exclusivamente el ground truth
previamente definido.

Si ambos enfoques realizan la misma pregunta, deberán recibir la misma
información funcional.

Si aparece una ambigüedad no contemplada en el ground truth:

1. se pausa la ejecución;
2. se define una respuesta neutral;
3. la nueva regla se documenta;
4. debe aplicarse de la misma manera a ambos enfoques.

No se debe decidir una nueva regla en función del resultado obtenido por uno
de los enfoques.

# 9. Evaluación externa

La suite de aceptación será independiente del proyecto visible para el agente.

Los agentes no tendrán acceso a:

- ground-truth.md;
- tests externos;
- evaluator;
- resultados de otras ejecuciones.

La evaluación se realizará mediante la API pública de UrbanWear.

Los tests serán black-box y no dependerán de la estructura interna elegida por
el agente.

# 10. Evaluación acumulativa

Los tests serán acumulativos.

V1:

tests V1

V2:

tests V1 + tests V2

V3:

tests V1 + tests V2 + tests V3

Esto permitirá evaluar tanto la implementación del nuevo cambio como la
preservación de comportamientos anteriores.

# 11. Ciclos de corrección

Cuando el agente declare terminada una versión:

1. se ejecutará la suite externa;
2. se registrarán los resultados;
3. si existen fallas, se informará únicamente el comportamiento funcional que
   no fue satisfecho;
4. el agente podrá realizar una corrección;
5. se ejecutará nuevamente la suite.

Se permitirá un máximo de tres ciclos de corrección por versión.

Si después del tercer ciclo continúan existiendo fallas, la versión será
registrada como incompleta.

# 12. Continuidad entre versiones

Una versión incompleta no será corregida manualmente antes de continuar.

La siguiente versión deberá partir del estado realmente alcanzado por la
trayectoria anterior.

Esto permite observar posibles efectos acumulativos durante la evolución.

# 13. Métricas

## 13.1 Cumplimiento funcional

C = tests aprobados / tests activos

Se expresará como porcentaje.

## 13.2 Preservación del comportamiento previo

Para V2 y V3:

P = tests anteriores aprobados / tests anteriores totales

Se expresará como porcentaje.

## 13.3 Ciclos de corrección

Cantidad de iteraciones adicionales realizadas después de evaluar la primera
implementación presentada por el agente.

## 13.4 Intervenciones humanas

Cantidad de mensajes enviados por el desarrollador después del requerimiento
inicial.

## 13.5 Tiempo

Se medirá desde el envío del requerimiento correspondiente a una versión hasta:

- superar la suite externa; o
- alcanzar el máximo de tres ciclos de corrección.

El tiempo incluye interacción real con el agente.

Las interrupciones personales ajenas al experimento deben excluirse de la
medición.

## 13.6 Uso del agente

Se registrará consumo de tokens, créditos u otra métrica equivalente cuando la
herramienta permita obtenerla de forma comparable.

Si la herramienta no permite obtener este dato de manera confiable, la métrica
será considerada opcional y no se estimará manualmente.

# 14. Registro de cada ejecución

Para cada combinación de trayectoria y versión deberán registrarse:

- approach;
- run;
- version;
- hora de inicio;
- hora de finalización;
- tests aprobados;
- tests totales;
- tests previos aprobados;
- tests previos totales;
- ciclos de corrección;
- intervenciones humanas;
- tiempo total;
- uso del agente, si está disponible;
- observaciones.

También deberán conservarse las conversaciones completas con el agente cuando
la herramienta permita exportarlas o registrarlas.

# 15. Tests internos

El agente podrá crear tests internos dentro del repositorio.

Estos tests forman parte de su proceso de desarrollo.

No serán utilizados como métrica oficial del experimento.

Los resultados oficiales serán los obtenidos mediante la suite externa.

# 16. Finalización de una versión

Una versión se considera válida cuando todos los tests externos activos son
superados.

Una versión se considera incompleta cuando alcanza el máximo de tres ciclos de
corrección y todavía existen tests externos fallidos.

# 17. Congelamiento del protocolo

Este protocolo debe considerarse congelado antes de comenzar Prompt Run 1 V1.

No deberá modificarse después de observar resultados parciales con el objetivo
de favorecer o perjudicar alguno de los enfoques.

Cualquier modificación inevitable deberá documentarse explícitamente y
justificarse en el análisis final de la prueba de concepto.
