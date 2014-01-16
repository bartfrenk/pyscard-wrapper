from sys import argv
from ..commands.utils import to_byte_list
from apdus import CAPDU, RAPDU


class GPShellParser(object):

    prefixes = {"Response", "Wrapped command", "Command"}
    apdus = {"-->": CAPDU, "<--": RAPDU}

    def __init__(self):
        pass

    @classmethod
    def parse(cls, file_name):
        with open(file_name) as file:
            commands = []
            current = {}
            for line in file:
                terms = cls._dissect_line(line)
                if terms:
                    if terms["prefix"] == "Command" and current:
                        commands.append(current);
                        current = {}
                    current[terms["prefix"]] = cls._get_apdu(terms)
            return commands

    @classmethod
    def _dissect_line(cls, line):
        for prefix in cls.prefixes:
            if line.startswith(prefix):
                terms = line.split()
                return {"prefix": prefix, "infix": terms[-2], "apdu": terms[-1]}
        return None

    @classmethod
    def _get_apdu(cls, terms):
        return cls.apdus[terms["infix"]](to_byte_list(terms["apdu"]))




if __name__ == "__main__":
    if len(argv) > 1:
        try:
            print(GPShellParser.parse(argv[1]))
        except IOError:
            print("File " + argv[1] + " does not exist.")
    else:
        print("Specify gpshell output file to parse.")
