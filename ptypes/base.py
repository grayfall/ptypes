import abc
import typing as t
from functools import reduce


A = t.TypeVar('A')
B = t.TypeVar('B')
F = t.TypeVar('F', bound=t.Callable)


__all__ = ['Parametric', 'Monoid', 'Functor', 'Applicative', 'Monad']


def identity(x: A) -> A:
    return x


class Parametric(metaclass=abc.ABCMeta):
    """
    Parametric types are type-factories (higher-kinded types). They must
    define `create(cls, name, ...)` producing a fully parametrised type.
    Additionally, they must define attribute `__parameters__`: an
    Optional[Tuple] of parameter types for `create` to fill-in.
    """

    __param__: t.Optional[t.Tuple] = None

    def __init__(self, *args, **kwargs):
        if self.__param__ is None:
            raise TypeError(
                f'cannot initialise an instance of unparametrised class '
                f'{type(self).__name__}'
            )

    @classmethod
    @abc.abstractmethod
    def create(cls, name: str, *args, **kwargs) -> t.Type['Parametric']:
        raise NotImplementedError


class Monoid(t.Generic[A], metaclass=abc.ABCMeta):
    """
    The Monoid abstract base class. Must satisfy the following laws
    mappend mempty x = x
    mappend x mempty = x
    mappend x (mappend y z) = mappend (mappend x y) z
    mconcat = foldr mappend mempty
    """

    @classmethod
    @abc.abstractmethod
    def mempty(cls):
        """
        Create an empty monoid.
        mempty :: m
        """
        raise NotImplementedError

    @abc.abstractmethod
    def mappend(self, other: 'Monoid[A]') -> 'Monoid[A]':
        """
        mappend :: m -> m -> m
        """
        raise NotImplementedError

    def __add__(self, other: 'Monoid[A]') -> 'Monoid[A]':
        """
        An operator overload for Monoid.append
        :param other:
        :return:
        """
        return self.mappend(other)

    @classmethod
    def concat(cls, xs: t.Iterable['Monoid[A]']) -> 'Monoid[A]':
        """
        Fold an iterable of monoids.
        mconcat :: [m] -> m
        """
        return reduce(cls.mappend, xs, cls.mempty())


class Functor(t.Generic[A], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def fmap(self, f: t.Callable[[A], B]) -> 'Functor[B]':
        raise NotImplementedError


class Applicative(t.Generic[F], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def amap(self, other: Functor) -> Functor:
        raise NotImplementedError


class Monad(t.Generic[A], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def bind(self, f: t.Callable[[A], 'Monad[B]']) -> 'Monad[B]':
        """
        Monadic bind operation (Haskell's >>=)
        :param f:
        :return:
        """
        raise NotImplementedError

    # We can't have a proper monadic unit (Haskell's return) without
    # type-inference and higher-kinded types;
    @classmethod
    @abc.abstractmethod
    def unit(cls, *args, **kwargs) -> 'Monad[A]':
        raise NotImplemented

    def join(self):
        """
        join :: Monad m => m (m a) -> m a
        Remove one level of monadic structure, projecting its
        bound argument into the outer level.
        """

        return self.bind(identity)


if __name__ == '__main__':
    raise RuntimeError


