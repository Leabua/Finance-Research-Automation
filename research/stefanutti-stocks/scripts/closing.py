import yfinance as yf
from config import TICKER, csv_path


def fetch_calgro_closing():
    print(f"Fetching raw closing prices for {TICKER}...")

    stock = yf.Ticker(TICKER)

    df = stock.history(period="6mo")

    if not df.empty:
        close_data = df[["Close"]]

        output_path = csv_path("close")

        close_data.to_csv(output_path)
        print(f"Saved {len(close_data)} raw records to {output_path}")
        return close_data
    else:
        print("Error: No data found.")
        return None


if __name__ == "__main__":
    fetch_calgro_closing()
