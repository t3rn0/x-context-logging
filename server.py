import json

from fastapi import APIRouter, FastAPI, Request
from loguru import logger

from context import Context
from logger import setup_logger

setup_logger()


app = FastAPI()
router = APIRouter(prefix="/root")


@router.get("")
async def some_get_method() -> None:
    logger.info("Inside GET method.")


@app.middleware("http")
async def add_context(request: "Request", call_next):
    context_header = request.headers.get("X-context", "{}")
    context = json.loads(context_header)
    with Context(**context):
        return await call_next(request)


app.include_router(router)
