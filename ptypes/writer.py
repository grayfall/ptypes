import typing as t

from ptypes.base import Functor, Monad, Monoid, Parametric

A = t.TypeVar('A')
B = t.TypeVar('B')
M = t.TypeVar('M', bound=Monoid)


__all__ = ['Writer']


# TODO implement applicative
class Writer(Parametric, Functor, Monad, t.Generic[M, A]):

    __param__ = None

    def __init__(self, value: A, log: M):
        super().__init__()
        self._value = (value, log)

    def fmap(self, f: t.Callable[[A], B]) -> 'Writer[M, B]':
        a, w = self.run()
        return type(self)(f(a), w)

    def bind(self, f: t.Callable[[A], 'Writer[M, B]']) -> 'Writer[M, B]':
        a, w1 = self.run()
        b, w2 = f(a).run()
        return type(self)(b, w1 + w2)

    @classmethod
    def unit(cls, value: A) -> 'Writer[M, A]':
        raise TypeError(
            f'Cannot call unit in an unparametrised {cls.__name__}'
        )

    def run(self) -> t.Tuple[A, M]:
        """
        Extract value from Writer.
        """
        return self._value

    @classmethod
    def create(cls, name: str, parameter: t.Type[M], *args, **kwargs) -> t.Type['Writer[M]']:
        """
        Create a parametrised Writer type
        """

        def unit(cls, value: A) -> Writer[M, A]:
            return cls(value, parameter.mempty())

        namespace = dict(
            unit=classmethod(unit),
            __param__=(parameter,)
        )

        # TODO this used to be `type(name, (cls, Generic[A]), namespace)`, but Python >= 3.7 prohibits dynamic generics:
        #      find a way around the issue (see https://bugs.python.org/issue33188)
        return type(name, (cls,), namespace)  # ignore type


if __name__ == '__main__':
    raise RuntimeError
