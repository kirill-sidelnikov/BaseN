def CalcSize(base):
    global base_alph
    base_alph = int(base)
    min_comp = 16
    if base <= 188:
        max_block_bit_count = 64
    elif base >= 189:
        max_block_bit_count = 256
    for i in range(max_block_bit_count, 7, -8):
        for j in range(25):
            min_bits_count = pow(2, i)
            max_symbol_count = pow(base, j)
            if ((max_symbol_count >= min_bits_count)
                    and ((max_symbol_count/min_bits_count) <= min_comp)):
                bit_length_term = i
                symbol_quantity_term = j
                min_comp = max_symbol_count/min_bits_count
    global bit_length
    bit_length = int(bit_length_term)
    global block_byte
    block_byte = int(bit_length / 8)
    global symbol_quantity
    symbol_quantity = int(symbol_quantity_term)


def Alphabet(base):
    global alphabet
    if base == 32:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    if base == 64:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    else:
        alphabet = ''
        for i in range(base):
            alphabet += chr(i+33)
        return alphabet


def EncodeBlock(data):
    bit_str = ''
    base_str = ''
    diff_bit = 0
    diff_byte = 0

    for byte in data:
        bin_byte = bin(byte).lstrip('0b')
        bin_byte = bin_byte.zfill(8)
        bit_str += bin_byte

    if len(bit_str) != bit_length:
        diff_bit = bit_length - len(bit_str)
        diff_byte = int(diff_bit / 8)
        bit_str = bit_str.ljust(bit_length, '0')

    dec_int = int(bit_str, 2)

    base_indexes = []
    for i in range(symbol_quantity):
        base_index = dec_int % base_alph
        base_indexes.append(base_index)
        dec_int = dec_int // base_alph
    base_indexes.reverse()

    for base_index in base_indexes:
        base_str += alphabet[base_index]

    if diff_byte != 0:
        base_str = base_str[0:symbol_quantity-diff_byte]

    return base_str


def DecodeBlock(text):
    bit_str = ''
    bin_byte = ''
    text_str = ''
    char_indexes = []
    dec_int = 0
    diff_text = 0
    text_len = len(text)

    if text_len != symbol_quantity:
        diff_text = int(symbol_quantity - text_len)
        for i in range(diff_text):
            text += alphabet[base_alph-1]

    text_len = len(text)

    for char in text:
        char_index = alphabet.index(char)
        char_indexes.append(char_index)

    for i in range(text_len):
        dec_int += int(char_indexes[i]) * pow(base_alph, text_len-i-1)

    bit_str = bin(dec_int).lstrip('0b')
    bit_str = bit_str.zfill(bit_length)

    for i in range(block_byte):
        bin_byte = bit_str[0:8]
        text_str += chr(int(bin_byte, 2))
        bit_str = bit_str[8:]

    if diff_text != 0:
        text_str = text_str[0:block_byte-diff_text]

    return text_str.encode("ISO-8859-1")


def baseEncode(inFile, outFile):
    output = open(outFile, 'w', encoding="UTF-8")
    with open(inFile, 'rb') as input:
        bytes = input.read(block_byte)
        while bytes:
            output.write(EncodeBlock(bytes))
            bytes = input.read(block_byte)
        output.close()
    input.close()


def baseDecode(inFile, outFile):
    output = open(outFile, 'wb')
    with open(inFile, 'r', encoding="UTF-8") as input:
        bytes = input.read(symbol_quantity)
        while bytes:
            output.write(DecodeBlock(bytes))
            bytes = input.read(symbol_quantity)
        output.close()
    input.close()
