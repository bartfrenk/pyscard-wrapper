from smartcard.util import toHexString
from random import randint


class SliceIterator:
    """Iterates over subiterators of fixed length."""

    def __init__(self, lst, steps):
        self.lst = lst
        self.steps = steps
        self.current = 0

    def __iter__(self):
        return self

    def next(self):
        if self.current < len(self.lst):
            result = self.lst[self.current:self.current + self.steps]
            self.current += self.steps
            return result
        else:
            raise StopIteration


def to_hex_str(bytes, max_display_length=None):
    """Convert a bytestring to its hexadecimal representation."""
    if max_display_length is None:
        return toHexString(bytes)
    else:
        result = ""
        for word in SliceIterator(bytes, max_display_length):
            result += toHexString(word) + "\n"
        return result[:-1]


def ubq_rand(n):
    """Generate a random ubiqu-1 message with specified payload length."""
    header = [randint(0, 0xFF) for _ in range(60)]
    payload = [randint(0, 0xFF) for _ in range(n)]
    length = [n / 0x100, n % 0x100]
    return header + length + [~x for x in length] + payload


def to_byte_list(hex_string):
    # assume that hex_string has no spaces nor indicating characters,
    # such as '0x', or ':'
    if len(hex_string) % 2 != 0:
        raise ValueError("String must be of even length.")
    else:
        return [int(byte, 16) for byte in SliceIterator(hex_string, 2)]


if __name__ == "__main__":
    for word in SliceIterator(ubq_rand(31), 8):
        print(to_hex_str(word))
    print(to_hex_str(to_byte_list("A0FF10")))
