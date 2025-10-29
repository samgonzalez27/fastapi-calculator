import subprocess
import sys
import time
import signal
import pytest
import os


def start_uvicorn(port: int = 8002):
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc


def wait_for_server(url: str, timeout: float = 5.0):
    import httpx

    start = time.time()
    while True:
        try:
            r = httpx.get(url)
            return r
        except Exception:
            if time.time() - start > timeout:
                raise
            time.sleep(0.1)


if os.environ.get("RUN_PLAYWRIGHT") != "1":
    # Skip entire module unless explicitly enabled to avoid requiring Playwright/browser
    pytest.skip("Playwright tests are opt-in. Set RUN_PLAYWRIGHT=1 to enable", allow_module_level=True)


def test_playwright_ui_add_and_result():
    # Start server
    port = 8002
    proc = start_uvicorn(port=port)
    try:
        wait_for_server(f"http://127.0.0.1:{port}/", timeout=8.0)

        # Import Playwright inside test so tests that don't run this test don't need the package
        try:
            from playwright.sync_api import sync_playwright
        except Exception as exc:
            pytest.skip(f"Playwright not available: {exc}")

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}/")
            page.fill('#a', '6')
            page.fill('#b', '7')
            page.select_option('#op', 'add')
            page.click('#go')
            # Wait for result text to update
            page.wait_for_selector('#out')
            out = page.locator('#out').inner_text()
            assert 'status: 200' in out
            assert '"result": 13' in out or '13' in out
            browser.close()
    finally:
        try:
            proc.send_signal(signal.SIGINT)
        except Exception:
            proc.terminate()
        proc.wait(timeout=5)
