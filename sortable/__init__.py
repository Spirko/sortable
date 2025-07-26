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

"""
sortable: A Python abstract base class to simplify creating sortable objects,
with functionality similar to functools.total_ordering.
"""

from .core import Sortable

__all__ = ["Sortable"]
__version__ = "0.1.0"
