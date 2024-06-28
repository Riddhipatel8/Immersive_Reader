from flask import Flask, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get Azure credentials from environment variables
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_RESOURCE = 'https://cognitiveservices.azure.com/.default'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_token', methods=['GET'])
def get_token():
    url = f'https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': AZURE_CLIENT_ID,
        'client_secret': AZURE_CLIENT_SECRET,
        'scope': AZURE_RESOURCE,
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        return jsonify({'access_token': token})
    else:
        return jsonify({'error': 'Unable to fetch token'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
