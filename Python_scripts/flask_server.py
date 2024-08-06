from flask import Flask, jsonify, request

app = Flask(__name__)

#première route de test
@app.route('/')
def index():
    return "Hello World"

#Lance le serveur sur le port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)
