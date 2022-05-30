class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_children(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def __reversed__(self):
        return reversed(self._children)

    def __len__(self):
        return len(self._children)

    def depth_first(self):
        yield self
        for ch in self:
            yield from ch.depth_first()


if __name__ == '__main__':
    root = Node(0)
    for i in range(1, 10):
        node = Node(i)
        for j in range(1, 5):
            node.add_children(Node(i * j))
        root.add_children(node)

    for ch in reversed(root):
        print(ch, end=':')
        for ch1 in ch:
            print(ch1, end=' ')
        print('length-{!r}\r'.format(len(ch)))

    for ch in root.depth_first():
        print(ch, end=' ')
