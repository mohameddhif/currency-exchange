from flask import Flask, render_template, request, jsonify
import json
import urllib.request

app = Flask(__name__)

KEY = 'fca_live_VZXZ0d9Ae7fu8JKNDauUcWafWyx7fDLUybkOOSLL'
CURRENCY_API = f'https://api.freecurrencyapi.com/v1/currencies?apikey={KEY}'
LATEST_API = 'https://api.freecurrencyapi.com/v1/latest'

def fetch_supported_currencies():
    try:
        req = urllib.request.Request(CURRENCY_API, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        if 'data' in data:
            currencies = {code: details['name'] for code, details in data['data'].items()}
            return currencies
    except Exception as e:
        print(f"Error fetching currencies: {e}")
        return {}

@app.route('/')
def index():
    currencies = fetch_supported_currencies()
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    amount = data.get('amount')
    from_currency = data.get('from')
    to_currency = data.get('to')

    if not amount:
        return jsonify({'error': 'Please enter a valid amount.'}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount value.'}), 400

    url = f'{LATEST_API}?apikey={KEY}&base_currency={from_currency}&currencies={to_currency}'

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

        if 'data' in data and to_currency in data['data']:
            rate = data['data'][to_currency]
            converted_amount = round(amount * rate, 2)
            return jsonify({'converted_amount': converted_amount})
        else:
            return jsonify({'error': 'Error fetching data from API.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
