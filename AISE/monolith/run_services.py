"""
Microservices Orchestrator & Runner
Runs all four microservices concurrently on separate ports:
  - Catalog Service:        http://127.0.0.1:5001
  - Shopping Cart Service:  http://127.0.0.1:5002
  - Discount Service:       http://127.0.0.1:5003
  - Order Service:          http://127.0.0.1:5004
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
    print("  LAUNCHING E-COMMERCE MICROSERVICES ARCHITECTURE")
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
        time.sleep(0.4)

    print("================================================================")
    print("  All 4 microservices are active. Press Ctrl+C to terminate.")
    print("================================================================")

    # Monitor output from all services
    try:
        while True:
            for name, proc, port in processes:
                # Read available output non-blocking
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

