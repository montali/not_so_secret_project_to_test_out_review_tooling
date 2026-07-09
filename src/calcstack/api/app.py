"""A small FastAPI app exposing the calculator over HTTP.

Endpoints:

* ``POST /calc``      — evaluate an expression, record it, return the result
* ``GET  /history``   — list past calculations
* ``DELETE /history`` — clear the history
* ``GET  /health``    — liveness probe
* ``GET  /``          — the static web UI (once it is installed)

Run it with::

    uvicorn calcstack.api.app:app --reload
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import Response

from calcstack.engine.errors import CalculatorError
from calcstack.history import HistoryEntry, default_history
from calcstack.parser import evaluate

STATIC_DIR = Path(__file__).parent / "static"


class CalcRequest(BaseModel):
    expression: str


class CalcResponse(BaseModel):
    expression: str
    result: str


app = FastAPI(title="calcstack API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/calc", response_model=CalcResponse)
def calc(request: CalcRequest) -> CalcResponse:
    try:
        result = evaluate(request.expression)
    except CalculatorError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    default_history().add(request.expression, str(result))
    return CalcResponse(expression=request.expression, result=str(result))


@app.get("/history", response_model=list[HistoryEntry])
def history() -> list[HistoryEntry]:
    return default_history().all()


@app.delete("/history")
def clear_history() -> dict[str, str]:
    default_history().clear()
    return {"status": "cleared"}


@app.get("/")
def index() -> Response:
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse({"message": 'calcstack API. POST /calc with {"expression": "2 + 3 * 4"}.'})


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
