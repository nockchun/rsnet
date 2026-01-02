import sys
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return f'Flask and Docker Test {sys.version_info}'

@app.route('/hello', methods=['GET'])
def hello_world():
	return jsonify({'message': 'Hello World'})

@app.route('/test', methods=['GET'])
def test():
	return jsonify({'test': 'test'})

if __name__ == "__main__":
	app.run(debug=False, host="0.0.0.0")