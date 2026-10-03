from flask import Flask, request, jsonify

app = Flask(__calculadora__)

@app.route('/sumar', methods=['GET'])
def sumar():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    return jsonify({"resultado": a + b})

@app.route('/restar', methods=['GET'])
def restar():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    return jsonify({"resultado": a - b})

@app.route('/multiplicar', methods=['GET'])
def multiplicar():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    return jsonify({"resultado": a * b})

@app.route('/dividir', methods=['GET'])
def dividir():
    a = float(request.args.get('a'))
    b = float(request.args.get('b'))
    if b == 0:
        return jsonify({"error": "División entre cero no permitida"}), 400
    return jsonify({"resultado": a / b})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
