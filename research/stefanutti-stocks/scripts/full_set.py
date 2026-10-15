import os
import pandas as pd
from config import TICKER, csv_name, GENERATED_DIR

from balance import fetch_calgro_balance_sheet
from cash_flows import fetch_calgro_cashflows
from closing import fetch_calgro_closing
from growth_est import fetch_calgro_growth_estimates
from income import fetch_calgro_income_statement
from price_targets import fetch_calgro_price_targets
from recommendations import fetch_calgro_recommendations


def create_full_workbook():
    workbook_name = csv_name("raw_data").replace(".csv", ".xlsx")
    output_dir = GENERATED_DIR / "models"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / workbook_name

    sheets = {
        "Balance Sheet": fetch_calgro_balance_sheet,
        "Cash Flows": fetch_calgro_cashflows,
        "Close Prices": fetch_calgro_closing,
        "Growth Estimates": fetch_calgro_growth_estimates,
        "Income Statement": fetch_calgro_income_statement,
        "Price Targets": fetch_calgro_price_targets,
        "Recommendations": fetch_calgro_recommendations,
    }

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, fetch_fn in sheets.items():
            print(f"\n--- {sheet_name} ---")
            df = fetch_fn()
            if df is not None and not df.empty:
                df = df.copy()
                if hasattr(df.index, "tz") and df.index.tz is not None:
                    df.index = df.index.tz_localize(None)
                df.to_excel(writer, sheet_name=sheet_name, index=True)
                print(f"Wrote {len(df)} rows to sheet '{sheet_name}'")
            else:
                print(f"Skipping '{sheet_name}' — no data returned")

    print(f"\nWorkbook saved to {output_path}")


if __name__ == "__main__":
    create_full_workbook()
