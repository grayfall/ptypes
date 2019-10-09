import typing as t

from ptypes.base import Monad, Functor

A = t.TypeVar('A')
B = t.TypeVar('B')


__all__ = ['bind', 'fmap']


def fmap(func: t.Callable[[A], B], value: Functor[A]) -> Functor[B]:
    return value.fmap(func)


def bind(func: t.Callable[[A], Monad[B]], value: Monad[A]) -> Monad[B]:
    return value.bind(func)


if __name__ == '__main__':
    raise RuntimeError
