"""FastAPI calculator application with centralized logging.

This module defines the FastAPI application and routes for simple
arithmetic operations. It configures logging via :mod:`app.logging_config`.
"""
import logging
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .logging_config import configure_logging
from .calculator import add, sub, mul, div

# ensure logging is configured (idempotent)
configure_logging()

logger = logging.getLogger("calculator")


class Operands(BaseModel):
    """Pydantic model for the two operands accepted by endpoints."""

    a: float
    b: float


app = FastAPI()

# serve a tiny static frontend so Playwright e2e tests can interact with a UI
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def read_index():
    """Return the static index.html if present, otherwise return a JSON status.

    The presence of a small static UI allows optional Playwright tests to
    exercise the application in a browser. If the file is not present the
    endpoint returns a minimal JSON response for health checking.
    """
    index = static_dir / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Application startup handler used to log that the app started."""
    logger.info("Starting FastAPI Calculator app")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware that logs incoming requests and their durations.

    The middleware logs when a request starts and when it completes; if an
    exception occurs it is logged and re-raised so Starlette can produce the
    appropriate error response.
    """
    start = time.time()
    # Use lazy formatting to avoid building strings when the logger is disabled
    logger.info("Incoming request %s %s", request.method, request.url)
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled exception during request")
        raise
    duration = time.time() - start
    logger.info(
        "Completed %s %s with status=%s in %.3fs",
        request.method,
        request.url,
        response.status_code,
        duration,
    )
    return response


@app.get("/add")
def route_add(a: float, b: float):
    """Add two numbers provided as query parameters and return JSON result."""
    result = add(a, b)
    return {"operation": "add", "a": a, "b": b, "result": result}


@app.get("/sub")
def route_sub(a: float, b: float):
    """Subtract b from a and return JSON result."""
    result = sub(a, b)
    return {"operation": "sub", "a": a, "b": b, "result": result}


@app.get("/mul")
def route_mul(a: float, b: float):
    """Multiply a and b and return JSON result."""
    result = mul(a, b)
    return {"operation": "mul", "a": a, "b": b, "result": result}


@app.get("/div")
def route_div(a: float, b: float):
    """Divide a by b and return JSON result; returns 400 on division by zero."""
    try:
        result = div(a, b)
    except ZeroDivisionError as exc:
        logger.warning("Attempted division by zero: %s / %s", a, b)
        raise HTTPException(status_code=400, detail="division by zero") from exc
    return {"operation": "div", "a": a, "b": b, "result": result}
