# UrbanWear Evaluator POC

Evaluation materials for the UrbanWear specification-driven development POC.
The repository records the acceptance strategy, versioned input briefs,
automated acceptance tests, experiment protocol, and observed results for the
coupon evolutions V1 through V4.

> This repository is public. Its evaluation criteria and ground-truth material
> are intentionally included for transparent review of the POC.

## Contents

- [`input-briefs/`](input-briefs/): briefs provided for each version.
- [`tests/`](tests/): automated acceptance tests.
- [`ground-truth.md`](ground-truth.md): expected product behavior used for
  evaluation.
- [`acceptance-test-plan.md`](acceptance-test-plan.md): test plan and metrics.
- [`experiment-protocol.md`](experiment-protocol.md): experimental procedure.
- [`results/`](results/): generated specifications, prompts, and results.

## Run the tests

Create a Python environment, install the dependencies, and run pytest:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
pytest
```

The tests expect the UrbanWear application to be available according to the
configuration in [`tests/conftest.py`](tests/conftest.py).
