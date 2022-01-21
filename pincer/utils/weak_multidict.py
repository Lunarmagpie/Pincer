from __future__ import annotations

from collections import defaultdict
from typing import DefaultDict, Generic, Optional, TypeVar, overload
from weakref import WeakSet, finalize


T = TypeVar("T")


class WeakMultidict(Generic[T]):
    def __init__(self) -> None:
        self.dict: DefaultDict[str, WeakSet[T]] = defaultdict(WeakSet)

    def __on_del_callback(self, key):
        if len(self[key]) == 1:
            del self[key]

    def __setitem__(self, key, value):
        self.dict[key].add(value)
        finalize(value, self.__on_del_callback, key)

    def __getitem__(self, key) -> WeakSet[T]:
        if key in self.dict:
            return self.dict[key]
        raise KeyError(f"WeakMultidict does not have key `{key}`")

    def __delitem__(self, key):
        del self.dict[key]

    @overload
    def get(self, key, default) -> Optional[T]:
        ...

    def get(self, key, *args) -> Optional[T]:
        if key in self.dict:
            return self.dict[key]

        if args:
            return None or args[0]
        return None
