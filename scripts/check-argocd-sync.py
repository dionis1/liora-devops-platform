#!/usr/bin/env python3
"""Wait for actual Argo reconciliation; emit only non-secret status evidence."""
import argparse
import json
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kubeconfig", required=True)
    parser.add_argument("--application", default="liora-dev")
    parser.add_argument("--namespace", default="argocd")
    parser.add_argument("--revision", required=True, help="Expected full Git commit SHA")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    deadline = time.monotonic() + args.timeout
    last = None
    while time.monotonic() < deadline:
        raw = subprocess.check_output([
            "kubectl", "--kubeconfig", args.kubeconfig, "-n", args.namespace,
            "get", "application", args.application, "-o", "json",
        ], text=True)
        app = json.loads(raw)
        status = app.get("status", {})
        operation = status.get("operationState", {})
        current = {
            "application": app["metadata"]["name"],
            "repository": app["spec"]["source"]["repoURL"],
            "target": app["spec"]["source"]["targetRevision"],
            "path": app["spec"]["source"]["path"],
            "sync": status.get("sync", {}).get("status"),
            "health": status.get("health", {}).get("status"),
            "revision": status.get("sync", {}).get("revision"),
            "operation": operation.get("phase"),
            "operation_revision": operation.get("syncResult", {}).get("revision"),
            "conditions": status.get("conditions", []),
        }
        if current != last:
            print(json.dumps(current), flush=True)
            last = current
        if (current["sync"] == "Synced" and current["health"] == "Healthy"
                and current["revision"] == args.revision
                and current["operation"] == "Succeeded"
                and current["operation_revision"] == args.revision
                and not current["conditions"]):
            print(json.dumps({"result": "PASSED", "observed_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                              **current, "resources": status.get("resources", []),
                              "history": status.get("history", [])}, indent=2), flush=True)
            return
        time.sleep(3)
    raise SystemExit("FAILED: expected revision did not reach Synced + Healthy with a successful operation")


if __name__ == "__main__":
    main()
