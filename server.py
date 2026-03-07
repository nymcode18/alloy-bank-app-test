from flask import Flask, request, jsonify, send_from_directory
import requests
import base64
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

app = Flask(__name__)

ALLOY_TOKEN  = os.getenv('ALLOY_TOKEN')
ALLOY_SECRET = os.getenv('ALLOY_SECRET')

# Encode credentials for Basic Auth
credentials = base64.b64encode(
    f'{ALLOY_TOKEN}:{ALLOY_SECRET}'.encode()
).decode()

# Serve the HTML form
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Handle form submission
@app.route('/apply', methods=['POST'])
def apply():
    form_data = request.json
    try:
        response = requests.post(
            'https://sandbox.alloy.co/v1/evaluations/',
            headers={
                'Authorization': f'Basic {credentials}',
                'Content-Type': 'application/json'
            },
            json=form_data
        )
        result = response.json()
        outcome = result.get('summary', {}).get('outcome', 'Unknown')
        return jsonify({'outcome': outcome})
    except Exception as e:
        return jsonify({'outcome': 'Error'})

if __name__ == '__main__':
    app.run(port=3000, debug=True)