"""
Microservices Orchestrator & Runner
Runs all microservices plus the Frontend UI concurrently:
  - Frontend UI Service:    http://127.0.0.1:5000
  - Catalog Service:        http://127.0.0.1:5001  (Swagger: :5001/apidocs/)
  - Shopping Cart Service:  http://127.0.0.1:5002  (Swagger: :5002/apidocs/)
  - Discount Service:       http://127.0.0.1:5003  (Swagger: :5003/apidocs/)
  - Order Service:          http://127.0.0.1:5004  (Swagger: :5004/apidocs/)
"""

import os
import signal
import subprocess
import sys
import time

SERVICES = [
    ("Catalog Service", "services/catalog_service/app.py", 5001),
    ("Shopping Cart Service", "services/cart_service/app.py", 5002),
    ("Discount Service", "services/discount_service/app.py", 5003),
    ("Order Service", "services/order_service/app.py", 5004),
    ("Frontend UI Service", "services/frontend_service/app.py", 5000),
]

processes = []


def stop_all(signum=None, frame=None):
    print("\n[Runner] Shutting down all microservices...")
    for name, proc, port in processes:
        if proc.poll() is None:
            print(f"  Stopping {name} (Port {port}, PID {proc.pid})...")
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
    print("[Runner] All services stopped.")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, stop_all)
    signal.signal(signal.SIGTERM, stop_all)

    python_executable = sys.executable
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("================================================================")
    print("  LAUNCHING E-COMMERCE MICROSERVICES & FRONTEND UI")
    print("================================================================")
    print("  Frontend Storefront UI : http://127.0.0.1:5000")
    print("  Catalog Swagger Docs   : http://127.0.0.1:5001/apidocs/")
    print("  Cart Swagger Docs      : http://127.0.0.1:5002/apidocs/")
    print("  Discount Swagger Docs  : http://127.0.0.1:5003/apidocs/")
    print("  Order Swagger Docs     : http://127.0.0.1:5004/apidocs/")
    print("================================================================")

    for name, script_rel, port in SERVICES:
        script_path = os.path.join(base_dir, script_rel)
        print(f"-> Starting {name:22} on http://127.0.0.1:{port}")
        proc = subprocess.Popen(
            [python_executable, script_path],
            cwd=base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        processes.append((name, proc, port))
        time.sleep(0.3)

    print("================================================================")
    print("  All services active. Open http://127.0.0.1:5000 in your browser.")
    print("  Press Ctrl+C to stop all services.")
    print("================================================================")

    try:
        while True:
            for name, proc, port in processes:
                if proc.stdout:
                    line = proc.stdout.readline()
                    if line:
                        print(f"[{port}] {line.strip()}")
                ret = proc.poll()
                if ret is not None:
                    print(f"[{port}] {name} exited with code {ret}")
                    stop_all()
            time.sleep(0.05)
    except KeyboardInterrupt:
        stop_all()


if __name__ == "__main__":
    main()
