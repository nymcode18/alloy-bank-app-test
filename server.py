from flask import Flask, request, jsonify, send_from_directory
import requests
import base64
import os
import logging
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

ALLOY_TOKEN  = os.getenv('ALLOY_TOKEN')
ALLOY_SECRET = os.getenv('ALLOY_SECRET')

if not ALLOY_TOKEN or not ALLOY_SECRET:
    raise ValueError("Missing ALLOY_TOKEN or ALLOY_SECRET in .env file")

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
        response.raise_for_status()
        result = response.json()
        outcome = result.get('summary', {}).get('outcome', 'Unknown')
        app.logger.info(f"Evaluation outcome: {outcome}")
        return jsonify({'outcome': outcome})
    except requests.exceptions.HTTPError as e:
        app.logger.error(f"Alloy API error: {e.response.status_code} - {e.response.text}")
        return jsonify({'outcome': 'Error', 'detail': 'API request failed'}), 502
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'outcome': 'Error', 'detail': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)