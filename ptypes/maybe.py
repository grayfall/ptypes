import abc
import typing as t
from functools import partial

from ptypes.base import Applicative, Functor, Monad

A = t.TypeVar('A')
B = t.TypeVar('B')


__all__ = ['Maybe', 'Just', 'Nothing']


class Maybe(Functor, Applicative, Monad, t.Generic[A], metaclass=abc.ABCMeta):
    """
    A Maybe func implementation
    """

    @classmethod
    def unit(cls, value: A) -> 'Just[A]':
        return Just(value)

    @abc.abstractmethod
    def from_maybe(self, default: A) -> A:
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__str__()

    @abc.abstractmethod
    def __bool__(self) -> bool:
        raise NotImplementedError


class Just(Maybe):

    """A Maybe that contains a value.
    Represents a Maybe that contains a value (represented as Just a).
    """

    def __init__(self, value: A) -> None:
        self._value = value

    def fmap(self, f: t.Callable[[A], B]) -> Maybe[B]:
        try:
            result = f(self._value)
        except TypeError:
            result = partial(f, self._value)
        return type(self)(result)

    def amap(self, other: Maybe) -> Maybe:
        return other.fmap(self._value)

    def bind(self, f: t.Callable[[A], Maybe[B]]) -> Maybe[B]:
        """
        Just x >>= f = f x.
        """
        return f(self._value)

    def from_maybe(self, default: A) -> A:
        return self._value

    def __str__(self) -> str:
        return f'Just {self._value}'

    def __bool__(self):
        return True


class Nothing(Maybe):

    """Represents an empty Maybe.
    Represents an empty Maybe that holds nothing (in which case it has
    the value of Nothing).
    """

    def fmap(self, f: t.Callable[[A], B]) -> Maybe[B]:
        return Nothing()

    def amap(self, other: Maybe) -> Maybe[B]:
        return Nothing()

    def bind(self, f: t.Callable[[A], Maybe[B]]) -> Maybe[B]:
        """
        Nothing >>= f = Nothing
        """
        return Nothing()

    def from_maybe(self, default: A) -> A:
        return default

    def __bool__(self):
        return False

    def __str__(self) -> str:
        return 'Nothing'


if __name__ == '__main__':
    raise RuntimeError
