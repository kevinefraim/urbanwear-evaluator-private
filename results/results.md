# Resultados de la POC

## 1. Resumen experimental

La POC comparó dos estrategias de desarrollo asistido por inteligencia
artificial para la evolución progresiva de una misma funcionalidad:

- Prompt-Driven Development;
- Spec-Driven Development (SDD).

Ambas trayectorias comenzaron desde el mismo baseline V0 de UrbanWear y
recibieron los mismos tickets funcionales para V1, V2, V3 y V4.

Cada versión se ejecutó en una nueva conversación con el agente.

La principal diferencia experimental fue el contexto persistente disponible:

- Prompt-Driven conservó principalmente el código generado en las versiones
  anteriores.
- SDD conservó el código junto con especificaciones, planes y tareas
  estructuradas dentro del repositorio.

La evaluación funcional se realizó mediante una suite externa no visible para
el agente.

La suite acumulativa estuvo compuesta por:

- V1: 30 tests;
- V2: 37 tests;
- V3: 46 tests;
- V4: 66 tests.

Además existieron 2 tests de infraestructura correspondientes a V0.

## 2. Resultados Prompt-Driven

### 2.1. V1

- Tiempo inicial: ~5 min
- First attempt: 29/30
- Cumplimiento first attempt: 96.67%
- Aclaraciones: 0
- Intervenciones humanas: 1
- Ciclos de corrección: 1
- Tiempo de corrección: ~2 min
- Resultado final: 30/30
- Cumplimiento final: 100%
- Tiempo de trabajo del agente registrado: ~7 min

El único fallo del primer intento estuvo relacionado con `validUntil`.

El agente interpretó el límite final de vigencia de forma no inclusiva sin
solicitar una aclaración previa.

Luego de indicarle que `validUntil` debía considerarse inclusivo, corrigió el
comportamiento en un ciclo y alcanzó el 100% de cumplimiento.

### 2.2. V2

- Tiempo inicial: ~5 min
- First attempt: 37/37
- Cumplimiento first attempt: 100%
- Preservación V1: 30/30
- Cumplimiento del cambio V2: 7/7
- Aclaraciones: 3
- Intervenciones humanas: 1
- Ciclos de corrección: 0
- Resultado final: 37/37
- Tiempo de trabajo del agente registrado: ~5 min

Antes de implementar, el agente solicitó definición de:

1. máximo total de usos;
2. máximo diario de usos;
3. zona horaria utilizada para determinar el día calendario.

Se definieron:

- 3 usos exitosos totales por usuario y cupón;
- 1 uso exitoso por día;
- utilización de UTC para determinar el día calendario.

La implementación alcanzó el 100% en el primer intento y preservó completamente
V1.

### 2.3. V3

- Tiempo inicial: ~4 min
- First attempt: 46/46
- Cumplimiento first attempt: 100%
- Preservación V1-V2: 37/37
- Cumplimiento del cambio V3: 9/9
- Aclaraciones: 0
- Intervenciones humanas: 0
- Ciclos de corrección: 0
- Resultado final: 46/46
- Tiempo de trabajo del agente registrado: ~4 min

El agente incorporó la segmentación mediante `allowedUserIds` sin solicitar
aclaraciones adicionales.

La interpretación adoptada fue compatible con el comportamiento esperado y no
se produjeron regresiones.

### 2.4. V4

- Tiempo inicial: ~7 min
- First attempt: 66/66
- Cumplimiento first attempt: 100%
- Preservación V1-V3: 46/46
- Cumplimiento del cambio V4: 20/20
- Aclaraciones: 0
- Intervenciones humanas: 0
- Ciclos de corrección: 0
- Resultado final: 66/66
- Tiempo de trabajo del agente registrado: ~7 min

La implementación Prompt-Driven incorporó correctamente en el primer intento la
evolución temporal de cupones.

También resolvió correctamente los casos de múltiples revisiones, revisiones
creadas fuera de orden, herencia parcial, preservación del historial y
composición de reglas anteriores.

No fueron necesarias aclaraciones ni correcciones.

## 3. Resultados Spec-Driven Development

### 3.1. V1

- Tiempo inicial: ~7 min
- First attempt: 28/30
- Cumplimiento first attempt: 93.33%
- Aclaraciones: 5
- Intervenciones humanas: 4
- Ciclos de corrección: 2
- Resultado final: 30/30
- Cumplimiento final: 100%
- Tiempo de trabajo del agente registrado: ~9 min

Antes de implementar, el agente solicitó aclaraciones sobre:

- política de reutilización;
- comportamiento con categorías;
- valores válidos de `type`;
- límite del descuento fijo;
- evaluación de `minimumAmount`.

Estas decisiones fueron incorporadas a los artefactos SDD.

Sin embargo, el first attempt presentó dos fallos:

1. se aceptó un descuento porcentual superior a 100%;
2. `validUntil` no fue considerado inclusivo.

