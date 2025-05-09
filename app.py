from flask import Flask, jsonify
import threading
import time
import yfinance as yf

app = Flask(__name__)
cached_nav = {"nav": "$0.00"}

PORTFOLIO = {
    "AAPL": 0.2,
    "MSFT": 0.2,
    "GOOGL": 0.2,
    "NVDA": 0.2,
    "AMZN": 0.2,
}

def calculate_nav():
    total = 0
    for ticker, weight in PORTFOLIO.items():
        price = yf.Ticker(ticker).info["regularMarketPrice"]
        total += weight * price
    return round(total, 2)

def refresh_nav_every_hour():
    while True:
        try:
            nav_value = calculate_nav()
            cached_nav["nav"] = f"${nav_value}"
            print(f"Updated NAV: {cached_nav['nav']}")
        except Exception as e:
            print(f"Error updating NAV: {e}")
        time.sleep(3600)  # wait one hour

@app.route("/nav")
def get_nav():
    return jsonify(cached_nav)

if __name__ == "__main__":
    threading.Thread(target=refresh_nav_every_hour, daemon=True).start()
    app.run(debug=False, host='0.0.0.0')

