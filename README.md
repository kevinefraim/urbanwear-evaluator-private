# UrbanWear Evaluator POC

Materiales de evaluación para la POC de desarrollo guiado por especificaciones
de UrbanWear. El repositorio registra la estrategia de aceptación, los briefs
de entrada versionados, las pruebas de aceptación automatizadas, el protocolo
experimental y los resultados observados de las evoluciones de cupones V1 a V4.

> Este repositorio es público. Sus criterios de evaluación y material de
> referencia se incluyen deliberadamente para permitir una revisión transparente
> de la POC.

## Contenido

- [`input-briefs/`](input-briefs/): briefs provistos para cada versión.
- [`tests/`](tests/): pruebas de aceptación automatizadas.
- [`ground-truth.md`](ground-truth.md): comportamiento esperado del producto
  utilizado para la evaluación.
- [`acceptance-test-plan.md`](acceptance-test-plan.md): plan de pruebas y métricas.
- [`experiment-protocol.md`](experiment-protocol.md): procedimiento experimental.
- [`results/`](results/): especificaciones, prompts y resultados generados.

## Ejecutar las pruebas

Crear un entorno de Python, instalar las dependencias y ejecutar pytest:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
pytest
```

Las pruebas esperan que la aplicación UrbanWear esté disponible según la
configuración de [`tests/conftest.py`](tests/conftest.py).
