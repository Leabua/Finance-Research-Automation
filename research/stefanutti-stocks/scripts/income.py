import yfinance as yf
from config import TICKER, csv_path


def fetch_calgro_income_statement():
    print(f"Fetching 4-year income statement for {TICKER}...")

    stock = yf.Ticker(TICKER)

    df = stock.income_stmt

    if df is not None and not df.empty:
        df.columns = df.columns.astype(str)

        output_path = csv_path("income_stmt")

        df.to_csv(output_path, index=True)
        print(f"Saved income statement ({len(df.columns)} years) to {output_path}")
        return df
    else:
        print("Error: No income statement data found or ticker is invalid.")
        return None


if __name__ == "__main__":
    fetch_calgro_income_statement()
