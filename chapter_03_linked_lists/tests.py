import unittest
from .models import Cell, Sentinel, TopSentinel, BottomSentinel
from .algorithms import make_list, iterate, add_at_beginning, add_at_end, \
    insert_cell, delete_cell, insert_into_sorted, copy_list, find_cell, \
    find_cell_before__no_sentinel, find_cell_before__sentinel


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
        self.assertTrue(isinstance(top_cell.bottom_sentinel, BottomSentinel))

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
        self.assertNotIn('bottom_sentinel', top_cell.__dict__)

    def test_iterate(self):
        values = [1, 2, 3]

        top_cell = make_list(values)
        self.assertListValues(top_cell, values)

        top_cell = make_list(values, use_sentinel=False)
        self.assertListValues(top_cell, values)

        top_cell = make_list(values, is_doubly_linked=True)
        self.assertListValues(top_cell, values)

        top_cell = make_list(values, use_sentinel=False, is_doubly_linked=True)
        self.assertListValues(top_cell, values)

    def assertListValues(self, top_cell, values):
        _values = [cell.value for cell in iterate(top_cell)]
        self.assertEqual(_values, values)

    def test_find_cell(self):
        values = [1, 2, 3]
        target_value = 3
        top_cell = make_list(values)
        target_cell = find_cell(top_cell, target_value)
        self.assertEqual(target_cell.value, target_value)

    def test_find_cell_before__no_sentinel(self):
        values = [1, 2, 3]
        target_value = 2
        top_cell = make_list(values, use_sentinel=False)
        cell_before = find_cell_before__no_sentinel(top_cell, target_value)
        self.assertEqual(cell_before.next.value, target_value)

        target_value = 1
        cell_before = find_cell_before__no_sentinel(top_cell, target_value)
        self.assertIsNone(cell_before)

    def test_find_cell_before__sentinel(self):
        values = [1, 2, 3]
        target_value = 2
        top_cell = make_list(values)
        cell_before = find_cell_before__sentinel(top_cell, target_value)
        self.assertEqual(cell_before.next.value, target_value)

        target_value = 1
        cell_before = find_cell_before__sentinel(top_cell, target_value)
        self.assertIsNotNone(cell_before)
        self.assertEqual(cell_before.next.value, target_value)

    def test_add_at_beginning(self):
        values = [1, 2, 3]

        top_cell = make_list(values)
        new_cell = Cell('a')
        newtop_cell = add_at_beginning(top_cell, new_cell)
        self.assertListValues(newtop_cell, ['a'] + values)
        self.assertTrue(isinstance(newtop_cell, TopSentinel))

        top_cell = make_list(values, is_doubly_linked=True)
        new_cell = Cell('b', is_doubly_linked=True)
        newtop_cell = add_at_beginning(top_cell, new_cell)
        self.assertListValues(newtop_cell, ['b'] + values)
        self.assertTrue(isinstance(newtop_cell, TopSentinel))

        top_cell = make_list(values, use_sentinel=False)
        new_cell = Cell('c')
        self.assertRaises(AssertionError, add_at_beginning, top_cell, new_cell)

    def test_add_at_end(self):
        values = [1, 2, 3]

        top_cell = make_list(values)
        new_cell = Cell('a')
        newtop_cell = add_at_end(top_cell, new_cell)
        self.assertListValues(newtop_cell, values + ['a'])
        self.assertTrue(isinstance(newtop_cell, TopSentinel))

        top_cell = make_list(values, is_doubly_linked=True)
        new_cell = Cell('b', is_doubly_linked=True)
        newtop_cell = add_at_end(top_cell, new_cell)
        self.assertListValues(newtop_cell, values + ['b'])
        self.assertTrue(isinstance(newtop_cell, TopSentinel))

        top_cell = make_list(values, use_sentinel=False)
        new_cell = Cell('c')
        self.assertRaises(AssertionError, add_at_end, top_cell, new_cell)

    def test_insert_cell(self):
        values = [1, 2, 3]
        top_cell = make_list(values)
        new_cell = Cell('a')

        none_value = insert_cell(top_cell.next, new_cell)
        self.assertIsNone(none_value)
        self.assertListValues(top_cell, [1, 'a', 2, 3])

        insert_cell(top_cell.next.next, Cell('b'))
        self.assertListValues(top_cell, [1, 'a', 'b', 2, 3])

        top_cell = make_list(values, is_doubly_linked=True)
        new_cell = Cell('d', is_doubly_linked=True)

        none_value = insert_cell(top_cell.next.next, new_cell)
        self.assertIsNone(none_value)
        self.assertListValues(top_cell, [1, 2, 'd', 3])

    def test_delete_cell(self):
        values = [1, 2, 3]
        top_cell = make_list(values)

        none_value = delete_cell(top_cell.next)
        self.assertIsNone(none_value)
        self.assertListValues(top_cell, [1, 3])

        self.assertRaises(AssertionError, delete_cell, top_cell.next.next)

        delete_cell(top_cell)
        self.assertListValues(top_cell, [3])

        delete_cell(top_cell)
        self.assertListValues(top_cell, [])

        top_cell = make_list(values, is_doubly_linked=True)
        none_value = delete_cell(top_cell.next.next)
        self.assertIsNone(none_value)
        self.assertListValues(top_cell, [1, 2])

        self.assertRaises(AssertionError, delete_cell, top_cell.next.next)

        delete_cell(top_cell)
        self.assertListValues(top_cell, [2])

        delete_cell(top_cell)
        self.assertListValues(top_cell, [])

        self.assertRaises(AssertionError, delete_cell, top_cell)
        self.assertRaises(AssertionError, delete_cell, top_cell.next)

    def test_insert_into_sorted(self):

        values = [1, 3, 4]
        top_cell = make_list(values)
        none_value = insert_into_sorted(top_cell, Cell(2))
        self.assertIsNone(none_value)
        self.assertListValues(top_cell, [1, 2, 3, 4])

        values = [3, 4]
        top_cell = make_list(values)
        insert_into_sorted(top_cell, Cell(2))
        self.assertListValues(top_cell, [2, 3, 4])

        values = [3]
        top_cell = make_list(values)
        insert_into_sorted(top_cell, Cell(2))
        self.assertListValues(top_cell, [2, 3])

        values = [3]
        top_cell = make_list(values)
        insert_into_sorted(top_cell, Cell(4))
        self.assertListValues(top_cell, [3, 4])

        values = [1, 2]
        top_cell = make_list(values)
        insert_into_sorted(top_cell, Cell(3))
        self.assertListValues(top_cell, [1, 2, 3])

        values = [1, 3, 4]
        top_cell = make_list(values, is_doubly_linked=True)
        none_value = insert_into_sorted(top_cell,
                                        Cell(2, is_doubly_linked=True))
        self.assertIsNone(none_value)
        self.assertListValues(top_cell, [1, 2, 3, 4])

        values = [1, 3, 4]
        top_cell = make_list(values, is_doubly_linked=True)
        insert_into_sorted(top_cell, Cell(0, is_doubly_linked=True))
        self.assertListValues(top_cell, [0, 1, 3, 4])

        values = [1]
        top_cell = make_list(values, is_doubly_linked=True)
        insert_into_sorted(top_cell, Cell(0, is_doubly_linked=True))
        self.assertListValues(top_cell, [0, 1])

        values = [1, 2, 3]
        top_cell = make_list(values, is_doubly_linked=True)
        insert_into_sorted(top_cell, Cell(4, is_doubly_linked=True))
        self.assertListValues(top_cell, [1, 2, 3, 4])
        
    def test_copy(self):
        values = [1, 2, 3]
        top_cell = make_list(values)
        new_top_cell = copy_list(top_cell)
        self.assertTrue(isinstance(new_top_cell, TopSentinel))
        self.assertIsNot(top_cell, new_top_cell)
        self.assertListValues(new_top_cell, values)

        values = [1, 2, 3]
        top_cell = make_list(values, is_doubly_linked=True)
        new_top_cell = copy_list(top_cell)
        self.assertTrue(isinstance(new_top_cell, TopSentinel))
        self.assertIsNot(top_cell, new_top_cell)
        self.assertListValues(new_top_cell, values)
        self.assertTrue(
            isinstance(new_top_cell.bottom_sentinel, BottomSentinel))
        self.assertEqual(new_top_cell.bottom_sentinel.prev.value, 3)
