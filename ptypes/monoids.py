import abc
import operator as op
import typing as t

import pandas as pd
from fn import F

from ptypes.base import Monoid, Parametric

A = t.TypeVar('A')

__all__ = ['MList', 'DataFrameMonoid', 'MRows', 'MTuple', 'MStruct']


class MList(list, Monoid):

    @classmethod
    def mempty(cls):
        return cls()

    def mappend(self, other: 'MList') -> 'MList':
        return self + other

    def __add__(self, other: 'MList') -> 'MList':
        return type(self)(super().__add__(other))


class DataFrameMonoid(Monoid, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def binder(self, a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
        pass

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def __init__(self, df: t.Optional[pd.DataFrame]):
        self._df = df

    def __repr__(self):
        return f'{type(self).__name__}({repr(self.df)})'

    def __str__(self):
        return repr(self.df)

    @classmethod
    def mempty(cls):
        return cls(None)

    def mappend(self, other: 'DataFrameMonoid') -> 'DataFrameMonoid':
        return type(self)(self.binder(self.df, other.df))


class MRows(DataFrameMonoid):

    _rbind = (
        F(filter, lambda x: x is not None)
        >> list
        >> (lambda x: pd.concat(x, axis=0, sort=True) if x else None)
    )

    def binder(self, a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
        return self._rbind([a, b])


class MTuple(Parametric, Monoid):

    __param__ = None

    def __init__(self, *args: Monoid):
        super().__init__()
        if len(args) != len(self.__param__):
            raise ValueError(
                f'{type(self).__name__} requires {len(self.__param__)} '
                f'arguments, got {len(args)}'
            )
        # TODO we might consider removing these type checks
        wrong_type = next((
            (arg, param) for arg, param in zip(args, self.__param__)
            if not isinstance(arg, param)
        ), None)
        if wrong_type:
            arg, param = wrong_type
            raise TypeError(f'argument {arg!r} is not an instance of {param}')
        self._values = args

    def __repr__(self):
        typename = type(self).__name__
        values = ', '.join(map(repr, self._values))
        return f'{typename}({values})'

    def __getitem__(self, item: int):
        return self._values[item]

    def __iter__(self):
        return iter(self._values)

    @classmethod
    def mempty(cls):
        raise TypeError(
            f'Cannot call mempty on an unparametrised {cls.__name__}'
        )

    def mappend(self, other: 'MTuple') -> 'MTuple':
        appended = (
            a + b for a, b in zip(self._values, other._values)
        )
        return type(self)(*appended)

    @classmethod
    def create(cls, name: str, parameters=t.Sequence[t.Type[Monoid]],
               *args, **kwargs) -> t.Type['MTuple']:
        """
        Create a parametrised MTuple type.
        :param name: type name
        :param parameters: a sequence of monoid types
        """

        def mempty(cls):
            return cls(*[monoid.mempty() for monoid in parameters])

        namespace = dict(
            mempty=classmethod(mempty),
            __param__=tuple(parameters)
        )

        return type(name, (MTuple,), namespace)


class MStruct(MTuple):

    @staticmethod
    def _make_attrgetter(idx: int):
        return property(lambda self: self._values[idx])

    @classmethod
    def create(cls, name: str, parameters: t.Sequence[t.Tuple[str, t.Type[Monoid]]], *args, **kwargs) -> t.Type['MStruct']:
        """
        Create a parametrised MTuple type.
        :param name: type name
        :param parameters: a sequence of attribute names and corresponding
        monoid types.
        """

        def mempty(cls):
            return cls(*[monoid.mempty() for _, monoid in parameters])

        getters = {
            attr: cls._make_attrgetter(i) for i, (attr, _) in enumerate(parameters)
        }
        namespace = dict(
            __param__=list(map(op.itemgetter(1), parameters)),
            mempty=classmethod(mempty),
            **getters
        )

        return type(name, (MStruct,), namespace)


if __name__ == '__main__':
    raise RuntimeError
