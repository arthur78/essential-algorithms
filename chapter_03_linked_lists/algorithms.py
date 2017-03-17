from .models import Cell, TopSentinel, BottomSentinel


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

    # Find the last cell of the list.
    if is_doubly_linked:
        is_not_last_cell = lambda cell: not isinstance(cell, BottomSentinel)
    else:
        is_not_last_cell = lambda cell: cell.next
    last_cell = top_cell
    while is_not_last_cell(last_cell):
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
    else:
        use_sentinel = False
        current_cell = top_cell

    if use_sentinel and current_cell.is_doubly_linked:
        is_not_last_cell = lambda cell: not isinstance(cell, BottomSentinel)
    else:
        is_not_last_cell = lambda cell: cell

    while is_not_last_cell(current_cell):
        yield current_cell
        current_cell = current_cell.next


def make_list(values, use_sentinel=True, is_doubly_linked=False):
    """A helper to create a linked list based on the given values.

    :param values: An iterable of cell values.
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
