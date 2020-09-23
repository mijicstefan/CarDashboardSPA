from sll.node import Node

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        new_node = Node(value)

        if self.size == 0:
            self.head = new_node
            self.tail = new_node

        elif self.head == self.tail:
            self.head.pointer = new_node
            self.tail = new_node

        else:
            self.tail.pointer = new_node
            self.tail = new_node
        self.size += 1

    def prepend(self, value):
        new_node = Node(value)

        if self.size == 0:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.pointer = self.head
            self.head = new_node
        self.size += 1

    def remove_first(self):

        if self.size == 0:
            return

        elif self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.pointer
        self.size -= 1

    def remove_last(self):

        if self.size == 0:
            return

        elif self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            current = self.head
            while current.pointer != self.tail:
                current = current.pointer
            current.pointer = None
            self.tail = current
        self.size -= 1

    def first(self):
        if self.size > 0:
            return self.head.value

    def last(self):
        if self.size > 0:
            return self.tail.value

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.pointer

    def __len__(self):
        return self.size
