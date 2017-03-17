import sys


class Cell(object):

    def __init__(self, value=None, is_doubly_linked=False):
        self.value = value
        self.next = None
        if is_doubly_linked:
            self.prev = None

    @property
    def is_doubly_linked(self):
        return 'prev' in self.__dict__

    def __str__(self):
        return "{}".format(self.value)


class Sentinel(Cell):
    """
    Quote from the book:
        - A sentinel is a cell that is part of the linked list but that doesn't
        contain any meaningful data. It is used only as a placeholder so that
        algorithms can refer to a cell that comes before the first cell.

        - A sentinel may seem like a waste of space, but it removes the need
        special-purpose code and makes the algorithm simpler and more elegant.
    """

    def __init__(self, is_doubly_linked=False):
        super(Sentinel, self).__init__(None, is_doubly_linked)


class TopSentinel(Sentinel):
    pass


class BottomSentinel(Sentinel):

    def __init__(self):
        # Assume a bottom sentinel always implies doubly linked lists.
        super(BottomSentinel, self).__init__(is_doubly_linked=True)
