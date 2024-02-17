import asyncio
import json
import time

from fastapi import APIRouter, FastAPI, Request
from loguru import logger

from context import Context
from logger import setup_logger

SLEEP_INTERVAL = 5

setup_logger()


app = FastAPI()
router = APIRouter(prefix="/root")


@router.get("/async")
async def async_get_method() -> None:
    logger.info("Inside async GET method.")
    await asyncio.sleep(SLEEP_INTERVAL)


@router.get("/sync")
def sync_get_method() -> None:
    logger.info("Inside sync GET method.")
    time.sleep(SLEEP_INTERVAL)


@app.middleware("http")
async def add_context(request: "Request", call_next):
    context_header = request.headers.get("X-context", "{}")
    context = json.loads(context_header)
    with Context(**context):
        return await call_next(request)


app.include_router(router)
