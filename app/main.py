"""FastAPI calculator application with centralized logging."""
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .calculator import add, sub, mul, div
from .logging_config import configure_logging

# ensure logging is configured (idempotent)
configure_logging()
import logging

logger = logging.getLogger("calculator")


class Operands(BaseModel):
    a: float
    b: float


app = FastAPI()

# serve a tiny static frontend so Playwright e2e tests can interact with a UI
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def read_index():
    index = static_dir / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting FastAPI Calculator app")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    logger.info(f"Incoming request {request.method} {request.url}")
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.exception("Unhandled exception during request")
        raise
    duration = time.time() - start
    logger.info(
        f"Completed {request.method} {request.url} with status={response.status_code} in {duration:.3f}s"
    )
    return response


@app.get("/add")
def route_add(a: float, b: float):
    result = add(a, b)
    return {"operation": "add", "a": a, "b": b, "result": result}


@app.get("/sub")
def route_sub(a: float, b: float):
    result = sub(a, b)
    return {"operation": "sub", "a": a, "b": b, "result": result}


@app.get("/mul")
def route_mul(a: float, b: float):
    result = mul(a, b)
    return {"operation": "mul", "a": a, "b": b, "result": result}


@app.get("/div")
def route_div(a: float, b: float):
    try:
        result = div(a, b)
    except ZeroDivisionError:
        logger.warning("Attempted division by zero: %s / %s", a, b)
        raise HTTPException(status_code=400, detail="division by zero")
    return {"operation": "div", "a": a, "b": b, "result": result}
