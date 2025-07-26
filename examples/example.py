# Copyright (C) 2025 Jeffery Spirko
#
# Sortable is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sortable is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sortable. If not, see <https://www.gnu.org/licenses/>.

from sortable import Sortable

class Person(Sortable):
  """
  Sample intermediate class using Sortable.
  
  Person defines __eq__, but not the ordering operators.
  Sortable provides __ne__ automagically.
  A subclass will have to provide at least one concrete implementation.
  
  """
  def __init__(self, name: str):
    super().__init__()
    self.name: str = name

  def __eq__(self, other: 'Student') -> bool:
    return self.name == other.name

class Student(Person):
  """
  Sample class that uses Sortable through an intermediate parent class.
  
  Sortable provides only __le__, which bothers pylance.  Nevertheless,
  python can instantiate Student() objects because Sortable provides
  the other abstract methods.
  """
  
  def __init__(self, name: str, average: float):
    super().__init__(name=name)
    self.average: float = average

  def __le__(self, other: 'Student') -> bool:
    return self.average <= other.average

  def __repr__(self):
    return f'Student(name={self.name}, average={self.average})'

if __name__ == "__main__":

  def print_method_types(cls):
    """Quick-and-dirty function to check if abstract methods have been defined. """
    if not isinstance(cls, type):
      print('Not a class')
    for op in Sortable.__abstractmethods__:
      status = 'Abstract' if op in getattr(cls, '__abstractmethods__', set()) else 'Concrete'
      print(op, status)

  print_method_types(Student)

  s1 = Student('Awesome', 90)
  s3 = Student('A2', 90)
  s2 = Student('Medium', 70)

  print(f'{s1=}, {s2=}, \n{s1 > s2=}')
  print()
  print(f'{s1=}, {s3=}, \n{s1 <= s3=}')

  pass
