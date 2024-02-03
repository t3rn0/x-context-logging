# Copied and modified from https://github.com/afonasev/context_logging

from collections import UserDict
from contextlib import ContextDecorator
from contextvars import ContextVar, Token
from inspect import getframeinfo, stack
from typing import Any, ChainMap, Optional, Type, cast

ROOT_CONTEXT_NAME = "root"


class _ContextFactory(ContextDecorator):
    def __init__(self, name: Optional[str] = None, /, **kwargs: Any) -> None:
        self.name = name or context_name_with_code_path()
        self._context_data = kwargs

    def __enter__(self) -> "ContextObject":
        context = self.create_context()
        context.start()
        return context

    def __exit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_value: Optional[Exception],
        traceback: Any,
    ) -> None:
        context = _current_context.get()
        context.finish(exc_value)

    def create_context(self) -> "ContextObject":
        return ContextObject(
            name=self.name,
            **self._context_data,
        )


class ContextObject(UserDict):
    def __init__(
        self,
        name: str,
        **kwargs: Any,
    ) -> None:
        self.name = name

        self._context_data = kwargs

        self._parent_context: Optional[ContextObject] = None
        self._parent_context_token: Optional[Token[ContextObject]] = None

    @property
    def data(self) -> ChainMap[Any, Any]:
        return ChainMap(self._context_data, self._parent_context or {})

    def start(self) -> None:
        self._parent_context = _current_context.get()
        self._parent_context_token = _current_context.set(self)

    def finish(self, exc: Optional[Exception] = None) -> None:
        _current_context.reset(cast(Token, self._parent_context_token))


def context_name_with_code_path() -> str:
    """
    >>> _default_name()
    'Context /path_to_code/code.py:10'
    """
    caller = getframeinfo(stack()[2][0])
    return f"Context {caller.filename}:{caller.lineno}"


root_context = _ContextFactory(ROOT_CONTEXT_NAME).create_context()

_current_context: ContextVar[ContextObject] = ContextVar("ctx", default=root_context)


# TODO operator __or__
# >> current_context | some_dict
# ...
# TypeError: CurrentContextProxy.__init__() takes 1 positional argument but 2 were given
# TODO handle json dumps
# >> json.dumps(current_context)
# ...
# TypeError: Object of type CurrentContextProxy is not JSON serializable
class CurrentContextProxy(UserDict):
    def __init__(self) -> None:
        pass

    @property
    def data(self) -> ContextObject:
        return _current_context.get()


current_context = CurrentContextProxy()
Context = _ContextFactory
