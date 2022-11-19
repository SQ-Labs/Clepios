import numpy as np
from Pyfhel import Pyfhel
HE = Pyfhel()           # Creating empty Pyfhel object
HE.contextGen(scheme='bfv', n=2**14, t_bits=40)  # Generate context for 'bfv'/'ckks' scheme
                        # The n defines the number of plaintext slots.
                        #  There are many configurable parameters on this step
                        #  More info in Demo_2, Demo_3, and Pyfhel.contextGen()
HE.keyGen()             # Key Generation: generates a pair of public/secret keys
integer1 = np.array([64], dtype=np.int64)
integer2 = np.array([-2], dtype=np.int64)
ctxt1 = HE.encryptInt(integer1) # Encryption makes use of the public key
ctxt2 = HE.encryptInt(integer2) # For integers, encryptInt function is used.
ctxtSum = ctxt1 + ctxt2         # `ctxt1 += ctxt2` for inplace operation
ctxtSub = ctxt1 - ctxt2         # `ctxt1 -= ctxt2` for inplace operation
ctxtMul = ctxt1 * ctxt2         # `ctxt1 *= ctxt2` for inplace operation
ctxtDiv = ctxt1 / 2
resSum = HE.decryptInt(ctxtSum) # Decryption must use the corresponding function
                                #  decryptInt.
resSub = HE.decryptInt(ctxtSub)
resMul = HE.decryptInt(ctxtMul)
resDiv = HE.decryptInt(ctxtDiv)
print("#. Decrypting result:")
print("     addition:       decrypt(ctxt1 + ctxt2) =  ", resSum)
print("     substraction:   decrypt(ctxt1 - ctxt2) =  ", resSub)
print("     multiplication: decrypt(ctxt1 + ctxt2) =  ", resMul)
print("     division:       decrypt(ctxt1 / ctxt2) =  ", resDiv)
