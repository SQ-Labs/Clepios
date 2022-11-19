import copy
from curses import termattrs
from http.client import REQUEST_URI_TOO_LONG
from typing import Sequence
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

age = HE.encryptFrac(np.array([10.0], dtype=np.float64))
sys = HE.encryptFrac(np.array([80.0], dtype=np.float64))
dia = HE.encryptFrac(np.array([100.0], dtype=np.float64))
chol = HE.encryptFrac(np.array([400], dtype=np.float64))
height = HE.encryptFrac(np.array([1.75], dtype=np.float64))
weight = HE.encryptFrac(np.array([80.0], dtype=np.float64))

x = 0.072 * age + 0.013 * sys - 0.029 * dia - 0.008 * chol - 0.053 * height + 0.021 * weight 
HE.rescale_to_next(x)

def power(x, n):
    if n == 1:
        return x
    elif n % 2 == 0:
        return power(x * x, n // 2)
    else:
        return x * power(x * x, n // 2)

def taylor_series(x):
    r = 1/4 * x - 1/48 * power(x, 3) #+ 1/480 * power(x, 5) #- 17/80640 * power(x, 7)
    # r + 1/2
    return r + 1/2

px = taylor_series(x)

decX = HE.decryptFrac(x)
decPx = HE.decryptFrac(px)

_r = lambda x: np.round(x, decimals=3)
print("x = {}".format(_r(decX)))    
print("px = {}".format(_r(decPx)))