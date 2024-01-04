from collections import namedtuple
from core.utils import get_head_bits, rotate_heads, sort_heads
from django.test import TestCase

Theory = namedtuple('Theory', ['data', 'result'])


class TestHeadUtils(TestCase):

    def test_sort(self):
        result = ''.join(sort_heads('snwe'))
        self.assertEqual(result, 'nesw')

    def test_rotate(self):
        for theory in [
            Theory(['n', 0], 'n'),
            Theory(['e', 0], 'e'),
            Theory(['s', 0], 's'),
            Theory(['w', 0], 'w'),
            Theory(['n', 1], 'e'),
            Theory(['e', 1], 's'),
            Theory(['s', 1], 'w'),
            Theory(['w', 1], 'n'),
            Theory(['n', 2], 's'),
            Theory(['e', 2], 'w'),
            Theory(['s', 2], 'n'),
            Theory(['w', 2], 'e'),
            Theory(['n', 3], 'w'),
            Theory(['e', 3], 'n'),
            Theory(['s', 3], 'e'),
            Theory(['w', 3], 's'),
            Theory(['ns', 1], 'ew'),
            Theory(['nw', 2], 'es'),
            Theory(['new', 3], 'nsw'),
            Theory(['nesw', 1], 'nesw'),
            Theory(['nesw', 2], 'nesw'),
            Theory(['nesw', 3], 'nesw'),
            Theory(['nesw', 4], 'nesw'),
        ]:
            result = ''.join(rotate_heads(*theory.data))
            self.assertEqual(result, theory.result)
