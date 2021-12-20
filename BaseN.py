alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def Encode(data):
    bit_str = ''
    base_str = ''
    diff = 0

    for byte in data:
        bin_byte = bin(byte).lstrip('0b')
        bin_byte = bin_byte.zfill(8)
        bit_str += bin_byte

    if len(bit_str) != 24:
        diff = 24 - len(bit_str)
        bit_str = bit_str.ljust(24, '0')

    dec_int = int(bit_str, 2)

    base_indexes = []
    for i in range(4):
        base_index = dec_int % 64
        base_indexes.append(base_index)
        dec_int = dec_int // 64
    base_indexes.reverse()

    for base_index in base_indexes:
        base_str += alphabet[base_index]

    if diff == 8:
        base_str = base_str[0:3] + '='
    elif diff == 16:
        base_str = base_str[0:2] + '=='

    return base_str


def baseEncode(inFile, outFile):
    output = open(outFile, 'w')
    with open(inFile, 'rb') as input:
        bytes = input.read(3)
        while bytes:
            output.write(Encode(bytes))
            bytes = input.read(3)
        input.close()
    output.close()
