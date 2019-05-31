'''Systematyczny cykliczny kod Hamminga'''
import logging
import numpy as np


class Hamming:

    n = 7
    k = 4

    P = np.array([
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 1],
        [1, 0, 1]
    ])

    G = np.concatenate((P, np.identity(k)), axis=1)

    H = np.concatenate((np.identity(n-k), P.T), axis=1)

    # Tabela dekodowania, syndrom s postaci np. 011 odpowiada poprawce o ind 3
    S = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])

    ''' uruchamia logi'''
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Stworzenie Hamming")
        self.input = None
        self.output = None

    '''Koduje numpyArray kodem (7, 4)'''
    def encode(self, numpyArray):
        logging.debug("Kodowanie Hamminga(7, 4)")
        output = []
        bits_array = np.unpackbits(numpyArray).reshape(-1, 4)
        for i, bits in enumerate(bits_array):
            if not i % 1000:
                print(i/len(bits_array))
            extra = bits.dot(Hamming.G)
            extra %= 2
            output.append([int(x) for x in extra.tolist()])
        logging.debug("Kodowanie obliczone, pakowanie bitów")
        #print(output[:10])
        np_out = np.packbits(output)
        #print(repr(np_out[:5]))
        logging.debug("Kodowanie skończone")
        return np_out

    '''Dekoduje numpyArray kodem (7, 4)'''
    def decode(self, numpyArray):
        logging.debug("Dekodowanie Hamminga(7, 4)")
        print('numpy array: ', repr(numpyArray[:7]))
        output = []
        unpacked_out = np.unpackbits(numpyArray)
        print('unpacked: ', repr(unpacked_out[:7]), 'len: ', len(unpacked_out), 'mod7: ', (len(unpacked_out) % 7))
        if(len(unpacked_out) % 7):
            shortened_out = unpacked_out[:-(len(unpacked_out) % 7)]
        else:
            shortened_out = unpacked_out
        print('shortened:', repr(shortened_out[:7]))
        reshaped_out = shortened_out.reshape(-1, 7)
        print('reshaped: ', repr(reshaped_out[:7]))
        for bits in reshaped_out:
            s = bits.dot(Hamming.H.T)
            s %= 2
            e = Hamming.S[4 * int(s[2]) + 2 * int(s[1]) + int(s[0])]
            c = np.logical_xor(e, bits)
            output.append([bool(x) for x in c[3:].tolist()])
        print('out: ', repr(output[:4]))
        np_out = np.packbits(output)
        return np_out