El primer ciclo corrigió el rango porcentual pero el problema de vigencia
continuó.

Fue necesario un segundo ciclo para corregir completamente la interpretación de
`validUntil`.

El resultado final fue 30/30.

### 3.2. V2

- Tiempo inicial: ~5 min
- First attempt: 37/37
- Cumplimiento first attempt: 100%
- Preservación V1: 30/30
- Cumplimiento del cambio V2: 7/7
- Aclaraciones: 3
- Intervenciones humanas: 1
- Ciclos de corrección: 0
- Resultado final: 37/37
- Tiempo de trabajo del agente registrado: ~5 min

El agente consultó las mismas tres decisiones principales de negocio que habían
aparecido durante la trayectoria Prompt-Driven:

- máximo total;
- máximo diario;
- zona horaria.

Estas decisiones quedaron registradas dentro de la especificación persistente de
V2.

La implementación obtuvo 37/37 en el primer intento.

### 3.3. V3

- Tiempo inicial: ~4 min
- First attempt: 46/46
- Cumplimiento first attempt: 100%
- Preservación V1-V2: 37/37
- Cumplimiento del cambio V3: 9/9
- Aclaraciones: 0
- Intervenciones humanas: 0
- Ciclos de corrección: 0
- Resultado final: 46/46
- Tiempo de trabajo del agente registrado: ~4 min

La segmentación de clientes fue incorporada correctamente y no produjo
regresiones.

No fueron necesarias aclaraciones ni correcciones.

### 3.4. V4

- Tiempo inicial: ~5 min
- First attempt: 66/66
- Cumplimiento first attempt: 100%
- Preservación V1-V3: 46/46
- Cumplimiento del cambio V4: 20/20
- Aclaraciones: 7
- Intervenciones humanas: 2
- Ciclos de corrección: 0
- Resultado final: 66/66
- Tiempo de trabajo del agente registrado: ~5 min

Antes de implementar V4, el proceso SDD hizo explícitas diferentes decisiones
relacionadas con:

- campos modificables mediante PATCH;
- inmutabilidad del código;
- comportamiento de `effectiveFrom`;
- cambios inmediatos y programados;
- exposición de revisiones programadas;
- `maxUsesPerUser`;
- `active`;
- preservación de reglas anteriores.

Estas definiciones fueron incorporadas a los artefactos SDD.

La implementación alcanzó 66/66 tests en el primer intento y preservó
completamente el comportamiento anterior.

## 4. Comparación por versión

| Versión | Prompt first attempt | SDD first attempt | Prompt final | SDD final |
| ------- | -------------------: | ----------------: | -----------: | --------: |
| V1      |       29/30 (96.67%) |    28/30 (93.33%) |        30/30 |     30/30 |
| V2      |         37/37 (100%) |      37/37 (100%) |        37/37 |     37/37 |
| V3      |         46/46 (100%) |      46/46 (100%) |        46/46 |     46/46 |
| V4      |         66/66 (100%) |      66/66 (100%) |        66/66 |     66/66 |

## 5. Preservación del comportamiento

| Evolución         | Prompt |   SDD |
| ----------------- | -----: | ----: |
| V2 preserva V1    |  30/30 | 30/30 |
| V3 preserva V1-V2 |  37/37 | 37/37 |
| V4 preserva V1-V3 |  46/46 | 46/46 |

Ambos enfoques alcanzaron una preservación funcional del 100% en todas las
evoluciones evaluadas.

## 6. Cumplimiento de requisitos nuevos

| Versión | Tests nuevos | Prompt |   SDD |
| ------- | -----------: | -----: | ----: |
| V2      |            7 |    7/7 |   7/7 |
| V3      |            9 |    9/9 |   9/9 |
| V4      |           20 |  20/20 | 20/20 |

No se observaron diferencias funcionales en los requisitos incorporados desde
V2 hasta V4.

## 7. Aclaraciones e intervenciones

| Métrica                            | Prompt-Driven |    SDD |
| ---------------------------------- | ------------: | -----: |
| Aclaraciones V1                    |             0 |      5 |
| Aclaraciones V2                    |             3 |      3 |
| Aclaraciones V3                    |             0 |      0 |
| Aclaraciones V4                    |             0 |      7 |
| **Aclaraciones totales**           |         **3** | **15** |
| **Intervenciones humanas totales** |         **2** |  **7** |
| **Ciclos de corrección totales**   |         **1** |  **2** |

SDD produjo una mayor cantidad de explicitaciones de requisitos.

Esto fue especialmente visible en V1 y V4, donde el agente detuvo la
implementación para solicitar definiciones antes de consolidar la
especificación.

Sin embargo, la mayor cantidad de aclaraciones no se tradujo automáticamente en
un mayor cumplimiento funcional: en V1 el first attempt de SDD obtuvo un test
menos que Prompt-Driven.

## 8. Tiempo registrado

