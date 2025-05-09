from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route("/nav")
def get_nav():
    try:
        # Example portfolio with weights
        portfolio = {
            "AAPL": 0.2,
            "MSFT": 0.2,
            "GOOGL": 0.2,
            "AMZN": 0.2,
            "TSLA": 0.2
        }

        total_nav = 0
        for ticker, weight in portfolio.items():
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")["Close"].iloc[-1]
            total_nav += price * weight

        return jsonify({"nav": f"${total_nav:.2f}"})

    except Exception as e:
        print("Error fetching NAV:", e)
        return jsonify({"nav": "Unavailable"})
