from .models import Cell, TopSentinel, BottomSentinel, Sentinel


def insert_into_sorted(top_cell, new_cell):
    """Insert a new cell into the sorted list.

    :param top_cell: The list's first cell.
    :type top_cell: TopSentinel
    :param new_cell: The new cell to insert so the list remains sorted.
    :type new_cell: Cell
    :rtype: TopSentinel
    """
    assert isinstance(top_cell, TopSentinel)
    is_doubly_linked = top_cell.is_doubly_linked
    if is_doubly_linked:
        assert new_cell.is_doubly_linked

    def is_last_cell(cell):
        return isinstance(cell.next, BottomSentinel) or not cell.next

    after_me = top_cell
    while not is_last_cell(after_me) and after_me.next < new_cell:
        after_me = after_me.next

    new_cell.next = after_me.next
    after_me.next = new_cell
    if is_doubly_linked:
        new_cell.prev = after_me
        new_cell.next.prev = new_cell


def delete_cell(after_me):
    """Delete the cell after the given cell.

    The deleted (unlinked) cell will be garbage-collected.

    This algorithm takes only a few steps, so it runs in O(1) time.

    :param after_me: The cell after which insert the new cell.
    :type: Cell
    """
    assert after_me.next and not isinstance(after_me.next, BottomSentinel)
    assert not isinstance(after_me, BottomSentinel)

    is_doubly_linked = after_me.is_doubly_linked

    if after_me.next.next:
        after_me.next = after_me.next.next
        if is_doubly_linked:
            after_me.next.prev = after_me
    else:
        after_me.next = None


def insert_cell(after_me, new_cell):
    """Insert a new cell after the cell.

    This algorithm takes only a few steps, so it runs in O(1) time.

    :param after_me: The cell after which insert the new cell.
    :type: Cell
    :param new_cell: The new cell to insert.
    :type: Cell
    """
    assert not isinstance(new_cell, Sentinel)
    is_doubly_linked = after_me.is_doubly_linked
    if is_doubly_linked:
        assert new_cell.is_doubly_linked

    new_cell.next = after_me.next
    after_me.next = new_cell
    if is_doubly_linked:
        new_cell.prev = after_me
        new_cell.next.prev = new_cell


def add_at_end(top_cell, new_cell):
    """Add a new cell at the end of a linked list, represented by its top
    cell.

    This algorithm performs (K + M * N) number of steps, where N is the size
    of the input list and M and K are fixed (and negligible at big N),
    so the algorithm's runtime is O(N).

    :param top_cell: The list's first cell.
    :type top_cell: TopSentinel
    :param new_cell: The new cell to add at the end.
    :type new_cell: Cell
    :rtype: TopSentinel
    """
    assert isinstance(top_cell, TopSentinel)

    is_doubly_linked = top_cell.is_doubly_linked
    if is_doubly_linked:
        assert new_cell.is_doubly_linked

    def is_last(cell):
        return isinstance(cell, BottomSentinel) or not cell.next

    last_cell = top_cell
    while not is_last(last_cell):
        last_cell = last_cell.next

    # Got the last cell. Now adjust the cell links.
    if is_doubly_linked:
        new_cell.prev = last_cell.prev  # Last cell is bottom sentinel.
        new_cell.prev.next = new_cell
        new_cell.next = last_cell
        last_cell.prev = new_cell
    else:
        last_cell.next = new_cell

    return top_cell


def add_at_beginning(top_cell, new_cell):
    """Add a new cell at the beginning of a linked list, represented by its
    top cell.

    The algorithm performs the fixed number of steps, regardless of the size
    of the input list, so its runtime is O(1).

    :param top_cell: The list's first cell.
    :type top_cell: TopSentinel
    :param new_cell: The new cell to add at the beginning.
    :type new_cell: Cell
    :rtype: TopSentinel
    """
    assert isinstance(top_cell, TopSentinel)

    is_doubly_linked = top_cell.is_doubly_linked
    if is_doubly_linked:
        assert new_cell.is_doubly_linked

    new_cell.next = top_cell.next
    top_cell.next = new_cell
    if is_doubly_linked:
        new_cell.prev = top_cell
        new_cell.next.prev = new_cell

    return top_cell


def iterate(top_cell):
    """Iterate over the linked list represented by its top cell.

    :param top_cell: The list's first cell.
    :type top_cell: Cell
    """
    if isinstance(top_cell, TopSentinel):
        use_sentinel = True
        current_cell = top_cell.next
        if not current_cell:  # Empty list.
            return
    else:
        use_sentinel = False
        current_cell = top_cell

    def is_last(cell):
        return (use_sentinel and isinstance(cell, BottomSentinel)) or not cell

    while not is_last(current_cell):
        yield current_cell
        current_cell = current_cell.next


def make_list(values, use_sentinel=True, is_doubly_linked=False):
    """A helper to create a linked list based on the given values.

    :param values: An iterable of cell values.

    :param is_doubly_linked: Doubly linked lists allow for more efficient list
        manipulation. For example, they let addition and removal of cells at
        the list's end in O(1) time.

    :return: A top cell of the created list.
    :rtype: Cell | TopSentinel
    """
    assert len(values) > 0

    if use_sentinel:
        top_cell = TopSentinel(is_doubly_linked)
        values = [None] + list(values)
    else:
        top_cell = Cell(is_doubly_linked=is_doubly_linked)

    current_cell = top_cell
    last_cell_index = len(values) - 1
    for i, value in enumerate(values):
        current_cell.value = value
        if i < last_cell_index:
            next_cell = Cell(is_doubly_linked=is_doubly_linked)
            current_cell.next = next_cell
            if is_doubly_linked:
                next_cell.prev = current_cell
            current_cell = next_cell

    if use_sentinel and is_doubly_linked:
        bottom_cell = BottomSentinel()
        bottom_cell.prev = current_cell
        current_cell.next = bottom_cell

    return top_cell
