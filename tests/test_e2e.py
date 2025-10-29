import subprocess
import sys
import time
import signal
import httpx


def start_uvicorn(port: int = 8001):
    # Start uvicorn programmatically in a subprocess without the reloader so
    # tests can reliably start and stop the server (reloaders spawn extra
    # processes that make termination unreliable).
    run_code = (
        "import uvicorn; uvicorn.run(\"app.main:app\", host=\"127.0.0.1\", "
        f"port={port}, reload=False)"
    )
    cmd = [sys.executable, "-c", run_code]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc


def wait_for_server(url: str, timeout: float = 5.0):
    start = time.time()
    while True:
        try:
            r = httpx.get(url)
            return r
        except Exception:
            if time.time() - start > timeout:
                raise
            time.sleep(0.1)


def test_e2e_add_and_shutdown():
    port = 8001
    proc = start_uvicorn(port=port)
    try:
        # wait for server
        r = wait_for_server(f"http://127.0.0.1:{port}/add?a=2&b=3", timeout=8.0)
        assert r.status_code == 200
        assert r.json()["result"] == 5
    finally:
        # terminate server
        try:
            proc.send_signal(signal.SIGINT)
        except Exception:
            proc.terminate()
        proc.wait(timeout=5)
