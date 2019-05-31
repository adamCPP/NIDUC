from unittest import TestCase
import numpy as np

from application.hamming.hamming import Hamming


class TestHamming(TestCase):

    def setUp(self):
        self.hamming = Hamming()
        self.single_byte = np.empty(1, dtype='uint8')
        self.single_byte[0] = 117  # binary: 01110101

    def test_encode(self):
        result = self.hamming.encode(self.single_byte).tolist()
        expected_result = [[0., 0., 1., 0., 1., 1., 1.], [1., 1., 0., 0., 1., 0., 1.]]
        self.assertEqual(result, expected_result)
