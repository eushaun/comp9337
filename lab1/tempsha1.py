import hashlib
import sys
import time
  
# Open file
try:
    file_name = sys.argv[1]
    f = open(file_name,'r')
    plain_text = f.read()
except:
    sys.exit() 

start_time = time.time()
result = hashlib.sha1(plain_text.encode())
digest = result.hexdigest()
hash_time = time.time() - start_time 
print("Hash generation time is: ", hash_time)

# printing the equivalent hexadecimal value. 
# print("The hexadecimal equivalent of SHA1 digest is : ") 
# print(result.hexdigest())
# print('='*100) 
