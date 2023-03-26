import flask
from IPython import get_ipython
import json
from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    requestData = request.json
    response = requests.post('https://f49e-35-197-58-189.ngrok.io/ask', json=requestData)
    print(response.json())
    responseData = response.json()
    return responseData


if __name__ == '__main__':
	app.run()