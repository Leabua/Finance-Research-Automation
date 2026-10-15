import yfinance as yf
from config import TICKER, csv_path


def fetch_calgro_balance_sheet():
    print(f"Fetching 4-year balance sheet for {TICKER}...")

    stock = yf.Ticker(TICKER)

    df = stock.balance_sheet

    if df is not None and not df.empty:
        df.columns = df.columns.astype(str)

        output_path = csv_path("balance_sheet")

        df.to_csv(output_path, index=True)
        print(f"Saved balance sheet ({len(df.columns)} years) to {output_path}")
        return df
    else:
        print("Error: No balance sheet data found or ticker is invalid.")
        return None


if __name__ == "__main__":
    fetch_calgro_balance_sheet()
