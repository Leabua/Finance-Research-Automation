# Running the research automation

## Review the completed work

Open the reports and PNG figures on GitHub, or download the Excel files from the [portfolio index](../README.md). The published models contain the analysis and formulas; a Python environment is only needed to run the scripts.

## Set up Python

From the repository root, use a Python environment compatible with the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with `.venv\Scripts\Activate.ps1` in PowerShell.

## Generate J-curves from the saved assumptions

These commands do not fetch market data:

```bash
python research/calgro-m3/scripts/generate_bankenveld.py
python research/calgro-m3/scripts/generate_memorial_parks.py
python research/calgro-m3/scripts/generate_fleurhof_south_hills.py
python research/calgro-m3/scripts/generate_combined.py
```

The numerical assumptions are embedded in the original chart scripts. Outputs are written to `research/calgro-m3/generated/figures/`. Chart paths are resolved from the script location, so the commands also work from other working directories. The original scripts export high-resolution figures and can take some time to render.

The metric, header and scenario table scripts render the values stored in their source code; they do not recalculate those values from the Excel models.

## Generate another Monte Carlo forecast

Install the optional forecasting dependency, then run:

```bash
python -m pip install -r requirements-forecast.txt
python research/calgro-m3/scripts/generate_monte_carlo.py
```

The script reads the saved `research/calgro-m3/data/CGR_close.csv`, resamples the observations to month-end and fits exponential smoothing to the last 60 monthly log prices. It retains the historical research assumption of a **430 ZAc final observation**, then simulates 1,000 paths across 36 months.

The forecast CSV is written to `generated/data/` and the charts to `generated/figures/` within the Calgro case study. The published figures and forecast CSV remain the original research outputs. The historical dependency versions and simulation seed were not recorded, so a new run is not expected to reproduce the archived percentiles exactly. The [official Darts installation guide](https://unit8co.github.io/darts/quickstart/00-quickstart.html) provides environment guidance.

## Refresh financial data

These commands require internet access and request new data from Yahoo Finance through `yfinance`:

```bash
python research/calgro-m3/scripts/full_set.py
python research/stefanutti-stocks/scripts/full_set.py
```

Each command saves CSV exports to its case study's `generated/data/` and a raw-data workbook to `generated/models/`. Data availability depends on provider coverage for the ticker; sheets with no returned data are skipped.

The generated raw-data workbooks do not recreate the manually developed standardisation, ratio or project-model sheets in the published Excel files. Updating those models requires reviewing the new data and revising the assumptions separately.

`generate_recent_movements.py` fetches new prices for CGR and SSK, while `generate_cgr_special.py` fetches new CGR prices. Both retain the original CGR price override of 430 ZAc. `generate_cgr_special_local.py` uses the saved Calgro closing-price CSV instead. Review those historical assumptions before using the scripts for a new research date.

All generated outputs are ignored by Git so that running the scripts keeps the archived research intact.
