from iso7816 import StatusWord
from termcolor import colored
from utils import SliceIterator, to_hex_str, ubq_rand

# TODO: print command APDUs when requested
# TODO: clean up output from a call to a Test instance
# TODO: add a Timed mixin, to measure the time taken for commands

class Response(object):
    """Store the response APDU in a structured way."""

    display_width = 16

    def __init__(self, data, sw):
        self.data = data
        if sw is None:
            self.sw = sw
        else:
            self.sw = StatusWord(sw)

    def __str__(self):
        result = "SW: " + str(self.sw) + "\n"
        if self.data is not None:
            for word in SliceIterator(self.data, self.__class__.display_width):
                result += to_hex_str(word) + "\n"
        return result

    def matches(self, other):
        return (self.sw is None or self.sw == other.sw) and \
               (self.data is None or self.data == other.data)


class Command(object):
    """Send command APDUs to the smart card."""

    def __init__(self, label, apdu, verbosity=0):
        self.label = label
        self.apdu = apdu
        self.verbosity = verbosity

    def __call__(self, context):
        (data, sw1, sw2) = context.cardservice.connection.transmit(self.apdu)
        return self.process(Response(data, (sw1, sw2)))

    def process(self, response):
        return self.label + ": " + str(response)


class Test(Command):
    """Test the response of card commands."""

    msg = {
        True: colored("Success", "green"),
        False: colored("Failure", "red")
    }

    def __init__(self, label, apdu, rdata=None, sw=(0x90, 0x00)):
        super(Test, self).__init__(label, apdu)
        self.expected = Response(rdata, sw)

    def process(self, response):
        report = self.label + ": "
        if self.expected.matches(response):
            report += self.__class__.msg[True]
        else:
            report += self.__class__.msg[False] + "\n" + \
                      "Expected: " + str(self.expected) + "\n" + \
                      "Response: " + str(response)
        return report


if __name__ == "__main__":

    print(Response(ubq_rand(20), (0x90, 0x00)))
    print(Response(None, (0x90, 0x01)))
    print(Response([], (0x63, 0x02)))

    response = Response([0x00 for _ in range(10)], (0x90, 0x00))
    expected = Response(None, (0x90, 0x00))
    print(expected.matches(response))
    test = Test('test', [0x00, 0x00, 0x00, 0x00, 0x00])
    print(test.process(Response([0x00, 0x00, 0x00, 0x00, 0x00], (0x90, 0x00))))
