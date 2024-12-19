import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
KEY = os.getenv('FREE_CURRENCY_API_KEY')
BASE_URL = 'https://api.freecurrencyapi.com/v1'

def fetch_supported_currencies():
    """Fetch supported currencies from the API."""
    if not KEY:
        print("Error: API Key is missing.")
        return {}
    
    try:
        url = f"{BASE_URL}/currencies"
        response = requests.get(url, params={'apikey': KEY}, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'data' in data:
            return {code: details['name'] for code, details in data['data'].items()}
        return {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching currencies: {e}")
        return {}

@app.route('/')
def index():
    currencies = fetch_supported_currencies()
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided.'}), 400

    amount = data.get('amount')
    from_currency = data.get('from')
    to_currency = data.get('to')

    # Basic input validation
    if not amount:
        return jsonify({'error': 'Please enter a valid amount.'}), 400
    
    if not from_currency or not to_currency:
        return jsonify({'error': 'From and To currencies are required.'}), 400

    try:
        amount = float(amount)
        if amount < 0:
            return jsonify({'error': 'Amount cannot be negative.'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid amount value.'}), 400

    try:
        url = f'{BASE_URL}/latest'
        params = {
            'apikey': KEY,
            'base_currency': from_currency,
            'currencies': to_currency
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        # Handle API errors specifically
        if response.status_code != 200:
            return jsonify({'error': 'External API error. Please try again later.'}), response.status_code

        data = response.json()

        if 'data' in data and to_currency in data['data']:
            rate = data['data'][to_currency]
            converted_amount = round(amount * rate, 2)
            return jsonify({'converted_amount': converted_amount})
        else:
            return jsonify({'error': 'Target currency not supported or not found.'}), 400

    except requests.exceptions.Timeout:
        return jsonify({'error': 'API request timed out.'}), 504
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Failed to connect to the currency service.'}), 503
    except Exception:
        # Avoid leaking internal details with a generic error
        return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == "__main__":
    # Use debug mode only if set in .env
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
