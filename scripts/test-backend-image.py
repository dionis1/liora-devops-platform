#!/usr/bin/env python3
"""Test the exact runtime image with PostgreSQL; keep credentials out of output."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request


def docker(*args):
    return subprocess.check_output(["docker", *args], text=True).strip()


def main():
    image = sys.argv[1] if len(sys.argv) > 1 else "liora-backend:ci"
    prefix = "liora-image-test-" + secrets.token_hex(4)
    database, backend, migrate = [prefix + suffix for suffix in ("-db", "-api", "-migrate")]
    # UserCreate limits passwords to 40 characters; use 128 random bits.
    password = secrets.token_hex(16)
    network_created = False
    with tempfile.TemporaryDirectory(prefix="liora-image-test-") as work:
        envfile = Path(work) / "backend.env"
        env = {
            "POSTGRES_USER": "app", "POSTGRES_DB": "app",
            "POSTGRES_PASSWORD": secrets.token_hex(24), "POSTGRES_SERVER": database,
            "POSTGRES_PORT": "5432", "SECRET_KEY": secrets.token_hex(32),
            "FIRST_SUPERUSER": "image-test@example.com", "FIRST_SUPERUSER_PASSWORD": password,
            "PROJECT_NAME": "Image-validation", "ENVIRONMENT": "local",
            "SMTP_HOST": "smtp.invalid", "SMTP_PORT": "1025", "SMTP_TLS": "false",
            "EMAILS_FROM_EMAIL": "noreply@example.com",
        }
        fd = os.open(envfile, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as stream:
            stream.write("".join(f"{key}={value}\n" for key, value in env.items()))
        hardened = ["--network", prefix, "--env-file", str(envfile), "--memory", "256m",
                    "--read-only", "--tmpfs", "/tmp:rw,size=64m", "--cap-drop", "ALL",
                    "--security-opt", "no-new-privileges:true"]
        try:
            docker("network", "create", prefix)
            network_created = True
            docker("run", "-d", "--name", database, "--network", prefix,
                   "--env-file", str(envfile), "--memory", "256m",
                   "--tmpfs", "/var/lib/postgresql/data:rw,size=256m", "postgres:16.10")
            for _ in range(90):
                ready = subprocess.run(["docker", "exec", database, "pg_isready", "-U", "app", "-d", "app"],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if ready.returncode == 0:
                    break
                time.sleep(1)
            else:
                raise RuntimeError("PostgreSQL readiness timed out")
            print("PASS isolated PostgreSQL 16.10 ready", flush=True)
            # The deployed init container invokes this same Bash script.
            docker("run", "--name", migrate, *hardened, image, "bash", "scripts/prestart.sh")
            print("PASS image migration and initial superuser under read-only/non-root restrictions", flush=True)
            docker("run", "-d", "--name", backend, *hardened,
                   "-p", "127.0.0.1::8000", image)
            port = docker("port", backend, "8000/tcp").split(":")[-1]
            base = "http://127.0.0.1:" + port

            def request(path, data=None, token=None, method=None):
                headers = {}
                if isinstance(data, dict):
                    data = json.dumps(data).encode()
                    headers["Content-Type"] = "application/json"
                elif data is not None:
                    headers["Content-Type"] = "application/x-www-form-urlencoded"
                if token:
                    headers["Authorization"] = "Bearer " + token
                req = urllib.request.Request(base + path, data=data, headers=headers, method=method)
                with urllib.request.urlopen(req, timeout=5) as response:
                    return response.status, response.read()

            for _ in range(90):
                try:
                    if request("/readyz")[0] == 200:
                        break
                except (OSError, TimeoutError):
                    pass
                time.sleep(1)
            else:
                raise RuntimeError("Image database readiness timed out")
            assert request("/api/v1/utils/health-check/") == (200, b"true")
            assert request("/api/v1/openapi.json")[0] == 200
            print("PASS default image entrypoint, health, database readiness and OpenAPI", flush=True)
            form = urllib.parse.urlencode({"username": env["FIRST_SUPERUSER"], "password": password}).encode()
            token = json.loads(request("/api/v1/login/access-token", data=form)[1])["access_token"]
            status, body = request("/api/v1/items/", data={"title": "Alpine runtime validation"}, token=token)
            assert status == 200
            item = json.loads(body)
            path = "/api/v1/items/" + item["id"]
            assert json.loads(request(path, token=token)[1])["title"] == "Alpine runtime validation"
            assert request(path, token=token, method="DELETE")[0] == 200
            print("PASS bcrypt login, JWT authentication and PostgreSQL item create/read/delete", flush=True)
            assert b"http_requests_total" in request("/metrics")[1]
            for _ in range(45):
                if docker("inspect", "--format", "{{.State.Health.Status}}", backend) == "healthy":
                    break
                time.sleep(1)
            else:
                raise RuntimeError("Docker HEALTHCHECK did not become healthy")
            assert docker("exec", backend, "id", "-u") == "10001"
            print("PASS metrics, Docker HEALTHCHECK and runtime UID 10001", flush=True)
            print("PASS exact backend runtime image: " + docker("image", "inspect", "--format", "{{.Id}}", image), flush=True)
        finally:
            for name in (backend, migrate, database):
                subprocess.run(["docker", "rm", "-f", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if network_created:
                subprocess.run(["docker", "network", "rm", prefix], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Temporary image-test containers, database, network and credentials cleaned up", flush=True)


if __name__ == "__main__":
    main()
