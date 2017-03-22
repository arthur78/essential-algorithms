import unittest
from .models import Cell, Sentinel, TopSentinel, BottomSentinel
from .algorithms import make_list, iterate, add_at_beginning, add_at_end, \
    insert_cell, delete_cell, insert_into_sorted


class LinkedListTest(unittest.TestCase):

    def test_make_list(self):
        """Test different scenarios of linked list creation."""

        top_cell = make_list((1, 2, 3))
        self.assertTrue(isinstance(top_cell, Cell))
        self.assertTrue(isinstance(top_cell, TopSentinel))
        self.assertIn('next', top_cell.__dict__)
        self.assertNotIn('prev', top_cell.__dict__)
        self.assertFalse(top_cell.is_doubly_linked)
        self.assertEqual(top_cell.next.value, 1)
        self.assertEqual(top_cell.next.next.value, 2)
        self.assertEqual(top_cell.next.next.next.value, 3)
        self.assertIsNone(top_cell.next.next.next.next)
        self.assertTrue(isinstance(top_cell.next.next.next, Cell))
        self.assertFalse(isinstance(top_cell.next.next.next, Sentinel))

        top_cell = make_list((1, 2), use_sentinel=False)
        self.assertTrue(isinstance(top_cell, Cell))
        self.assertFalse(isinstance(top_cell, TopSentinel))
        self.assertIn('next', top_cell.__dict__)
        self.assertNotIn('prev', top_cell.__dict__)
        self.assertFalse(top_cell.is_doubly_linked)
        self.assertEqual(top_cell.value, 1)
        self.assertEqual(top_cell.next.value, 2)
        self.assertIsNone(top_cell.next.next)
        self.assertTrue(isinstance(top_cell.next, Cell))
        self.assertFalse(isinstance(top_cell.next, Sentinel))

        top_cell = make_list('ab')
        self.assertEqual(top_cell.next.value, 'a')
        self.assertEqual(top_cell.next.next.value, 'b')

        top_cell = make_list(['c', 'd'], use_sentinel=False)
        self.assertEqual(top_cell.value, 'c')
        self.assertEqual(top_cell.next.value, 'd')

        top_cell = make_list('ab', is_doubly_linked=True)
        self.assertTrue(isinstance(top_cell, TopSentinel))
        self.assertEqual(top_cell.next.value, 'a')
        self.assertEqual(top_cell.next.next.value, 'b')
        self.assertIn('next', top_cell.__dict__)
        self.assertIn('prev', top_cell.__dict__)
        self.assertTrue(top_cell.is_doubly_linked)
        self.assertTrue(isinstance(top_cell.next.next.next, BottomSentinel))
        self.assertIsNone(top_cell.next.next.next.next)
        self.assertIsNone(top_cell.next.next.next.value)
        self.assertEqual(top_cell.next.prev, top_cell)
        self.assertEqual(top_cell.next.next.prev, top_cell.next)
        self.assertEqual(top_cell.next.next.next.prev, top_cell.next.next)

        top_cell = make_list('ab', use_sentinel=False, is_doubly_linked=True)
        self.assertTrue(isinstance(top_cell, Cell))
        self.assertFalse(isinstance(top_cell, Sentinel))
        self.assertEqual(top_cell.value, 'a')
        self.assertEqual(top_cell.next.value, 'b')
        self.assertIn('next', top_cell.__dict__)
        self.assertIn('prev', top_cell.__dict__)
        self.assertTrue(top_cell.is_doubly_linked)
        self.assertIsNone(top_cell.next.next)
        self.assertEqual(top_cell.next.prev, top_cell)

    def test_iterate(self):
        values = [1, 2, 3]

        _list = make_list(values)
        self.assertListValues(_list, values)

        _list = make_list(values, use_sentinel=False)
        self.assertListValues(_list, values)

        _list = make_list(values, is_doubly_linked=True)
        self.assertListValues(_list, values)

        _list = make_list(values, use_sentinel=False, is_doubly_linked=True)
        self.assertListValues(_list, values)

    def assertListValues(self, _list, values):
        _values = [cell.value for cell in iterate(_list)]
        self.assertEqual(_values, values)

    def test_add_at_beginning(self):
        values = [1, 2, 3]

        _list = make_list(values)
        new_cell = Cell('a')
        new_list = add_at_beginning(_list, new_cell)
        self.assertListValues(new_list, ['a'] + values)
        self.assertTrue(isinstance(new_list, TopSentinel))

        _list = make_list(values, is_doubly_linked=True)
        new_cell = Cell('b', is_doubly_linked=True)
        new_list = add_at_beginning(_list, new_cell)
        self.assertListValues(new_list, ['b'] + values)
        self.assertTrue(isinstance(new_list, TopSentinel))

        _list = make_list(values, use_sentinel=False)
        new_cell = Cell('c')
        self.assertRaises(AssertionError, add_at_beginning, _list, new_cell)

    def test_add_at_end(self):
        values = [1, 2, 3]

        _list = make_list(values)
        new_cell = Cell('a')
        new_list = add_at_end(_list, new_cell)
        self.assertListValues(new_list, values + ['a'])
        self.assertTrue(isinstance(new_list, TopSentinel))

        _list = make_list(values, is_doubly_linked=True)
        new_cell = Cell('b', is_doubly_linked=True)
        new_list = add_at_end(_list, new_cell)
        self.assertListValues(new_list, values + ['b'])
        self.assertTrue(isinstance(new_list, TopSentinel))

        _list = make_list(values, use_sentinel=False)
        new_cell = Cell('c')
        self.assertRaises(AssertionError, add_at_end, _list, new_cell)

    def test_insert_cell(self):
        values = [1, 2, 3]
        _list = make_list(values)
        new_cell = Cell('a')

        none_value = insert_cell(_list.next, new_cell)
        self.assertIsNone(none_value)
        self.assertListValues(_list, [1, 'a', 2, 3])

        insert_cell(_list.next.next, Cell('b'))
        self.assertListValues(_list, [1, 'a', 'b', 2, 3])

        _list = make_list(values, is_doubly_linked=True)
        new_cell = Cell('d', is_doubly_linked=True)

        none_value = insert_cell(_list.next.next, new_cell)
        self.assertIsNone(none_value)
        self.assertListValues(_list, [1, 2, 'd', 3])

    def test_delete_cell(self):
        values = [1, 2, 3]
        _list = make_list(values)

        none_value = delete_cell(_list.next)
        self.assertIsNone(none_value)
        self.assertListValues(_list, [1, 3])

        self.assertRaises(AssertionError, delete_cell, _list.next.next)

        delete_cell(_list)
        self.assertListValues(_list, [3])

        delete_cell(_list)
        self.assertListValues(_list, [])

        _list = make_list(values, is_doubly_linked=True)
        none_value = delete_cell(_list.next.next)
        self.assertIsNone(none_value)
        self.assertListValues(_list, [1, 2])

        self.assertRaises(AssertionError, delete_cell, _list.next.next)

        delete_cell(_list)
        self.assertListValues(_list, [2])

        delete_cell(_list)
        self.assertListValues(_list, [])

        self.assertRaises(AssertionError, delete_cell, _list)
        self.assertRaises(AssertionError, delete_cell, _list.next)

    def test_insert_into_sorted(self):

        values = [1, 3, 4]
        _list = make_list(values)
        none_value = insert_into_sorted(_list, Cell(2))
        self.assertIsNone(none_value)
        self.assertListValues(_list, [1, 2, 3, 4])

        values = [3, 4]
        _list = make_list(values)
        insert_into_sorted(_list, Cell(2))
        self.assertListValues(_list, [2, 3, 4])

        values = [3]
        _list = make_list(values)
        insert_into_sorted(_list, Cell(2))
        self.assertListValues(_list, [2, 3])

        values = [3]
        _list = make_list(values)
        insert_into_sorted(_list, Cell(4))
        self.assertListValues(_list, [3, 4])

        values = [1, 2]
        _list = make_list(values)
        insert_into_sorted(_list, Cell(3))
        self.assertListValues(_list, [1, 2, 3])

        values = [1, 3, 4]
        _list = make_list(values, is_doubly_linked=True)
        none_value = insert_into_sorted(_list, Cell(2, is_doubly_linked=True))
        self.assertIsNone(none_value)
        self.assertListValues(_list, [1, 2, 3, 4])

        values = [1, 3, 4]
        _list = make_list(values, is_doubly_linked=True)
        insert_into_sorted(_list, Cell(0, is_doubly_linked=True))
        self.assertListValues(_list, [0, 1, 3, 4])

        values = [1]
        _list = make_list(values, is_doubly_linked=True)
        insert_into_sorted(_list, Cell(0, is_doubly_linked=True))
        self.assertListValues(_list, [0, 1])

        values = [1, 2, 3]
        _list = make_list(values, is_doubly_linked=True)
        insert_into_sorted(_list, Cell(4, is_doubly_linked=True))
        self.assertListValues(_list, [1, 2, 3, 4])
