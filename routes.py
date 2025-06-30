import requests
from flask import render_template, request

def register_routes(app):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        converted_amount = None
        error = None
        amount = 0
        from_currency = to_currency = ""
        symbols = []

        # Get currency symbols from Frankfurter API
        symbols_url = "https://api.frankfurter.app/currencies"
        try:
            response = requests.get(symbols_url)
            response.raise_for_status()
            data = response.json()
            symbols = list(data.keys())
        except Exception as e:
            error = f"Failed to fetch symbols: {str(e)}"

        if request.method == 'POST' and not error:
            try:
                amount = float(request.form['amount'])
                from_currency = request.form['from_currency']
                to_currency = request.form['to_currency']

                convert_url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
                conv_response = requests.get(convert_url)
                conv_response.raise_for_status()
                conv_data = conv_response.json()

                if "rates" in conv_data and to_currency in conv_data["rates"]:
                    converted_amount = conv_data["rates"][to_currency]
                else:
                    error = "Conversion failed: no rates found."
            except Exception as e:
                error = "Conversion failed. Please try again."

        return render_template('index.html',
                               symbols=symbols,
                               converted_amount=converted_amount,
                               amount=amount,
                               from_currency=from_currency,
                               to_currency=to_currency,
                               error=error)
