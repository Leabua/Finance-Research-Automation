import yfinance as yf
from config import TICKER, csv_path


def fetch_calgro_recommendations():
    print(f"Fetching analyst recommendations for {TICKER}...")

    stock = yf.Ticker(TICKER)

    df = stock.recommendations_summary

    if df is not None and not df.empty:
        output_path = csv_path("recommendations")

        df.to_csv(output_path, index=True)
        print(f"Saved recommendations data to {output_path}")
        print("\nPreview of data:")
        print(df.head())
        return df
    else:
        print(f"\nNo recommendations found for {TICKER}.")
        print("Note: small caps don't get recommendations on yfinance.")
        return None


if __name__ == "__main__":
    fetch_calgro_recommendations()
