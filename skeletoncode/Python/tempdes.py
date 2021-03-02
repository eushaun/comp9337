
from Crypto.Cipher import DES
from Crypto import Random
cbc_key = "\x40\xfe\xdf\x38\x6d\xa1\x3d\x57"
print '='*100                    
print 'Key used: ', [x for x in cbc_key]

iv = Random.get_random_bytes(8)
print "IV used: ",[x for x in iv]
print '='*100

des1 = DES.new(cbc_key, DES.MODE_CBC, iv)
des2 = DES.new(cbc_key, DES.MODE_CBC, iv)

plain_text = "abcdefgh"
print "Plaintext is: ", plain_text

cipher_text = des1.encrypt(plain_text)
print"Ciphertext is: ",cipher_text
msg=des2.decrypt(cipher_text)
print "Original Message", msg
print '='*100

