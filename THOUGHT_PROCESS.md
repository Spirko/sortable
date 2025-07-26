# THOUGHT_PROCESS.md

## License

This document is part of the `sortable` Python package and is released under the GNU GPL v3 license. See the main repository for full license details.

---

## Why I created `sortable`

I was reading the documentation for Python, and a bunch of things seemed like they could go together.

* The `sorted()` Python builtin (https://docs.python.org/3/library/functions.html#sorted) mentions 
  that only `__lt__()` is needed, but [PEP 8](https://peps.python.org/pep-0008/) recommends all six 
  [rich comparisons](https://docs.python.org/3/reference/expressions.html#comparisons).

* The `abc` module (sic) allows defining an interface, so that Python can ensure that a class has
  given behaviors.  `@abstractmethod` methods of the abstract base class must be implemented by
  the subclass that is inheriting from the abstract base class.

* A lot of actual abstract classes are in [`collections.abc`](https://docs.python.org/3/library/collections.abc.html).  There's a nice table that lists them,
  along with the methods that are available for those classes.  An `Iterable`, for example, is
  anything that can provide an iterator.  There should be something that declares that your class
  provides the comparison operators.

* Searching the documentation, I stumbled across [@functools.total_ordering](https://docs.python.org/3/library/functools.html#functools.total_ordering).
  This cool class decorator fills in missing comparison operators!  That's neat.  That means that the PEP 8 recommendation
  is easier to satisfy, even when only manually implementing one comparison.  But alas, as of Python 3.13, this decorator
  doesn't work for any method that has been declared, even if the method is abstract.

So it seems impossible to make use of an abstract base class and also fill in missing comparison operators.  Well, no, it's not impossible.

## Abstract Base Class

The basic ABC is really easy.

```python
from abc import ABC, abstractmethod, update_abstractmethods

class Sortable(ABC):
    @abstractmethod
    def __eq(self, other) -> bool: pass
    # ...
```

This forces subclasses to provide implementations of each of the `@abstractmethod` methods before an instance can be created.
Only doing this wouldn't be very useful, except perhaps in type checking.

What I really want is to automagically provide missing implementations.

## First Attempt

My first attempt was to write a new version of `@functools.total_ordering`.  This probably would have worked, but I was having trouble
getting it just right.  It does have some key pieces.

```python
import functools
def total_ordering_abstract(cls):
    defined = {op: fn for op in functools._convert
               if (fn := getattr(cls, op, None)) is not None}
    overridden = {op: fn for op,fn in defined.items()
               if getattr(cls, op, None) is not getattr(object, op, None)}
    concrete = {op: fn for op,fn in overridden.items()
               if op not in getattr(cls, '__abstractmethods__', set())}
    # ...
    return cls
```

Here, I'm learning to probe the structure of a class.  `functools._convert` is a dictionary from the four ordering comparison
method names to versions implemented from each other.  That's how `@functools.total_ordering` works.  The `defined` line starts
with that list of strings (iterating over a dictionary iterates over its keys).  Sure, there are other ways to do this.  If
the functions aren't needed, `hasattr()` will suffice.  But I got in the habbit of `getattr()` with its default as a sentinel.

The second line is like what `@functools.total_ordering` actually uses.  It compares whether the given function in the class
is different from what `object()` provides.  This means the class or one of its superclasses overrode it.  This doesn't say
who did it and whether it's concrete or abstract.

The last line is a decent way to find out whether a method is abstract.  The `cls.__abstractmethods__` property is a
[frozenset](https://docs.python.org/3/library/functions.html#func-frozenset) listing methods which were marked with
`@abstractmethod`.  (It turns out this is less reliable than simply checking if the method is marked with `.__isabstractmethod__`.)

This would have worked, if I had used `.__isabstractmethod__`.  But once I was convinced this could work, it became boring.

## Second attempt

So I asked Copilot (shoot me) if it's possible for an `ABC` to have an optional `@abstractmethod`.  It suggested defining
the `__init_subclass__()` method.  That led to more documnation reading, specifically the Data model and
[Customizing class creation](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation).  It seems that
the superclass's `__init_subclass__()` is called by the subclass, as it's defined.  This is done after all of the
subclass's explicit methods are declared.  So it's a good opportunity to inspect and fill in the blanks.

There's just one problem.  Since the subclass isn't done being created yet, the `cls.__abstractmethods__` list hasn't 
been created yet.  That's apparently done by `ABCMeta` at a slightly later time.  So the `.__isabstractmethod__` property
of each method must be inspected individually.  The way to do that is:

```python
  # cls is available from the enclosing scope.
  def is_concrete(name):
    return (fn := getattr(cls, name, None)) is not None
            and not getattr(fn, '__isabstractmethod__', False)
```

From here, it's not that hard to inspect `cls` (the subclass) from `Sortable.__init_subclass__(cls)` (the superclass's method).
I adapted the functions, conversion dictionary, and method used by `@functools.total_ordering`.
