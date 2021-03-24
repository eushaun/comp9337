import random
from math import ceil
from decimal import Decimal
 
FIELD_SIZE = 100000
 
# Reconstruct secret
def reconstruct_secret(shares):
    sums = 0
    prod_arr = []
 
    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        # f(x_n)
        prod *= yj
 
 		# * (x - x_n) / (x_n - x_n-1)
        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))
 
        sums += Decimal(prod)
 
    return int(round(Decimal(sums), 0))
 
# calculate value of poly at x
def calculate_poly(x, coefficients):
    y = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        y += x ** coefficient_index * coefficient_value
    return y
 
 
 # generate polynomial of power m
def generate_polynomial(m, secret):
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(m - 1)]
    coeff.append(secret)
    return coeff
 
 # generate 6 shares
def generate_shares(secret):
	m = 3
	n = 6

	# generate polynomials
	coefficients = generate_polynomial(m, secret)

	# get 3 random points of polynomials
	shares = []
	for i in range(1, n+1):
		x = random.randrange(1, FIELD_SIZE)
		shares.append((x, calculate_poly(x, coefficients)))

	return shares

# (3,5) sharing scheme
secret = 99284122485312345921
print(f'Original Secret: {secret}')

# Phase I: Generation of shares
shares = generate_shares(secret)
print(f'Shares: {", ".join(str(share) for share in shares)}')

# Phase II: Secret Reconstruction
# Get 3 random shares
pool = random.sample(shares, 3)
print(f'Combining shares: {", ".join(str(share) for share in pool)}')
print(f'Reconstructed secret: {reconstruct_secret(pool)}')
