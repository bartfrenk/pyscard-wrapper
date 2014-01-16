# TODO: implement iterator over a bound data tree (i.e. one that has parsed a response)
# TODO: find clear way to print a parsed message

#import sys
#sys.path.append(".")
#
import utils


class ParseError(BaseException):
    pass


class TaggingError(LookupError):
    pass


class TagNode(utils.DictNode):

    def __init__(self, tags=None):
        super(TagNode, self).__init__()
        if tags:
            self.set(tags)

    def set(self, tags):
        previous = None
        for tag in tags:
            if isinstance(tag, list):
                if not previous:
                    raise ParseError("Not a valid tag tree.")
                else:
                    self.attach(previous, TagNode(tag))
            else:
                # always make sure to store tag as a tuple, even if it only
                # consists of a single symbol
                if isinstance(tag, tuple):
                    self.add(tag)
                    previous = tag
                else:
                    self.add((tag,))
                    previous = (tag,)
        return self

    def add(self, label, *args):
        self.children[label] = TagNode(*args)
        return self.children[label]

    def get(self, *labels):
        if len(labels) == 0:
            return self
        if isinstance(labels[0], tuple):
            return self.children[labels[0]].get(*labels[1:])
        else:
            return self.children[(labels[0],)].get(*labels[1:])

    def get_tag(self, sentence):

        def is_prefix(child):
            return list(child) == sentence[:len(child)]

        matches = filter(is_prefix, self.children)
        if len(matches) > 1:
            raise TaggingError('Multiple tags matching the initial segment.')
        return matches[0] if matches else None


class TagTree(TagNode):

    def root(self):
        return self


class AnyTag(TagTree):

    def get_tag(self, sentence):
        return self


class TaggedDataNode(utils.ListNode):

    def parse(self, sentence, format=None):
        i = 0
        unstructured = []
        while i < len(sentence):
            tag = format.get_tag(sentence[i:])
            if tag:
                if unstructured:
                    self.attach(UntaggedDataNode().store(unstructured))
                    unstructured = []
                length = sentence[i + len(tag)]
                content = sentence[i + len(tag) + 1: i + len(tag) + length + 1]
                self.attach(TaggedDataNode(tag).parse(content, format[tag]))
                i += len(tag) + length + 1
            else:
                unstructured.append(sentence[i])
                i += 1
        self.attach(UntaggedDataNode(unstructured))

        return self


class UntaggedDataNode(object):

    def __init__(self, content=None):
        self.content = content


class DataTree(TaggedDataNode):

    def __init__(self, format):
        self.children = []
        if isinstance(format, TagNode):
            self.format = format
        elif isinstance(format, list):
            # assume format is essentially a tree of tag implemented
            # with nested lists
            self.format = TagTree(format)

    def root(self):
        return self

    def parse(self, sentence):
        super(DataTree, self).parse(sentence, self.format)


def TLVParser(DataTree):
    pass


def test_tagtree():
    tree = TagTree([0x10, 0x20, [0x21, 0x22], 0x30])
    print(tree)


def test_datanode():
    tree = DataTree(TagTree([0x10, 0x20, [0x21, 0x22], 0x30]))
    tree.parse([0x10, 2, 0x0A, 0x0B, 0x20, 7, 0x21, 2, 0x2A, 0x2B, 0x22, 1, 0x2C,
                0x30, 4, 0x00, 0x00, 0x00, 0x00])
    print(tree)


if __name__ == "__main__":
    test_tagtree()
    test_datanode()
