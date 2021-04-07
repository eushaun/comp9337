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

    def __str__(self):
        return self.bit_array.to01()

    # add item into filter
    def add(self, key):
        for i in self.hashes(key):
            self.bit_array[i] = 1

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

    print(str(bloomf1))
    print(str(bloomf2))

    bloomf3.merge([bloomf1, bloomf2])
    print(str(bloomf3))
