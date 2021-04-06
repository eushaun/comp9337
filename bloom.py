import math
from bitarray import bitarray
import hashlib

 
class BloomFilter(object):

    # constructor
    def __init__(self, filter_size):
 
        self.filter_size = filter_size

        # Bit array of given size
        self.bit_array = bitarray(self.filter_size)
 
        # initialize all bits as 0
        self.bit_array.setall(0)

    # add item into filter
    def add(self, key):
        for i in self.hashes(key):
            self.bit_array[i] = 1
 
    # check for existence of item in filter
    def check(self, item):

        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                return False

        return True

    def hashes(self, key):
        h = hashlib.new('md5')
        h.update(str(key).encode())
        x = int(h.hexdigest(), 16)
        for _unused in range(2):
            if x < 1024 * self.filter_size:
                h.update(b'x')
                x = int(h.hexdigest(), 16)
            x, y = divmod(x, self.filter_size)
            yield y

    def merge(self, *args):
        self.bit_array.setall(0)
        for arg in args:
            self.bit_array |= arg.bit_array


# main function
if __name__ == "__main__":
    bloomf1 = BloomFilter(100)
    bloomf2 = BloomFilter(100)
    bloomf3 = BloomFilter(100)

    # words to be added
    word_present = ['abound','abounds','abundance','abundant','accessable',
        'bloom','blossom','bolster','bonny','bonus','bonuses',
        'coherent','cohesive','colorful','comely','comfort',
        'gems','generosity','generous','generously','genial']

    # word not added
    word_absent = ['bluff','cheater','hate','war','humanity',
    'racism','hurt','nuke','gloomy','facebook',
                   'geeksforgeeks','twitter']
 
    for item in word_present:
        bloomf1.add(item)

    for item in word_absent:
        bloomf2.add(item)

    print(bloomf1.bit_array.to01())
    print(bloomf2.bit_array.to01())

    bloomf3.merge(bloomf1, bloomf2)
    print(bloomf3.bit_array.to01())
