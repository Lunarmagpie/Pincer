# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from functools import partial
from typing import Awaitable, Callable, Optional

from pincer.commands.interactable import PartialInteractable


def command_extension(func: Optional[Callable[..., Awaitable[Optional[bool]]]] = None):
    if func is None:
        return command_extension

    def wrap(partial_interactable: PartialInteractable = None, *args, **kwargs):
        if partial_interactable is None:
            return partial(wrap, *args, **kwargs)

        partial_interactable._extensions.append(partial(func, *args, **kwargs))

        return partial_interactable

    return wrap
