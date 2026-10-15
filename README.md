# Finance Research Automation

**Equity research, Excel financial modelling and Python automation for South African listed companies.**

By [Leabua Khomari](https://github.com/Leabua)

This portfolio brings together financial statement analysis, company research, project cash-flow models and visualisation. The two case studies cover Calgro M3 and Stefanutti Stocks, with the Excel models, written research, supporting data and Python scripts available together.

## Explore the work

| Case study | Excel model | Written research | Focus |
| :--- | :--- | :--- | :--- |
| **Calgro M3 · JSE: CGR** | [Completed model (.xlsx)](research/calgro-m3/models/CGR-Full-with-Models.xlsx) · [Download](https://github.com/Leabua/Finance-Research-Automation/raw/refs/heads/main/research/calgro-m3/models/CGR-Full-with-Models.xlsx) | [May 2026 report (.pdf)](research/calgro-m3/reports/Calgro-May-2026-Analysis.pdf) | Property development, segment cash flows, J-curves and probabilistic forecasting |
| **Stefanutti Stocks · JSE: SSK** | [Research model (.xlsx)](research/stefanutti-stocks/models/SSK-Full-Model.xlsx) · [Download](https://github.com/Leabua/Finance-Research-Automation/raw/refs/heads/main/research/stefanutti-stocks/models/SSK-Full-Model.xlsx) | [26 May 2026 report](research/stefanutti-stocks/reports/Stefanutti-Stocks-Equity-Research.md) | Balance-sheet restructuring, earnings normalisation, order-book conversion and infrastructure scenarios |

The reports and figures reflect the **May 2026 research period**. Prices, financial inputs and forward scenarios are presented in that historical context.

## What the projects demonstrate

- **Financial modelling:** standardising reported financials, calculating ratios, and modelling project inflows, outflows and cumulative free cash flow in Excel.
- **Equity research:** connecting company strategy, financial performance, valuation, catalysts and risks in written investment research.
- **Research automation:** collecting financial statements and price histories with Python, exporting CSV datasets, and assembling Excel data workbooks.
- **Scenario analysis and visualisation:** modelling the timing of project cash flows and presenting forecast distributions, J-curves and market movements.

## Selected results

### Calgro M3: Monte Carlo forecast

The original forecast uses **1,000 simulated paths over 36 months**, with exponential smoothing fitted to log-transformed monthly prices. The shaded bands show the 10th–90th and 25th–75th percentiles. The 430 ZAc starting price is the research-period assumption.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="research/calgro-m3/figures/CGR_monte_carlo_forecast_dark.png">
  <img src="research/calgro-m3/figures/CGR_monte_carlo_forecast_light.png" alt="Calgro M3 historical prices and 36-month Monte Carlo forecast, showing the median and percentile bands" width="100%">
</picture>

[Forecast data (.csv)](research/calgro-m3/data/CGR_monte_carlo_forecast.csv) · [Forecast script](research/calgro-m3/scripts/generate_monte_carlo.py)

### Bankenveld: project cash-flow J-curve

The segment model traces the initial investment period, delivery ramp, peak activity and eventual tail. Annual cash inflows and outflows sit alongside cumulative free cash flow, making the funding period and modelled break-even point visible.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="research/calgro-m3/figures/bankenveld_jcurve_dark.png">
  <img src="research/calgro-m3/figures/bankenveld_jcurve_light.png" alt="Bankenveld project J-curve with annual cash inflows, annual outflows, cumulative free cash flow and modelled break-even" width="100%">
</picture>

[Excel model](research/calgro-m3/models/CGR-Full-with-Models.xlsx) · [Chart script](research/calgro-m3/scripts/generate_bankenveld.py)

### Calgro M3: combined project cash flows

The consolidated view combines Bankenveld, Memorial Parks and the active integrated residential developments over the model's ten-year window. It shows how cash from mature projects interacts with investment in the development pipeline.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="research/calgro-m3/figures/combined_jcurve_dark.png">
  <img src="research/calgro-m3/figures/combined_jcurve_light.png" alt="Calgro M3 combined ten-year cash-flow model, with segment inflows and outflows and cumulative free cash flow" width="100%">
</picture>

[Memorial Parks J-curve](research/calgro-m3/figures/memorial_parks_jcurve_light.png) · [Fleurhof and South Hills J-curve](research/calgro-m3/figures/fleurhof_south_hills_jcurve_light.png) · [All Calgro figures](research/calgro-m3/figures)

The J-curves illustrate the original model assumptions. The Monte Carlo distribution describes the fitted price model; it is separate from the fundamental valuation and project cash-flow scenarios.

## Inside the case studies

**[Calgro M3](research/calgro-m3/README.md)** includes a 12-sheet workbook with standardised financials, cumulative outlays, Bankenveld, Memorial Parks and other residential developments, alongside underlying statements and price data. The report examines the development pipeline, capital intensity, leverage and valuation. Both light and dark versions of the result charts are included.

**[Stefanutti Stocks](research/stefanutti-stocks/README.md)** includes an 11-sheet workbook with standardised financials, ratios, order-book J-curves and infrastructure scenarios. The accompanying report examines the restructuring, Kusile settlement, recurring earnings, cash conversion and execution risks. The company's [FY2026 reviewed results](research/stefanutti-stocks/sources/SSK-FY2026-Reviewed-Results.pdf) are stored separately as a source document.

The earlier [Standards and Curves workbook (.ods)](foundations/Standards-and-Curves.ods) documents the spreadsheet foundations behind the work. See its [notes](foundations/README.md) for the historical linked-file references.

## Repository layout

```text
research/
  calgro-m3/
  stefanutti-stocks/
    models/     Excel research models
    reports/    Written research
    data/       Saved CSV inputs and results
    figures/    Original charts and tables
    scripts/    Python data collection and chart generation
    archive/    Earlier models and report versions
foundations/    Earlier spreadsheet work
docs/           Methodology, running instructions and file provenance
```

Both case studies use the same folder structure; the SSK company results are in `sources/`, and the editable Calgro write-up is in `reports/source/`.

## Work with the files

The reports and figures can be viewed directly on GitHub. Download the `.xlsx` models and open them in Excel or LibreOffice to inspect the formulas and assumptions. No Python setup is needed to review the completed work.

To run the automation, see [running the scripts](docs/RUNNING.md). Generated outputs are saved separately from the published research models and original figures.

[Methodology and data notes](docs/METHODOLOGY.md) · [File provenance](docs/PROVENANCE.md)
