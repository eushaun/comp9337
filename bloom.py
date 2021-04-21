import math
from bitarray import bitarray
import re
import mmh3
 
class BloomFilter(object):

    def __init__(self, filter_size):
 
        self.filter_size = filter_size

        # bit array
        self.bit_array = bitarray(self.filter_size)
 
        # initialize all bits as 0
        self.bit_array.setall(0)

    def __str__(self):
        return self.bit_array.to01()

    # add item into filter
    def add(self, key):
        for i in self.hashes(key):
            self.bit_array[i] = 1
 
    # code snippets taken from
    # https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
    # compute value of string using 3 different hash functions
    def hashes(self, key):
        seed = [42, 69, 99]
        for i in seed:
            index = mmh3.hash(str(key), i) % self.filter_size
            yield index

    # merge a list of bloom filters into a single filter
    def merge(self, filters_list):
        self.bit_array.setall(0)
        for dbf in filters_list:
            self.bit_array |= dbf.bit_array

    def restart(self):
        self.bit_array.setall(0)

# main function
if __name__ == "__main__":
    bloomf1 = BloomFilter(100)
    bloomf2 = BloomFilter(100)
    bloomf3 = BloomFilter(100)

    # words to be added
    word_present = [67488643248729147932]

    # word not added
    word_absent = ['bluff','cheater','hate','war','humanity',
    'racism','hurt','nuke','gloomy','facebook',
                   'geeksforgeeks','twitter']
 
    for item in word_present:
        bloomf1.add(item)

    for item in word_absent:
        bloomf2.add(item)

    print(bloomf1.bit_array)
    print(str(bloomf2))

    #bloomf3.merge([bloomf1, bloomf2])
