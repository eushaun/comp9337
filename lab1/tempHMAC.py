#Following code reads its source file and computes an HMAC signature for it:
import hmac
import sys
import time

secret_key = b'secret-shared-key-goes-here'

digest_maker = hmac.new(secret_key) # in your code replace key
f = open(sys.argv[1], 'rb')
try:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)
finally:
    f.close()

start_time = time.time()
digest = digest_maker.hexdigest()
hmac_time = time.time() - start_time
print("HMAC signature generation time is: ", hmac_time)

# print('='*100) 
# print("HMAC digest generated for \"lorem.txt\" file is:", digest)
# print('='*100) 