| Versión              | Prompt-Driven |         SDD |
| -------------------- | ------------: | ----------: |
| V1                   |        ~7 min |      ~9 min |
| V2                   |        ~5 min |      ~5 min |
| V3                   |        ~4 min |      ~4 min |
| V4                   |        ~7 min |      ~5 min |
| **Total registrado** |   **~23 min** | **~23 min** |

Los valores representan el tiempo aproximado de trabajo del agente registrado
durante las ejecuciones y ciclos de corrección.

No incluyen una medición precisa del costo computacional interno ni deben
interpretarse como benchmarks de rendimiento del modelo.

En el total acumulado no se observó una diferencia temporal relevante entre
ambos enfoques, aunque la distribución fue diferente.

SDD presentó mayor overhead inicial en V1, mientras que V4 fue completada en
menos tiempo registrado que la trayectoria Prompt-Driven.

## 9. Síntesis comparativa

Los dos enfoques alcanzaron finalmente el 100% de cumplimiento funcional en
todas las versiones.

Prompt-Driven obtuvo un mejor resultado en el first attempt de V1:

- Prompt: 29/30;
- SDD: 28/30.

Desde V2 hasta V4 ambos enfoques alcanzaron el 100% en el primer intento.

Tampoco se observaron diferencias en preservación funcional: ambas trayectorias
mantuvieron todos los comportamientos anteriores durante las sucesivas
evoluciones.

La diferencia más marcada apareció en el tratamiento explícito de requisitos.

SDD realizó 15 aclaraciones frente a 3 de Prompt-Driven y mantuvo esas
decisiones como artefactos persistentes de especificación, planificación y
tareas.

Esto permitió disponer de una representación explícita del conocimiento
funcional acumulado, aunque dentro de esta POC dicha ventaja documental no
produjo una mejora observable en la tasa de aprobación de los tests externos.

En términos temporales, ambos enfoques acumularon aproximadamente 23 minutos de
trabajo registrado del agente.

## 10. Interpretación de resultados

Los resultados no muestran una superioridad funcional general de SDD sobre el
enfoque Prompt-Driven para el caso evaluado.

El código existente y los tickets proporcionaron contexto suficiente para que
Prompt-Driven preservara correctamente la funcionalidad incluso durante la
evolución compleja de V4.

Al mismo tiempo, SDD mostró un comportamiento diferente durante el análisis de
requisitos.

La obligación de mantener una especificación persistente llevó al agente a
identificar y consultar una mayor cantidad de decisiones de negocio antes de
implementar, especialmente en V4.

Por lo tanto, el principal valor observado de SDD en esta experiencia no estuvo
en una mayor tasa de aprobación funcional, sino en la explicitación y
persistencia del contexto utilizado para desarrollar la funcionalidad.

También se observó que esa mayor formalización no garantiza por sí sola la
ausencia de errores. V1 constituye un ejemplo: pese a realizar más aclaraciones,
SDD presentó dos fallos en su primer intento y necesitó dos ciclos de
corrección.

## 11. Conclusión experimental

Dentro de las condiciones de esta POC, ambas estrategias fueron capaces de
desarrollar y evolucionar exitosamente la funcionalidad de cupones.

Prompt-Driven resultó suficiente para preservar el comportamiento funcional a
lo largo de las cuatro versiones y presentó resultados equivalentes o
superiores en first attempt.

SDD no produjo una mejora funcional cuantitativa sobre la suite de aceptación,
pero generó un conjunto persistente y estructurado de requisitos, decisiones,
planes y tareas que no estuvo disponible en la trayectoria Prompt-Driven.

Esto sugiere que el valor agregado de SDD puede encontrarse principalmente en
la gestión explícita del contexto y la trazabilidad de decisiones, mientras que
su impacto sobre la calidad funcional inmediata depende del tipo y escala del
problema.

En un sistema acotado como UrbanWear, el código existente resultó una fuente de
contexto suficiente para que un agente pudiera reconstruir gran parte de las
reglas previas.

En sistemas de mayor tamaño, con más funcionalidades, mayor separación temporal
entre cambios o participación de múltiples desarrolladores, la persistencia
estructurada ofrecida por SDD podría adquirir mayor relevancia.

## 12. Limitaciones

Los resultados deben interpretarse dentro de las limitaciones de la experiencia:

- se utilizó un único caso de estudio;
- se evaluó una única funcionalidad;
- existieron cuatro etapas de evolución;
- se realizó una trayectoria por enfoque;
- se utilizó el mismo agente/modelo;
- la muestra no permite realizar inferencias estadísticas generales;
- los tiempos fueron registrados manualmente de forma aproximada;
- la calidad documental de los artefactos SDD no fue evaluada mediante una
  métrica cuantitativa independiente.

Los resultados representan evidencia del comportamiento observado en esta POC,
no una demostración de superioridad general de uno de los enfoques.
