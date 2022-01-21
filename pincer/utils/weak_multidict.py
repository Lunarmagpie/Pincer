# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from collections import defaultdict
from typing import DefaultDict, Generic, Optional, TypeVar, overload, Set
from weakref import WeakSet, finalize


T = TypeVar("T")


class WeakMultidict(Generic[T]):
    def __init__(self) -> None:
        self.dict: DefaultDict[str, Set[T]] = defaultdict(WeakSet)

    def __on_del_callback(self, key):
        if len(self[key]) == 1:
            del self[key]

    def __setitem__(self, key, value):
        self.dict[key].add(value)
        finalize(value, self.__on_del_callback, key)

    def __getitem__(self, key) -> Set[T]:
        if key in self.dict:
            return self.dict[key]
        raise KeyError(f"WeakMultidict does not have key `{key}`")

    def __delitem__(self, key):
        del self.dict[key]

    @overload
    def get(self, key, default) -> Optional[Set[T]]:
        ...

    def get(self, key, *args) -> Optional[Set[T]]:
        if key in self.dict:
            return self.dict[key]

        if args:
            return None or args[0]
        return None
