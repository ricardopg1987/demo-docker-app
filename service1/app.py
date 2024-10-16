# service1/app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status')
def status():
    return jsonify({
        'status': 'success',
        'message': '¡Felicitaciones! Has establecido conexión con el Servicio 1'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
