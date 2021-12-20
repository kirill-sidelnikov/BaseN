import click


class BaseN:

    def __init__(self, base):
        if base == 32:
            self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
        if base == 64:
            self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        else:
            self.alphabet = ''
            for i in range(base):
                self.alphabet += chr(i + 33)

        max_block_bit_count = 0
        bit_length_term = 0
        symbol_quantity_term = 0
        self.base_alph = int(base)
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
                        and ((max_symbol_count / min_bits_count) <= min_comp)):
                    bit_length_term = i
                    symbol_quantity_term = j
                    min_comp = max_symbol_count / min_bits_count
        self.bit_length = int(bit_length_term)
        self.block_byte = int(self.bit_length / 8)
        self.symbol_quantity = int(symbol_quantity_term)

    def encode_block(self, data):
        alphabet = self.alphabet
        base_alph = self.base_alph
        bit_length = self.bit_length
        symbol_quantity = self.symbol_quantity
        bit_str = ''
        base_str = ''
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
            base_str = base_str[0:symbol_quantity - diff_byte]

        return base_str

    def decode_block(self, text):
        alphabet = self.alphabet
        base_alph = self.base_alph
        bit_length = self.bit_length
        symbol_quantity = self.symbol_quantity
        block_byte = self.block_byte
        text_str = ''
        char_indexes = []
        dec_int = 0
        diff_text = 0
        text_len = len(text)

        if text_len != symbol_quantity:
            diff_text = int(symbol_quantity - text_len)
            for i in range(diff_text):
                text += alphabet[base_alph - 1]

        text_len = len(text)

        for char in text:
            char_index = alphabet.index(char)
            char_indexes.append(char_index)

        for i in range(text_len):
            dec_int += int(char_indexes[i]) * pow(base_alph, text_len - i - 1)

        bit_str = bin(dec_int).lstrip('0b')
        bit_str = bit_str.zfill(bit_length)

        for i in range(block_byte):
            bin_byte = bit_str[0:8]
            text_str += chr(int(bin_byte, 2))
            bit_str = bit_str[8:]

        if diff_text != 0:
            text_str = text_str[0:block_byte - diff_text]

        return text_str.encode("ISO-8859-1")

    def base_encode(self, inFile, outFile):
        output = open(outFile, 'w', encoding="UTF-8")
        with open(inFile, 'rb') as input:
            bytes = input.read(self.block_byte)
            while bytes:
                output.write(self.encode_block(bytes))
                bytes = input.read(self.block_byte)
            output.close()
        input.close()

    def base_decode(self, inFile, outFile):
        output = open(outFile, 'wb')
        with open(inFile, 'r', encoding="UTF-8") as input:
            bytes = input.read(self.symbol_quantity)
            while bytes:
                output.write(self.decode_block(bytes))
                bytes = input.read(self.symbol_quantity)
            output.close()
        input.close()


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.option('-b', '--base', default=64, help='Base alphabet length.')
@click.option('-e', '--encode', 'mode', flag_value='encode', default=True, help='Encode mode.')
@click.option('-d', '--decode', 'mode', flag_value='decode', help='Decode mode.')
def main(input, output, base, mode):
    basen = BaseN(base)
    if mode == 'encode':
        basen.base_encode(input, output)
    elif mode == 'decode':
        basen.base_decode(input, output)


if __name__ == "__main__":
    main()
