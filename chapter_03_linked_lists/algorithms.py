from .models import Cell, TopSentinel, BottomSentinel


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

    is_doubly_linked = 'prev' in current_cell.__dict__
    if use_sentinel and is_doubly_linked:
        condition = lambda cell: not isinstance(cell, BottomSentinel)
    else:
        condition = lambda cell: cell.next

    while condition(current_cell):
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
    for value in values:
        current_cell.value = value
        next_cell = Cell(is_doubly_linked=is_doubly_linked)
        current_cell.next = next_cell
        if is_doubly_linked:
            next_cell.prev = current_cell
        current_cell = next_cell

    if use_sentinel and is_doubly_linked:
        bottom_cell = BottomSentinel()
        bottom_cell.prev = current_cell.prev
        current_cell.prev.next = bottom_cell

    return top_cell
