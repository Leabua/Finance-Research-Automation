import yfinance as yf
from config import TICKER, csv_path


def fetch_calgro_cashflows():
    print(f"Fetching 4-year cash flows for {TICKER}...")

    stock = yf.Ticker(TICKER)

    df = stock.cashflow

    if df is not None and not df.empty:
        df.columns = df.columns.astype(str)

        output_path = csv_path("cashflows")

        df.to_csv(output_path, index=True)
        print(f"Saved cash flows ({len(df.columns)} years) to {output_path}")
        return df
    else:
        print("Error: No cash flows data found or ticker is invalid.")
        return None


if __name__ == "__main__":
    fetch_calgro_cashflows()
