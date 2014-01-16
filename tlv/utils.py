class DictNode(object):

    def __init__(self, children=None):
        self.children = children or {}

    def __getitem__(self, label):
        return self.get(label)

    def __contains__(self, labels):
        if len(labels) == 0:
            return True
        elif labels[0] in self.children:
            return self.children[labels[0]].__contains__(labels[1:])
        else:
            return False

    def __iter__(self):
        return self.depth_first()

    def depth_first(self):
        pass

    def breadth_first(self):
        pass

    def attach(self, label, node):
        self.children[label] = node
        return node

    def add(self, label, *args):
        self.children[label] = DictNode(*args)
        return self.children[label]

    def get(self, *labels):
        if len(labels) == 0:
            return self
        return self.children[labels[0]].get(*labels[1:])

    def display(self):
        # prints node details: override this method in descendants
        print self


class DictTree(DictNode):

    def root(self):
        return self


class ListNode(object):

    default_label = None

    def __init__(self, label=None, children=None):
        self.children = children or []
        self.label = label or ListNode.default_label

    def append(self, label, children):
        node = ListNode(label, children = children)
        self.children.append(node)
        return node

    def add(self, label, *args):
        node = ListNode(label, *args)
        self.children.append(node)
        return node

    def attach(self, *children):
        self.children += children

    def get(self, *labels):
        """
        Return iterator over all node instances with the specified cumulative label.
        """
        if len(labels) == 0:
            yield self
        else:
            for tree in (child for child in self.children if child.label == labels[0]):
                for node in tree.get(*labels[1:]):
                    yield node


def test_dict_tree():
    tree = DictTree()
    tree.add("a").add("c")
    tree.add("b")
    print tree.get() is tree
    print tree.children
    print tree.get("a").children
    print ["a","b"] in tree
    print ["a","c"] in tree
    print ["a"] in tree
    print tree["a"].children

def test_list_node():
    tree = ListNode()
    tree.add("a").add("c")
    tree.add("a")
    tree.add("b")
    for node in tree.get("a"):
        print node.label
    for node in tree.get("a", "c"):
        print node.label
    for node in tree.get("a", "b"):
        print node.label



if __name__ == '__main__':
    test_list_node()

