import json
import sys
from typing import TYPE_CHECKING

from loguru import logger

from context import current_context

if TYPE_CHECKING:
    from loguru import Message, Record


def setup_logger() -> None:
    logger.remove()
    logger.add(_sink)
    logger.configure(patcher=_patcher)


def _patcher(message: "Record") -> None:
    """Copy values from thread context to extra field.
    Original extra data has higher priority than context data.
    """
    message["extra"] = dict(current_context, **message["extra"])


def _sink(message: "Message") -> None:
    print(
        json.dumps(
            {
                "time": message.record["time"].isoformat(),
                "level": message.record["level"].name,
                "message": message.record["message"],
                "extra": message.record["extra"],
            },
            default=str,
        ),
        file=sys.stdout,
    )
