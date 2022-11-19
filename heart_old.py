import numpy as np
from Pyfhel import Pyfhel
HE = Pyfhel()
bfv_params = {
    'scheme': 'BFV',
    'n': 2**13,
    't': 65537,
    't_bits': 20,
    'sec': 128,
}
HE.contextGen(**bfv_params)
HE.keyGen()
HE.rotateKeyGen()
HE.relinKeyGen()

a = np.array([60], dtype=np.int64)
sys = np.array([120], dtype=np.int64)
dia = np.array([70], dtype=np.int64)
chol = np.array([200], dtype=np.int64)
ht = np.array([175], dtype=np.int64)
wt = np.array([70], dtype=np.int64)

ctx_a = HE.encryptInt(a)
ctx_sys = HE.encryptInt(sys)
ctx_dia = HE.encryptInt(dia)
ctx_chol = HE.encryptInt(chol)
ctx_ht = HE.encryptInt(ht)
ctx_wt = HE.encryptInt(wt)

z = 72 * ctx_a + 13 * ctx_sys - 29 * ctx_dia + 8 * ctx_chol - 53 * ctx_ht + 21 * ctx_wt

fz = -17 * z**7 + 168 * z**5 - 1680 * z**3 + 20160 * z + 403200

print(HE.decryptInt(z))