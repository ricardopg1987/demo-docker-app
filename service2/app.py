# service2/app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status')
def status():
    return jsonify({
        'status': 'success',
        'message': '¡Excelente! Has establecido conexión con el Servicio 2'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)