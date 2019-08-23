# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2019 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

from jellyfish import damerau_levenshtein_distance
from jellyfish._jellyfish import (
    damerau_levenshtein_distance as py_damerau_levenshtein_distance,
)


class Comparer(object):
    """String comparer abstraction.

    The reason is to be able to change implementation."""

    def similarity(self, first, second):
        """Returns string similarity in range 0 - 100%."""
        try:
            try:
                distance = damerau_levenshtein_distance(first, second)
            except ValueError:
                # Needed on Python 2 only (actually jellyfish < 0.7.2)
                distance = py_damerau_levenshtein_distance(first, second)

            return int(
                100 * (1.0 - (float(distance) / max(len(first), len(second), 1)))
            )
        except MemoryError:
            # Too long string, mark them as not much similar
            return 50
