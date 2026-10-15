import yfinance as yf
from config import TICKER, csv_path


def fetch_calgro_growth_estimates():
    print(f"Fetching analyst growth estimates for {TICKER}...")

    stock = yf.Ticker(TICKER)

    df = stock.get_growth_estimates()

    if df is not None and not df.empty:
        output_path = csv_path("growth_estimates")

        df.to_csv(output_path, index=True)

        print(f"Saved growth estimates data to {output_path}")
        print("\nPreview of data:")
        print(df)
        return df
    else:
        print(f"\nNo growth estimates found for {TICKER}.")
        print(
            "Note: JSE small-caps rarely have forward-looking institutional growth consensus tables compiled on Yahoo Finance."
        )
        return None


if __name__ == "__main__":
    fetch_calgro_growth_estimates()
