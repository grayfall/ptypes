import abc
import typing as t
import itertools as it
from functools import partial

from ptypes.base import Applicative, Functor, Monad, Monoid

A = t.TypeVar('A')
B = t.TypeVar('B')


__all__ = ['MList']


# TODO replace built-in list with a persistent data structure
# TODO add concat (in general, we can define any monadic bind in terms of fmap followed by concat – rewrite the
#      Functor -> Applicative -> Monad hierarchy to automatically derive operations)
class MList(t.Generic[A], Monoid, Functor, Applicative, Monad):

    def __init__(self, iterable: t.Iterable[A]):
        self._values = list(iterable)

    @classmethod
    def mempty(cls):
        return cls([])

    def mappend(self, value: A) -> 'MList[A]':
        return type(self)(it.chain(self, [value]))

    def fmap(self, f: t.Callable[[A], B]) -> 'MList[B]':
        return type(self)(map(f, self))

    def amap(self, other: 'MList[A]') -> 'MList[B]':
        return type(self)(
            it.chain.from_iterable(other.fmap(f) for f in self)
        )

    def bind(self, f: t.Callable[[A], 'MList[B]']) -> 'MList[B]':
        return type(self)(
            it.chain.from_iterable(map(f, self))
        )

    @classmethod
    def unit(cls, value: A) -> 'MList[A]':
        return cls([value])

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item: t.Union[int, slice]) -> t.Union[A, t.List[A]]:
        return type(self)(self._values[item]) if isinstance(item, slice) else self._values[item]

    def __iter__(self) -> t.Iterator[A]:
        return iter(self._values)

    def __repr__(self):
        return f'{type(self).__name__}({repr(self._values)})'

    def __str__(self):
        return str(self._values)

    def __add__(self, other: 'MList[A]') -> 'MList[A]':
        return type(self)(it.chain(self, other))


if __name__ == '__main__':
    raise ValueError