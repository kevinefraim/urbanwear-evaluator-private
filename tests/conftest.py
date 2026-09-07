import os
import time
import uuid
import subprocess

import pytest
import requests


PROJECT_PATH = r"C:\Users\Kevin Efraim\OneDrive\urbanwear-sdd-poc\urbanwear"
PORT = "3100"


class UrbanWearServer:
    def __init__(self):
        self.base_url = f"http://localhost:{PORT}"
        self.db_path = os.path.join(
            PROJECT_PATH,
            f"evaluator-{uuid.uuid4().hex}.db"
        )
        self.process = None

    def __str__(self):
        return self.base_url

    def _env(self, now):
        env = os.environ.copy()
        env["PORT"] = PORT
        env["DATABASE_PATH"] = self.db_path
        env["TEST_NOW"] = now
        return env

    def reset(self):
        result = subprocess.run(
            "pnpm reset:seed",
            cwd=PROJECT_PATH,
            shell=True,
            env=self._env("2026-09-10T12:00:00.000Z"),
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"No se pudo resetear la base:\n"
                f"{result.stdout}\n{result.stderr}"
            )

    def start(self, now="2026-09-10T12:00:00.000Z"):
        self.process = subprocess.Popen(
            "pnpm start",
            cwd=PROJECT_PATH,
            shell=True,
            env=self._env(now),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for _ in range(40):
            try:
                response = requests.get(
                    f"{self.base_url}/products",
                    timeout=1
                )

                if response.status_code == 200:
                    return
            except requests.RequestException:
                pass

            time.sleep(0.2)

        self.stop()
        raise RuntimeError("UrbanWear no pudo iniciarse")

    def stop(self):
        if self.process is not None:
            subprocess.run(
                f"taskkill /PID {self.process.pid} /T /F",
                shell=True,
                capture_output=True
            )
            self.process = None

            time.sleep(0.3)

    def restart(self, now):
        self.stop()
        self.start(now)

    def cleanup(self):
        self.stop()

        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass


@pytest.fixture
def urbanwear_server():
    server = UrbanWearServer()

    server.reset()
    server.start()

    yield server

    server.cleanup()