'''Systematyczny cykliczny kod Hamminga'''
import logging
import numpy as np
from itertools import combinations_with_replacement
from itertools import permutations
import math


class Hamming:

    """Uruchamia logi"""
    def __init__(self, n=7):
        logging.basicConfig(level=logging.DEBUG)
        self.input = None
        self.output = None
        self.n = n
        self.k = (n+1) - int(math.log((n+1), 2)) - 1
        logging.debug(f"Hamming: Stworzenie hamming ({self.n}, {self.k})")

    """Uogólnione kodowanie Hamminga"""
    def encode(self, data):
        logging.debug(f"Kodowanie Hamminga ({self.n}, {self.k})")
        unpacked = np.unpackbits(data)
        for _ in range(len(unpacked) % self.k):
            unpacked = np.concatenate((unpacked, [0]))
        bits_array = unpacked.reshape(-1, int(self.k))
        output = []
        for bits in bits_array:
            prepared_bits = self.add_parity_bits(bits)
            output.append(self.encode_bits(prepared_bits))
        return np.array(np.packbits(output), dtype=np.uint8)

    """Wstawia zera w miejsca o pozycji będącej potęgą dwójki"""
    def add_parity_bits(self, bits):
        bits_index = 0
        result_bits_counter = 1
        power_of_2 = 1
        result = []
        while result_bits_counter <= self.n:
            if result_bits_counter == power_of_2:
                result.append(0)
                power_of_2 *= 2
            else:
                result.append(bits[bits_index])
                bits_index += 1
            result_bits_counter += 1
        return result

    """Koduje n bitów"""
    def encode_bits(self, bits):
        power_of_2 = 1
        while power_of_2 <= self.k:
            sum = 0
            bits_index = self.n - 1
            while bits_index >= 0:
                for l in range(power_of_2):
                    sum += bits[bits_index]
                    bits_index -= 1
                bits_index -= power_of_2
            bits[power_of_2 - 1] = sum % 2
            power_of_2 *= 2
        return bits

    """Dekodowanie n bitów"""
    def get_corrected_bits(self, bits):
        error = 0
        power_of_two = 1
        while power_of_two <= self.k:
            error += self.k_parity_bit_correctness(bits, power_of_two)
            power_of_two *= 2
        if error:
            error -= 1
            bits[error] = int(not bits[error])
        return bits

    """Uogólnione dekodowanie Hamminga"""
    def decode(self, data):
        unpacked = np.unpackbits(np.array(data, dtype=np.uint8))
        if len(unpacked) % self.n:
            unpacked = unpacked[:-(len(unpacked) % self.n)]

        result = []

        reshaped_data = np.array(unpacked).reshape(-1, self.n)
        for bits in reshaped_data:
            result.append(self.get_data_bits(self.get_corrected_bits(bits)))
        return np.packbits(np.array(result))

    """Wyciąganie bitów informacyjnych"""
    def get_data_bits(self, bits):
        # return sorted(list(
        #   set(range(self.n)) - set(x ** 2 - 1 for x in range(int(self.n ** 0.5)))
        # ))
        power_of_2 = 1
        result = []
        for i in range(self.n):
            if i != power_of_2 - 1:
                result.append(bits[i])
            else:
                power_of_2 *= 2
            i += 1
        return result

    def k_parity_bit_correctness(self, bits, k):
        j = self.n - 1
        sum = 0
        while j >= 0:
            for i in range(k):
                sum += bits[j]
                j -= 1
            j -= k
        if sum % 2 != 0:
            return k
        return 0


"""
print(list(combinations_with_replacement([0, 2], 3)))
hamming = Hamming()
bits = [0, 0, 0, 1]
print(bits)
bits = hamming.add_parity_bits(bits)
print(bits)
bits = hamming.encode_bits(bits)
print(bits)
bits[6] = 0
print(bits)
bits = hamming.get_corrected_bits(bits)
print(bits)
"""



