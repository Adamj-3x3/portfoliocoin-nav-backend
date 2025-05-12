from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import json

# Toggle this to 'contract' in the future to switch to on-chain weights
DATA_SOURCE = "json"

app = Flask(__name__)
CORS(app, origins=["https://portfolio-frontend-working.vercel.app"])

@app.route("/nav")
def get_nav():
    try:
        if DATA_SOURCE == "json":
            with open("portfolio_weights.json") as f:
                portfolio = json.load(f)

        elif DATA_SOURCE == "contract":
            # Placeholder for on-chain logic (to be implemented later)
            portfolio = {}
            print("Smart contract integration not yet implemented.")

        total_nav = 0
        for ticker, weight in portfolio.items():
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                price = hist["Close"].iloc[-1]
                total_nav += price * weight

        return jsonify({"nav": f"${total_nav:.2f}"})

    except Exception as e:
        print("Error fetching NAV:", e)
        return jsonify({"nav": "Unavailable"})
