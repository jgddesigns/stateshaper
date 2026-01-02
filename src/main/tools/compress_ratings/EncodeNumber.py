import random
import sys
import unicodedata



class EncodeNumber:

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.symbols = self.build_symbols()

        self.max_value = 144534

        self.max_slice = 6

        self.original_string = ""

        self.encoded_string = ""

        self.decoded_string = ""

        self.test_size = 100

        self.print_on = True


        self.multi_test(100, 100000)




    def multi_test(self, rounds, test_size=100000):
        passed = 0
        for _ in range(rounds):
            passed += 1 if self.test_run([test_size]) else 0

        print(f"\n\nTested {rounds} times. {passed} out of {rounds} matching.")


    def quick_test(self):
        self.encode()
        self.decode(self.encoded_string, self.symbols)


    def test_run(self, sizes=[50000, 50000, 50000, 100000, 100000, 100000], print_on=False):
        self.print_on = print_on
        for test_size in sizes:
            self.test_size = test_size
            self.encode()
            self.decode(self.encoded_string, self.symbols)
            data_match = self.compare_data()
            self.print_on = True
            print(f"\n\nTest Size: {self.test_size} characters") if self.print_on == True else None
            print(f"\nComparison of original vs decoded strings: {str(data_match)}") if self.print_on == True else None
            compression_string = f"\n{round(((len(self.original_string)-len(self.encoded_string))/len(self.original_string)) * 100)}%" if data_match == True else "None"
            print(f"\nCompression Achieved: {compression_string}") if self.print_on == True else None
            self.print_on = False

            return data_match

    # Creates the master list of symbols used to map the data to. Up to six numbers can be turned into 1, using a slice from the original string as a symbol's position in the 144,534 length array . 
    #
    # @return, symbols (list): A list of all symbols used to map the encoding data to. 
    def build_symbols(self):
        symbols = []

        for codepoint in range(0x110000):
            ch = chr(codepoint)
            cat = unicodedata.category(ch)

            if cat in {
                "Cc", "Cf", "Cs", "Co", "Cn",
                "Mn", "Me", "Sk"
            }:
                continue

            if not ch.isprintable():
                continue

            symbols.append(ch)

        return symbols


    # Returns a test string. 
    #
    # @return, num (string): A test string based on the current class variable, test_size. 
    def get_data(self):
        num = ""
        while len(num) < self.test_size: 
            num = num + str(random.randint(0, 9))
        return num


    # Compresses an integer into a smaller integer by assigning slices of the number to single symbols from a list of known printable symbols. Checks for the max possible value, and if over, reduces the slice size by 1 then re-checks the size until a symbol can be assigned. 
    #
    # @param, data (integer): An integer number of any length. If not passed, a test integer will be created.
    # @return, self.encoding_string: The full string of the processed encoding. 
    def encode(self, data=None):
        data = data if data else self.get_data()
        self.original_string = data
        code = []

        while len(data) > 0:
            length = self.max_slice if len(data) > self.max_slice - 1 else len(data) - 1
            while length >= 0 and len(data) > 0:
                if int(data[:length]) >= self.max_value:
                    length -= 1
                    continue
                else:
                    code.append(self.symbols[int(data[:length])])
                    data = data[length:]
                    length = 5

        self.encoded_string = "".join(code)

        print(f"Encoded String: {self.encoded_string}") if self.print_on == True else None
        print(f"Length of encoded string: {len(self.encoded_string)}") if self.print_on == True else None

        return self.encoded_string
    

    # Compresses an integer into a smaller integer by assigning slices of the number to single symbols from a list of known printable symbols. Checks for the max possible value, and if over, reduces the slice size by 1 then re-checks the size until a symbol can be assigned. 
    #
    # @param, data (integer): An integer number of any length. If not passed, a test integer will be created.
    # @return (string): The string of the index where the current symbol is stored. 
    def get_number(self, symbol, symbols):
        return f"{symbols.index(symbol):05d}"


    def decode(self, code, symbols, print_on=False):
        self.print_on = print_on
        num = ""
        while len(code) > 0:
            num = num + str(self.get_number(code[0], symbols))
            code = code[1:]

        print("\nOriginal string:\n") if self.print_on == True else None
        print(self.original_string) if self.print_on == True else None
        print("\nDecoded string:\n") if self.print_on == True else None
        print(num) if self.print_on == True else None
        self.decoded_string = num
        print(f"\nMatching: {self.compare_data()}") if self.print_on == True else None

        
    def compare_data(self):
        return self.original_string == self.decoded_string
    

EncodeNumber()