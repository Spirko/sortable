# sortable

**sortable** provides the Sortable Python abstract base class `Sortable` to simplify creating sortable objects, with ability like functools.total_ordering.  This allows developers to provide a minimal set of comparison operators, while automatically generating the rest.

The main motivation for this project was to learn how to write an abstract base class with optional `@abstractmethod ` methods.  It's still too clever for pylance, but it works.

## Features

- Abstract base class for sortable objects
- Enforces implementation of at least one equality and one ordering method
- Auto-generates missing comparison methods
- Inspired by and extends the behavior of `functools.total_ordering`

## Installation


To install the package in editable mode (recommended for development):

```bash
pip install -e .
```

## License

This project is licensed under the GNU General Public License v3 or later.  
See the LICENSE file for details.  (https://www.gnu.org/licenses/gpl-3.0.en.html)

This project includes logic adapted from Python's standard library (`functools.total_ordering`).


## Attribution

This project includes logic adapted from the Python standard library, particularly from `functools.total_ordering`.  
The original code is licensed under the Python Software Foundation License (PSFL).  
See the Python license (https://docs.python.org/3/license.html) for more information.
