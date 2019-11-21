import abc
import typing as t
import itertools as it
from functools import partial

from ptypes.base import Applicative, Functor, Monad, Monoid

A = t.TypeVar('A')
B = t.TypeVar('B')


__all__ = ['List']


# TODO replace built-in list with a persistent data structure
class List(t.Generic[A], Monoid, Functor, Applicative, Monad):

    def __init__(self, iterable: t.Iterable[A]):
        self._values = list(iterable)

    @classmethod
    def mempty(cls):
        return cls([])

    def mappend(self, value: A) -> 'List[A]':
        return type(self)(it.chain(self, [value]))

    def fmap(self, f: t.Callable[[A], B]) -> 'List[B]':
        return type(self)(map(f, self))

    def amap(self, other: 'List[A]') -> 'List[B]':
        return type(self)(
            it.chain.from_iterable(other.fmap(f) for f in self)
        )

    def bind(self, f: t.Callable[[A], 'List[B]']) -> 'List[B]':
        return type(self)(
            it.chain.from_iterable(map(f, self))
        )

    @classmethod
    def unit(cls, value: A) -> 'List[A]':
        return cls([value])

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item) -> t.Union[A, t.List[A]]:
        return type(self)(self._values[item])

    def __iter__(self) -> t.Iterator[A]:
        return iter(self._values)

    def __repr__(self):
        return f'{type(self).__name__}({repr(self._values)})'

    def __str__(self):
        return str(self._values)

    def __add__(self, other: 'List[A]') -> 'List[A]':
        return type(self)(it.chain(self, other))


if __name__ == '__main__':
    raise ValueError