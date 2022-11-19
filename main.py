from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import numpy as np
import base64
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

app = Flask(__name__)

# hello world
@app.route('/cypher')
def cypher():
    age = request.args.get('age', 0)
    sys = request.args.get('sys', 0)
    dia = request.args.get('dia', 0)
    chol = request.args.get('chol', 0)
    height = request.args.get('height', 0)
    weight = request.args.get('weight', 0)

    age = HE.encryptFrac(np.array([age], dtype=np.float64))
    sys = HE.encryptFrac(np.array([sys], dtype=np.float64))
    dia = HE.encryptFrac(np.array([dia], dtype=np.float64))
    chol = HE.encryptFrac(np.array([chol], dtype=np.float64))
    height = HE.encryptFrac(np.array([height], dtype=np.float64))
    weight = HE.encryptFrac(np.array([weight], dtype=np.float64))

    age_bytes = age.to_bytes()
    age_b64 = base64.b64encode(age_bytes).decode('utf-8')

    sys_bytes = sys.to_bytes()
    sys_b64 = base64.b64encode(sys_bytes).decode('utf-8')

    dia_bytes = dia.to_bytes()
    dia_b64 = base64.b64encode(dia_bytes).decode('utf-8')

    chol_bytes = chol.to_bytes()
    chol_b64 = base64.b64encode(chol_bytes).decode('utf-8')

    height_bytes = height.to_bytes()
    height_b64 = base64.b64encode(height_bytes).decode('utf-8')

    weight_bytes = weight.to_bytes()
    weight_b64 = base64.b64encode(weight_bytes).decode('utf-8')

    return jsonify({
        'age': age_b64,
        'sys': sys_b64,
        'dia': dia_b64,
        'chol': chol_b64,
        'height': height_b64,
        'weight': weight_b64
    })

@app.route('/compute', methods=['POST'])
def compute():
    # parse body
    body = request.get_json()
    age = body['age']
    sys = body['sys']
    dia = body['dia']
    chol = body['chol']
    height = body['height']
    weight = body['weight']


    age_bytes = base64.b64decode(age)
    age = PyCtxt(pyfhel=HE)
    age.from_bytes(age_bytes)

    sys_bytes = base64.b64decode(sys)
    sys = PyCtxt(pyfhel=HE)
    sys.from_bytes(sys_bytes)

    dia_bytes = base64.b64decode(dia)
    dia = PyCtxt(pyfhel=HE)
    dia.from_bytes(dia_bytes)

    chol_bytes = base64.b64decode(chol)
    chol = PyCtxt(pyfhel=HE)
    chol.from_bytes(chol_bytes)

    height_bytes = base64.b64decode(height)
    height = PyCtxt(pyfhel=HE)
    height.from_bytes(height_bytes)

    weight_bytes = base64.b64decode(weight)
    weight = PyCtxt(pyfhel=HE)
    weight.from_bytes(weight_bytes)

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
        return r + 1/2

    px = taylor_series(x)

    px_bytes = px.to_bytes()
    px_b64 = base64.b64encode(px_bytes).decode('utf-8')

    return jsonify({
        'result': px_b64
    })


@app.route('/decypher_result', methods=['POST'])
def decypher_result():
    body = request.get_json()
    result = body['result']

    result_bytes = base64.b64decode(result)
    result = PyCtxt(pyfhel=HE)
    result.from_bytes(result_bytes)

    result = HE.decryptFrac(result)

    return jsonify({
        'result': result[0]
    })

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
