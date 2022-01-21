# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from collections import defaultdict
from typing import (
    Any,
    DefaultDict,
    Dict,
    Generic,
    ItemsView,
    KeysView,
    List,
    Optional,
    Tuple,
    TypeVar,
    ValuesView,
    overload
)
from weakref import ProxyTypes, finalize, proxy, ref

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class Proxy(Generic[T]):

    __slots__ = ("ref")

    def __init__(self, obj) -> None:
        self.ref = ref(obj)

    def __getattr__(self, __name: str) -> Optional[Any]:
        if self.ref():
            return self.ref().__getattribute__(__name)
        return None


class WeakMultidict(Generic[K, V]):

    __slots__ = "dict"

    def __init__(self) -> None:
        self.dict: DefaultDict[K, List[V]] = defaultdict(list)

    def __on_del_callback(self, key):
        if not key:
            return

        self.dict[key] = list(filter(lambda obj: obj.ref() is not None, self.dict[key]))

        if not self[key]:
            del self[key]

    def __setitem__(self, key, value):
        finalize(value, self.__on_del_callback, key)
        self.dict[key].append(Proxy(value))

    def __getitem__(self, key) -> List[V]:
        if key in self:
            return self.dict[key]
        raise KeyError(f"WeakMultidict does not have key `{key}`")

    def __delitem__(self, key):
        del self.dict[key]

    def __iter__(self):
        return iter(self.dict)

    def __str__(self):
        return (
            "{"
            + ','.join(
                f"{key}:{value}" for key, value in self.items()
            )
            + "}"
        )

    @overload
    def get(self, key, default) -> Optional[List[V]]:
        ...

    def get(self, key, *args) -> Optional[List[V]]:
        if key in self:
            return self[key]

        if args:
            return None or args[0]
        return None

    def keys(self) -> KeysView[K]:
        return self.dict.keys()

    def values(self) -> ValuesView[List[V]]:
        return self.dict.values()

    def items(self) -> ItemsView[K, List[V]]:
        return self.dict.items()
