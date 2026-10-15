import pandas as pd
import yfinance as yf
from config import TICKER, csv_path


def fetch_calgro_price_targets():
    print(f"Fetching analyst price targets for {TICKER}...")

    stock = yf.Ticker(TICKER)

    targets_dict = stock.analyst_price_targets

    if targets_dict and isinstance(targets_dict, dict):
        df = pd.DataFrame.from_dict(
            targets_dict, orient="index", columns=["Price (ZAc)"]
        )

        output_path = csv_path("price_targets")

        df.to_csv(output_path, index=True)

        print(f"Saved price targets data to {output_path}")
        print("\nPreview of data:")
        print(df)
        return df
    else:
        print(f"\nNo price targets found for {TICKER}.")
        print(
            "Note: Small-cap stocks on the JSE rarely have aggregated price target metrics on Yahoo Finance."
        )
        return None


if __name__ == "__main__":
    fetch_calgro_price_targets()
