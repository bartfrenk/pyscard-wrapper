

class CAPDU(object):

    offsets = {"cla": 0, "ins": 1, "p1": 2, "p2": 3, "lc": 4}

    def __init__(self, bytes):
        if hasattr(bytes, "__len__") and len(bytes) >= len(CAPDU.offsets):
            for (name, offset) in CAPDU.offsets.items():
                setattr(self, name, bytes[offset])
            self.cdata = bytes[len(CAPDU.offsets):]
        else:
            raise ValueError("Invalid command APDU")


class RAPDU(object):

    offsets = {"sw1": -2, "sw2": -1}

    def __init__(self, bytes):
        if hasattr(bytes, "__len__") and len(bytes) >= len(RAPDU.offsets):
            for (name, offset) in RAPDU.offsets.items():
                setattr(self, name, bytes[offset])
            self.rdata = bytes[:-len(RAPDU.offsets)]
        else:
            raise ValueError("Invalid response APDU")

