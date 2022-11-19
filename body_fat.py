import numpy as np
from Pyfhel import Pyfhel, PyCtxt

HE = Pyfhel()           # Creating empty Pyfhel object
ckks_params = {
    'scheme': 'CKKS',   # can also be 'ckks'
    'n': 2**14,         # Polynomial modulus degree. For CKKS, n/2 values can be
                        #  encoded in a single ciphertext. 
                        #  Typ. 2^D for D in [10, 16]
    'scale': 2**30,     # All the encodings will use it for float->fixed point
                        #  conversion: x_fix = round(x_float * scale)
                        #  You can use this as default scale or use a different
                        #  scale on each operation (set in HE.encryptFrac)
    'qi_sizes': [60, 30, 30, 30, 30, 60] # Number of bits of each prime in the chain. 
                        # Intermediate values should be  close to log2(scale)
                        # for each operation, to have small rounding errors.
}

HE.contextGen(**ckks_params)  # Generate context for bfv scheme
HE.keyGen()             # Key Generation: generates a pair of public/secret keys
HE.rotateKeyGen()

bmi = 80/(1.75**2)
print(bmi)
bmi = HE.encryptFrac(np.array([bmi], dtype=np.float64))
age = HE.encryptFrac(np.array([30], dtype=np.float64))

# BFP = 1.20 × BMI + 0.23 × Age - 16.2 
bfp = 1.20 * bmi + 0.23 * age - 16.2

bfpDec = HE.decryptFrac(bfp)
print("bfp = {}".format(bfpDec))

# _r = lambda x: np.round(x, decimals=3)
# print("x = {}".format(_r(HE.decryptFrac(bfp))))