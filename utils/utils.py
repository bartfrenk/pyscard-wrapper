
def flatmap(sequence):
    return sum(sequence, [])


def int_to_bytes(number, length=None):
    modulus = 0x100
    current = number
    result = []
    while current != 0:
        result.append(current % modulus)
        current = current / modulus
    if length and len(result) < length:
        result += [0x00 for _ in range(length - len(result))]
    result.reverse()
    return result
