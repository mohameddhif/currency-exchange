# Currency Exchange Application

A simple and secure currency converter built with Flask and the [Free Currency API](https://freecurrencyapi.com/).

## 🚀 Features

- **Real-time Conversion:** Fetches the latest exchange rates from a reliable API.
- **Support for Multiple Currencies:** Dynamically loads supported currencies for the "From" and "To" selections.
- **Modern UI:** Clean interface built with Bootstrap.
- **Secure Backend:** 
  - Environment variable management for API keys.
  - Robust error handling and input validation.
  - Protection against information leakage.
  - Use of the `requests` library for reliable API communication.

## 🛠️ Prerequisites

- Python 3.8+
- An API Key from [Free Currency API](https://freecurrencyapi.com/)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohameddhif/currency-exchange
   cd currency_exchange
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   FREE_CURRENCY_API_KEY=your_api_key_here
   FLASK_DEBUG=True
   ```

## 🏃 Running the Application

Start the Flask server:
```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

## 📁 Project Structure

- `app.py`: The main Flask application containing backend logic and API integration.
- `templates/`: HTML templates (Jinja2).
- `static/`: CSS and JavaScript files.
- `.env`: (Local only) Sensitive configuration and secrets.
- `.gitignore`: Ensures secrets and system files aren't tracked by Git.
- `requirements.txt`: List of Python dependencies.

## 🔒 Security Notes

This project follows security best practices:
- **Secret Management:** API keys are never hardcoded in the source.
- **Input Validation:** Amounts and currency codes are validated on the server side.
- **Error Handling:** System details are suppressed in production-ready error responses.

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
