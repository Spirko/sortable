# Copyright (C) 2025 Jeffery Spirko
#
# Sortable is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sortable is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sortable.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod, update_abstractmethods

class Sortable(ABC):
  """
  Abstract base class that provides rich comparison methods.
  
  Implementations must define:
  * At least one of __eq__ or __ne__: to test for equality.
  * At least one of __lt__, __le__, __gt__, __ge__: to test for ordering.
  """
  @abstractmethod
  def __eq__(self, other) -> bool:  pass

  @abstractmethod
  def __ne__(self, other) -> bool:  pass

  @abstractmethod
  def __lt__(self, other) -> bool:  pass

  @abstractmethod
  def __le__(self, other) -> bool:  pass

  @abstractmethod
  def __gt__(self, other) -> bool:  pass

  @abstractmethod
  def __ge__(self, other) -> bool:  pass

  def __init_subclass__(cls, **kwargs):

    def is_concrete(name):
      """Helper for Sortable.__init_subclass__"""
      return (fn := getattr(cls, name, None)) is not None and not getattr(fn, '__isabstractmethod__', False)

    # Check for both equality methods
    has_eq = is_concrete('__eq__')
    has_ne = is_concrete('__ne__')

    if not (has_eq or has_ne):
      raise TypeError(f'{cls.__name__} must define __eq__ or __ne__.')

    if not has_ne:
      cls.__ne__ = _ne__from_eq
      cls.__ne__.__name__ = '__ne__'
    if not has_eq:
      cls.__eq__ = _eq__from_ne
      cls.__eq__.__name__ = '__eq__'

    # if all(op in cls.__abstractmethods__ for op in ordering_ops):
    #   raise TypeError(f'{cls.__name__} must define at least one of {ordering_ops}.')

    # Simulate this as being decorated with @total_ordering
    if any(is_concrete(op) for op in _compare_ops):
      # for op in ordering_ops:
      #   if is_concrete(op):
      #     setattr(getattr(cls, op), '__isabstractmethod__', False)
      concrete = {op for op in _compare_conversions.keys() if (getattr(cls, op, None) is not None and is_concrete(op))}
      root = max(concrete)   # prefer __lt__ to __le__ to __gt__ to __ge__
      for opname, opfunc in _compare_conversions[root].items():
        if opname not in concrete:
          opfunc.__name__ = opname
          setattr(cls, opname, opfunc)


    super().__init_subclass__(**kwargs)


    update_abstractmethods(cls)

# Technique copied from @functools.total_ordering
def _ne__from_eq(self: 'Sortable', other: 'Sortable') -> bool:
  'Retuurn a != b.  Computed by Sortable from not (a == b).'
  result = self.__ne__(other)
  return (not result) if result is not NotImplemented else NotImplemented

def _eq__from_ne(self: 'Sortable', other: 'Sortable') -> bool:
  'Retuurn a == b.  Computed by Sortable from not (a != b).'
  result = self.__eq__(other)
  return (not result) if result is not NotImplemented else NotImplemented

def __gt__from_lt(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a > b.  Computed by Sortable from (not a < b) and (a != b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and self != other

def __le__from_lt(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a <= b.  Computed by Sortable from (a < b) or (a == b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result or self == other

def __ge__from_lt(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a >= b.  Computed by Sortable from (not a < b).'
    op_result = type(self).__lt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def __ge__from_le(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a >= b.  Computed by Sortable from (not a <= b) or (a == b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result or self == other

def __lt__from_le(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a < b.  Computed by Sortable from (a <= b) and (a != b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result and self != other

def __gt__from_le(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a > b.  Computed by Sortable from (not a <= b).'
    op_result = type(self).__le__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def __lt__from_gt(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a < b.  Computed by Sortable from (not a > b) and (a != b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result and self != other

def __ge__from_gt(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a >= b.  Computed by Sortable from (a > b) or (a == b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result or self == other

def __le__from_gt(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a <= b.  Computed by Sortable from (not a > b).'
    op_result = type(self).__gt__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

def __le__from_ge(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a <= b.  Computed by Sortable from (not a >= b) or (a == b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result or self == other

def __gt__from_ge(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a > b.  Computed by Sortable from (a >= b) and (a != b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return op_result and self != other

def __lt__from_ge(self: 'Sortable', other: 'Sortable') -> bool:
    'Return a < b.  Computed by Sortable from (not a >= b).'
    op_result = type(self).__ge__(self, other)
    if op_result is NotImplemented:
        return op_result
    return not op_result

_compare_ops = ['__lt__', '__le__', '__gt__', '__ge__']
_compare_conversions = {
  '__lt__': { '__le__': __le__from_lt, '__gt__': __gt__from_lt, '__ge__': __ge__from_lt },
  '__ge__': { '__lt__': __lt__from_ge, '__le__': __le__from_ge, '__gt__': __gt__from_ge },
  '__le__': { '__lt__': __lt__from_le, '__gt__': __gt__from_le, '__ge__': __ge__from_le },
  '__gt__': { '__lt__': __lt__from_gt, '__le__': __le__from_gt, '__ge__': __ge__from_gt }
}
