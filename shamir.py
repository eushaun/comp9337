# pip install pycryptodome

from Crypto.Protocol.SecretSharing import Shamir
from binascii import hexlify, unhexlify

# generate 6 shares
def generate_shares(secret):
    return Shamir.split(3, 6, secret)

# reconstruct id
def reconstruct_secret(shares):
    return Shamir.combine(shares)


# FIELD_SIZE = 100000

# # calculate value of poly at x
# def calculate_poly(x, coefficients):
#     y = 0
#     for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
#         y += x ** coefficient_index * coefficient_value
#     return y
 
#  # generate 6 shares
# def generate_shares(secret):
# 	m = 3
# 	n = 6

# 	# generate polynomials
# 	coefficients = [random.randrange(0, FIELD_SIZE) for _ in range(m - 1)]
# 	coefficients.append(secret)

# 	# get 3 random points of polynomials
# 	shares = []
# 	for i in range(1, n+1):
# 		x = random.randrange(1, FIELD_SIZE)
# 		shares.append((x, calculate_poly(x, coefficients)))

# 	return shares

# # reconstruct id
# def reconstruct_secret(shares):
#     sums = 0
#     prod_arr = []
 
#     for j, share_j in enumerate(shares):
#         xj, yj = share_j
#         prod = Decimal(1)

#         prod *= yj
        
#         for i, share_i in enumerate(shares):
#             xi, _ = share_i
#             if i != j:
#                 prod *= Decimal(Decimal(xi)/(xi-xj))
 
#         sums += Decimal(prod)
#         print(sums)
#     return int(round(Decimal(sums), 0))
