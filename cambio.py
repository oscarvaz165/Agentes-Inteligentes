from flask import Flask, request, jsonify

app = Flask(__name__)


# Definición de las operaciones REST

@app.route('/api/v1/calculadora/sumar', methods=['GET'])
def sumar():
    # Obtener parámetros de consulta (query parameters)
    try:
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
        resultado = num1 + num2
        return jsonify({"operacion": "suma", "resultado": resultado}), 200
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros 'num1' y 'num2' requeridos y deben ser números."}), 400


@app.route('/api/v1/calculadora/restar', methods=['GET'])
def restar():
    try:
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
        resultado = num1 - num2
        return jsonify({"operacion": "resta", "resultado": resultado}), 200
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros 'num1' y 'num2' requeridos y deben ser números."}), 400


@app.route('/api/v1/calculadora/multiplicar/<float:num1>/<float:num2>', methods=['GET'])
def multiplicar(num1, num2):
    # Uso de segmentos de ruta (path segments)
    resultado = num1 * num2
    return jsonify({"operacion": "multiplicacion", "resultado": resultado}), 200


@app.route('/api/v1/calculadora/dividir', methods=['GET'])
def dividir():
    try:
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))

        if num2 == 0:
            return jsonify({"error": "División por cero no permitida."}), 400

        resultado = num1 / num2
        return jsonify({"operacion": "division", "resultado": resultado}), 200
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros 'num1' y 'num2' requeridos y deben ser números."}), 400


if __name__ == '__main__':
    # Ejecutar la aplicación: http://127.0.0.1:5000
    # Ejemplo de uso: http://127.0.0.1:5000/api/v1/calculadora/sumar?num1=10&num2=5
    app.run(debug=True)