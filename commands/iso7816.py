from utils import to_hex_str


class StatusWord(object):

    codes = {(0x90, 0x00): 'SW_OKAY',
             (0x69, 0x84): 'SW_DATA_INVALID',
             (0x6A, 0x86): 'SW_INCORRECT_P1P2',
             (0x67, 0x00): 'SW_WRONG_LENGTH'}

    def __init__(self, sw):
        self.sw = sw

    def __str__(self):
        return self.__class__.codes.get(self.sw, to_hex_str(list(self.sw)))

    def __eq__(self, other):
        return self.sw == other.sw

    def __ne__(self, other):
        return self.sw != other.sw

