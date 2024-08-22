"""
:Author:        David Stewart
:Contact:       https://www.linkedin.com/in/david-s-stewart/
:Date:          2024-01-01
:Compatibility: Python 3.9
:License:       MIT
"""

from random import Random
from unittest import TestCase
from binary.bitarray import BitArray


class _BitArray(TestCase):

    """Unit tests for BitArray class."""

    # Test construct.

    def test_construct_default(self):
        """Create an empty BitArray."""
        bit_array = BitArray()
        self.assertEqual(str(bit_array), '0b')
        self.assertEqual(bit_array.length, 0)
        self.assertEqual(len(bit_array), 0)

    def test_construct_int(self):
        """Create a BitArray with a specified size."""
        bit_array = BitArray(19)
        self.assertEqual(str(bit_array), '0b0000000000000000000')
        self.assertEqual(bit_array.length, 19)
        self.assertEqual(len(bit_array), 19)

    def test_construct_int_error(self):
        """Create a BitArray with a specified size with an error."""
        try:
            BitArray(-19)
        except Exception:
            pass
        else:
            self.fail()

    def test_construct_str(self):
        """Create a BitArray from a string."""
        bit_array = BitArray('0001011010100110001')
        self.assertEqual(str(bit_array), '0b0001011010100110001')
        self.assertEqual(bit_array.length, 19)
        self.assertEqual(len(bit_array), 19)

    def test_construct_str_error(self):
        """Create a BitArray from a string with an error."""
        try:
            BitArray('000101101010011000x')
        except Exception:
            pass
        else:
            self.fail()

    def test_construct_bytes(self):
        """Create a BitArray from bytes."""
        bit_array = BitArray(b'hello')
        self.assertEqual(str(bit_array),
                         '0b0001011010100110001101100011011011110110')
        self.assertEqual(bit_array.length, 40)
        self.assertEqual(len(bit_array), 40)

    def test_construct_bytearray(self):
        """Create a BitArray from bytearray."""
        bit_array = BitArray(bytearray(b'hello'))
        self.assertEqual(str(bit_array),
                         '0b0001011010100110001101100011011011110110')
        self.assertEqual(bit_array.length, 40)
        self.assertEqual(len(bit_array), 40)

    def test_construct_collection(self):
        """Create a BitArray from a collection."""
        bit_array = BitArray([True, True, False, True, False])
        self.assertEqual(str(bit_array), '0b11010')
        self.assertEqual(bit_array.length, 5)
        self.assertEqual(len(bit_array), 5)

    def test_construct_collection_variant(self):
        """Create a BitArray from a collection."""
        bit_array = BitArray([1, 0, None, '#', ''])
        self.assertEqual(str(bit_array), '0b10010')
        self.assertEqual(bit_array.length, 5)
        self.assertEqual(len(bit_array), 5)

    # Test contains.

    def test_contains_false_false(self):
        """Test contains False where expectation is False."""
        for length in range(20):
            bit_array = BitArray('1' * length)
            self.assertFalse(False in bit_array)

    def test_contains_false_true(self):
        """Test contains False where expectation is True."""
        for length in range(1, 20):
            bit_array = BitArray('0' * length)
            self.assertTrue(False in bit_array)

    def test_contains_false_true_alternating(self):
        """Test contains False where expectation is True with mixed data."""
        bit_array = BitArray()
        for _ in range(10):
            # Add only False values leaving 0's padded. Arrangement covers
            # all transitions
            bit_array.append(False)
            self.assertTrue(False in bit_array)
            bit_array.append(True)
            self.assertTrue(False in bit_array)
            bit_array.append(True)
            self.assertTrue(False in bit_array)

    def test_contains_true_false(self):
        """Test contains True where expectation is False."""
        for length in range(20):
            bit_array = BitArray('0' * length)
            self.assertFalse(True in bit_array)

    def test_contains_true_true(self):
        """Test contains True where expectation is True."""
        for length in range(1, 20):
            bit_array = BitArray('1' * length)
            self.assertTrue(True in bit_array)

    # Test add.

    def test_add(self):
        """Test add functionality using list equivalence."""
        for length_1 in range(10):
            for length_2 in range(10):
                bit_array_1 = BitArray('0' * length_1)
                bit_array_2 = BitArray('1' * length_2)
                bit_array_3 = BitArray('0' * length_1 + '1' * length_2)
                bit_array_4 = bit_array_1 + bit_array_2
                self.assertEqual(bit_array_3, bit_array_4)

    # Test slice.

    def test_slice(self):
        """Test slices."""
        # Loop through range and test against list behaviour.
        bit_array = BitArray('11001100')
        list_array = [v for v in bit_array]
        indexes = [None] + list(range(-10, 10))
        for start in indexes:
            for stop in indexes:
                slice_ = bit_array[start: stop]
                list_slice = list_array[start: stop]
                self.assertEqual([v for v in slice_], list_slice)

    def test_slice_step(self):
        """Test slices with steps."""
        # Loop through range and test against list behaviour.
        bit_array = BitArray('0b11001100110011001100')
        list_array = [v for v in bit_array]
        indexes = [None] + list(range(-20, 20))
        for start in indexes:
            for stop in indexes:
                for step in [1, 2, 3, 5]:
                    slice_ = bit_array[start: stop: step]
                    list_slice = list_array[start: stop: step]
                    self.assertEqual([v for v in slice_], list_slice)

    # Test append.

    def test_append_empty_false(self):
        """Test append False on an empty BitArray."""
        bit_array = BitArray()
        for index in range(19):
            self.assertEqual(str(bit_array), '0b' + '0' * index)
            self.assertEqual(bit_array.length, index)
            self.assertEqual(len(bit_array), index)
            bit_array.append(False)

    def test_append_empty_true(self):
        """Test append True on an empty BitArray."""
        bit_array = BitArray()
        for index in range(19):
            self.assertEqual(str(bit_array), '0b' + '1' * index)
            self.assertEqual(bit_array.length, index)
            self.assertEqual(len(bit_array), index)
            bit_array.append(True)

    def test_append_non_empty_false(self):
        """Test append False on a non empty BitArray."""
        bit_array = BitArray('1101')
        for index in range(19):
            self.assertEqual(str(bit_array), '0b1101' + '0' * index)
            self.assertEqual(bit_array.length, index + 4)
            self.assertEqual(len(bit_array), index + 4)
            bit_array.append(False)

    def test_append_non_empty_true(self):
        """Test append True on a non empty BitArray."""
        bit_array = BitArray('1101')
        for index in range(19):
            self.assertEqual(str(bit_array), '0b1101' + '1' * index)
            self.assertEqual(bit_array.length, index + 4)
            self.assertEqual(len(bit_array), index + 4)
            bit_array.append(True)

    # Test clear and zero.

    def test_clear(self):
        """Test clear on a BitArray."""
        bit_array = BitArray('1101')
        bit_array.clear()
        self.assertEqual(str(bit_array), '0b')
        self.assertEqual(bit_array.length, 0)
        self.assertEqual(len(bit_array), 0)

    def test_zero(self):
        """Test zero on a BitArray."""
        bit_array = BitArray('1101')
        bit_array.zero()
        self.assertEqual(str(bit_array), '0b0000')
        self.assertEqual(bit_array.length, 4)
        self.assertEqual(len(bit_array), 4)

    # Test copy.

    def test_copy_empty(self):
        """Test clear on an empty BitArray."""
        bit_array = BitArray()
        copy_array = bit_array.copy()
        self.assertEqual(bit_array, bit_array)
        self.assertEqual(bit_array, copy_array)

    def test_copy_non_empty(self):
        """Test clear on a non empty BitArray."""
        bit_array = BitArray('11101010')
        copy_array = bit_array.copy()
        self.assertEqual(bit_array, bit_array)
        self.assertEqual(bit_array, copy_array)

    # Test count.

    def test_count_empty(self):
        """Test count on an empty BitArray."""
        bit_array = BitArray()
        self.assertEqual(bit_array.count(False), 0)
        self.assertEqual(bit_array.count(True), 0)

    def test_count_non_empty(self):
        """Test count on a non empty BitArray."""
        bit_array = BitArray('11101010110')
        self.assertEqual(bit_array.count(False), 4)
        self.assertEqual(bit_array.count(True), 7)

    # Test extend.

    def test_extend_str(self):
        """Extend a BitArray with a string."""
        bit_array = BitArray('0001011010100110001')
        bit_array.extend('1100')
        self.assertEqual(str(bit_array), '0b00010110101001100011100')
        self.assertEqual(bit_array.length, 23)
        self.assertEqual(len(bit_array), 23)

    def test_extend_str_error(self):
        """Extend a BitArray with a string with an error."""
        bit_array = BitArray('0001011010100110001')
        try:
            bit_array.extend('110x')
        except Exception:
            pass
        else:
            self.fail()

    def test_extend_bytes(self):
        """Extend a BitArray with bytes."""
        bit_array = BitArray('0001011010100110001')
        bit_array.extend(b'x')
        self.assertEqual(str(bit_array),
                         '0b000101101010011000100011110')
        self.assertEqual(bit_array.length, 27)
        self.assertEqual(len(bit_array), 27)

    def test_extend_bytearray(self):
        """Extend a BitArray with bytearray."""
        bit_array = BitArray('0b0001011010100110001')
        bit_array.extend(bytearray(b'x'))
        self.assertEqual(str(bit_array),
                         '0b000101101010011000100011110')
        self.assertEqual(bit_array.length, 27)
        self.assertEqual(len(bit_array), 27)

    def test_extend_collection(self):
        """Extend a BitArray with a collection."""
        bit_array = BitArray('0001011010100110001')
        bit_array.extend([True, True, False, False])
        self.assertEqual(str(bit_array), '0b00010110101001100011100')
        self.assertEqual(bit_array.length, 23)
        self.assertEqual(len(bit_array), 23)

    def test_extend_collection_variant(self):
        """Extend a BitArray with a collection."""
        bit_array = BitArray('0001011010100110001')
        bit_array.extend([1, 'w', 0, ''])
        self.assertEqual(str(bit_array), '0b00010110101001100011100')
        self.assertEqual(bit_array.length, 23)
        self.assertEqual(len(bit_array), 23)

    # Test index.

    def test_index_empty(self):
        """Test index with empty array."""
        bit_array = BitArray()
        for value in [False, True]:
            try:
                bit_array.index(value)
            except Exception:
                pass
            else:
                self.fail()

    def test_index_all_false(self):
        """Test index with all False array."""
        bit_array = BitArray(10)
        self.assertEqual(bit_array.index(False), 0)
        try:
            bit_array.index(True)
        except Exception:
            pass
        else:
            self.fail()

    def test_index_all_true(self):
        """Test index with all True array."""
        bit_array = BitArray('1111111111')
        self.assertEqual(bit_array.index(True), 0)
        try:
            bit_array.index(False)
        except Exception:
            pass
        else:
            self.fail()

    def test_index_mix(self):
        """Test index with mixed array."""
        bit_array = BitArray('11001100')
        self.assertEqual(bit_array.index(False), 2)
        self.assertEqual(bit_array.index(True), 0)

    def test_index_slice(self):
        """Test index with slices."""
        # Loop through range and test against list behaviour.
        bit_array = BitArray('11001100')
        list_array = [v for v in bit_array]
        indexes = [None] + list(range(-10, 10))
        for value in [True, False]:
            for start in indexes:
                for stop in indexes:
                    try:
                        index = bit_array.index(value, start, stop)
                        list_index = list_array.index(value, start, stop)
                        self.assertEqual(index, list_index)
                    except Exception:
                        try:
                            list_index = list_array.index(value, start, stop)
                        except Exception:
                            pass
                        else:
                            self.fail()

    # Test index_of

    def test_index_of_empty(self):
        """Test index_of with empty array."""
        bit_array = BitArray()
        for value in [False, True]:
            try:
                bit_array.index_of(value, 0)
            except Exception:
                pass
            else:
                self.fail()
            try:
                bit_array.index_of(value, 10)
            except Exception:
                pass
            else:
                self.fail()

    def test_index_of_all_false(self):
        """Test index_of with all False array."""
        bit_array = BitArray(20)
        self.assertEqual(bit_array.index_of(False, 0), 0)
        self.assertEqual(bit_array.index_of(False, 10), 10)
        try:
            bit_array.index_of(True, 0)
        except Exception:
            pass
        else:
            self.fail()
        try:
            bit_array.index_of(True, 10)
        except Exception:
            pass
        else:
            self.fail()

    def test_index_of_all_true(self):
        """Test index_of with all True array."""
        bit_array = BitArray('11111111111111111111')
        self.assertEqual(bit_array.index_of(True, 0), 0)
        self.assertEqual(bit_array.index_of(True, 10), 10)
        try:
            bit_array.index_of(False, 0)
        except Exception:
            pass
        else:
            self.fail()
        try:
            bit_array.index_of(False, 10)
        except Exception:
            pass
        else:
            self.fail()

    def test_index_of_mix(self):
        """Test index_of with a mixed array."""
        bit_array = BitArray('11001100110011001100110011001100')
        self.assertEqual(bit_array.index_of(False, 0), 2)
        self.assertEqual(bit_array.index_of(False, 10), 22)
        self.assertEqual(bit_array.index_of(True, 0), 0)
        self.assertEqual(bit_array.index_of(True, 10), 20)
        try:
            bit_array.index_of(False, 30)
        except Exception:
            pass
        else:
            self.fail()
        try:
            bit_array.index_of(True, 30)
        except Exception:
            pass
        else:
            self.fail()

    # Test random_index

    def test_random_index_empty(self):
        """Test random_index with empty array."""
        bit_array = BitArray()
        random = Random()
        for value in [False, True]:
            try:
                bit_array.random_index(value, random)
            except Exception:
                pass
            else:
                self.fail()

    def test_random_index_all_false(self):
        """Test random_index with all False array."""
        bit_array = BitArray(20)
        random = Random()
        self.assertGreaterEqual(bit_array.random_index(False, random), 0)
        try:
            bit_array.random_index(True, random)
        except Exception:
            pass
        else:
            self.fail()

    def test_random_index_all_true(self):
        """Test random_index with all False array."""
        bit_array = BitArray('1111111111111111111111111111111111111111111')
        random = Random()
        self.assertGreaterEqual(bit_array.random_index(True, random), 0)
        try:
            bit_array.random_index(False, random)
        except Exception:
            pass
        else:
            self.fail()

    def test_random_index_mix(self):
        """Test random_index with a mixed array."""
        bit_array = BitArray('11001100110011001100110011001100')
        random = Random()
        self.assertGreaterEqual(bit_array.random_index(False, random), 0)
        self.assertGreaterEqual(bit_array.random_index(True, random), 0)

    # Test insert.

    def test_insert(self):
        """Test insert."""
        bit_array = BitArray('1010011001')
        list_array = [v for v in bit_array]
        for index in (-3, 0, 1, 5, 12, 20):
            bit_array.insert(index, True)
            list_array.insert(index, True)
            self.assertEqual([v for v in bit_array], list_array)

    # Test pop.

    def test_pop_end(self):
        """Test pop at default index."""
        bit_array = BitArray('1010011001')
        list_array = [v for v in bit_array]
        while bit_array:
            self.assertEqual(bit_array.pop(), list_array.pop())
            bit_array.pop()
            list_array.pop()
            self.assertEqual([v for v in bit_array], list_array)

    def test_pop_zero(self):
        """Test pop at index 0."""
        bit_array = BitArray('1010011001')
        list_array = [v for v in bit_array]
        while bit_array:
            self.assertEqual(bit_array.pop(0), list_array.pop(0))
            self.assertEqual([v for v in bit_array], list_array)

    def test_pop_mid(self):
        """Test pop at index 0."""
        bit_array = BitArray('1010011001')
        list_array = [v for v in bit_array]
        while bit_array:
            try:
                bit_value = bit_array.pop(5)
            except Exception:
                try:
                    list_value = list_array.pop(5)
                except Exception:
                    pass
                else:
                    self.fail()
                break
            else:
                list_value = list_array.pop(5)
                self.assertEqual(bit_value, list_value)
                self.assertEqual([v for v in bit_array], list_array)

    # Test reverse.

    def test_reverse(self):
        """Test reverse for a variety of sizes."""
        for initial in ('',
                        '1',
                        '10',
                        '100',
                        '11111110',
                        '101010101010',
                        '110010110100101101010010111100'):
            bit_array = BitArray(initial)
            list_array = [v for v in bit_array]
            bit_array.reverse()
            list_array.reverse()
            self.assertEqual([v for v in bit_array], list_array)

    # Test invert.

    def test_invert(self):
        """Test invert for a variety of configurations."""
        # Note that invert does not have a list equivalent.
        for initial in ('',
                        '1',
                        '10',
                        '100',
                        '11111110',
                        '101010101010',
                        '110010110100101101010010111100'):
            bit_array = BitArray(initial)
            inverted = bit_array.copy()
            inverted.invert()
            for a, b in zip(bit_array, inverted):
                self.assertNotEqual(a, b)
