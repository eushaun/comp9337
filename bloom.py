import math
from bitarray import bitarray
import mmh3

 
class BloomFilter(object):

    # constructor
    def __init__(self, filter_size):
 
        self.filter_size = filter_size

        # Bit array of given size
        self.bit_array = bitarray(self.filter_size)
 
        # initialize all bits as 0
        self.bit_array.setall(0)
 
    # add item into filter
    def add(self, item):
        
        digest1 = mmh3.hash(item) % self.filter_size

        digest2 = mmh3.hash128(item) % self.filter_size

        # set the bit True in bit_array
        self.bit_array[digest1] = True
        self.bit_array[digest2] = True
 
    # check for existence of item in filter
    def check(self, item):

        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                return False

        return True

# main function
if __name__ == "__main__":
    bloomf = BloomFilter(100)

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
        bloomf.add(item)
    print(bloomf.bit_array)
