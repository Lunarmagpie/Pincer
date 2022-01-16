# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from typing import Any, Awaitable, Callable


_log = logging.getLogger(__name__)

T = TypeVar("T")


class PartialInteractable(ABC):
    """
    Represents a command or message component to be registered to a class.

    Parameters
    ----------
    func : Callable[..., Awaitable[Any]]
        The function to run for this interaction.
    args : Any
        Args to be stored to used in register.
    kwargs : Any
        Kwargs to store to be used in register.
    """

    def __init__(self, func: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.func.__call__(*args, **kwds)

    @abstractmethod
    def register(self, manager: Any) -> type[T]:
        """Registers a command to a command handler to be called later"""


class Interactable:
    """
    Class that can register :class:`~pincer.commands.interactable.PartialInteractable`
    objects.
    """

    def __init__(self):
        for key, value in self.__class__.__dict__.items():
            if isinstance(value, PartialInteractable):
                setattr(self, key, value.register(self))