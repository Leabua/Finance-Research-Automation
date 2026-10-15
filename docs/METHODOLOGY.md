# Methodology and data notes

## Research workflow

1. Collect financial statements, closing prices and available analyst fields using the Python scripts and `yfinance`.
2. Save CSV exports and assemble a raw-data Excel workbook.
3. Standardise the financial statements and develop ratios and company-specific scenarios in Excel.
4. Assess the business, reported results, valuation, catalysts and risks in a written report.
5. Present the cash-flow scenarios, price movements and forecast distributions as figures.

The Excel research models and written reports contain the judgement and company-specific work. The data-export scripts automate collection and workbook assembly.

## Calgro M3 cash-flow scenarios

The models separate Bankenveld, Memorial Parks, and the other residential developments. Chart scripts contain arrays for annual inflows, annual outflows and cumulative free cash flow. The cumulative lines use shape-preserving interpolation for presentation, while the annual bars show the discrete inputs. The break-even markers follow those scenario inputs.

The combined cash-flow chart covers a ten-year window; individual project charts can cover longer periods. These are the original scenario horizons and should be read with the workbook and report.

## Calgro M3 probabilistic forecast

The saved Monte Carlo chart was generated using Darts exponential smoothing on log-transformed monthly prices. The script uses 60 monthly observations, a 36-month forecast horizon and 1,000 simulated paths. It exports the mean, median and 10th, 25th, 75th and 90th percentiles to CSV.

The final observed price is explicitly set to 430 ZAc in the script. This is a historical research assumption rather than a live quote. The simulated price distribution and the fundamental project valuation are separate parts of the research.

The original environment and random seed are not recorded. The committed forecast CSV and PNGs therefore serve as the record of the original simulation; subsequent runs can produce different paths and percentiles.

## Stefanutti Stocks

The Excel model includes statement standardisation, ratios, order-book scenarios and an infrastructure-pipeline scenario. The later report incorporates the FY2026 reviewed company results and distinguishes the Kusile settlement from recurring operating performance. Saved CSV exports and workbook sheets span different reporting periods, so the report's source notes matter when comparing figures.

## Sources, dates and units

- Financial-statement and price CSVs were exported using `yfinance`; the saved files are research-period snapshots.
- The SSK FY2026 results PDF is a company source document, stored separately from the authored report.
- Further company, announcement and market sources are listed in the original reports.
- Share prices marked **ZAc** are in South African cents; **ZAR** and **R** refer to South African rand. Follow each chart's scale, including thousands, millions or billions.
- Forecast assumptions, market prices and valuation multiples belong to the research date. Publishing the portfolio does not update the underlying analysis.

## Preservation

The main Excel workbooks, Calgro PDF, source documents, saved CSVs and original PNG figures are copied from the supplied collection. Earlier report and workbook versions are labelled in each case study's archive. Script changes for this publication concern file locations and generated-output separation; the original model assumptions are retained.

[File provenance](PROVENANCE.md) · [Running instructions](RUNNING.md)
