from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# Delay imports for darts to ensure it is installed first
def run():
    from darts import TimeSeries
    from darts.models import ExponentialSmoothing
    from darts.utils.utils import ModelMode, SeasonalityMode

    # Load data
    file_path = DATA_DIR / 'CGR_close.csv'
    df = pd.read_csv(file_path, parse_dates=[0], index_col=0)
    
    # In case there are multiple columns, take the first one or 'Close'
    if 'Close' in df.columns:
        df = df[['Close']]
    else:
        df.columns = ['Close']
        
    df = df.dropna()

    # Make index tz-naive if it's tz-aware to prevent issues with darts
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    # Resample to monthly (last trading day of the month)
    # Using 'ME' for month-end frequency
    df_monthly = df.resample('ME').last()
    df_monthly = df_monthly.dropna()

    # Take last 60 months
    df_hist = df_monthly.iloc[-60:].copy()

    # Historical May 2026 research assumption: anchor the final price at 430 ZAc
    if 'Close' in df_hist.columns:
        df_hist.iloc[-1, df_hist.columns.get_loc('Close')] = 430.0

    # Log transform to prevent negative prices and capture geometric brownian motion-like behavior
    df_log = np.log(df_hist)

    # Create TimeSeries
    ts = TimeSeries.from_series(df_log['Close'])

    # Fit ETS model (Exponential Smoothing)
    # Financial data typically doesn't have fixed seasonal patterns, so we disable seasonality
    # and use an additive trend on log prices (which corresponds to multiplicative trend on raw prices).
    try:
        model = ExponentialSmoothing(trend=ModelMode.ADDITIVE, seasonal=SeasonalityMode.NONE)
        model.fit(ts)
    except Exception as e:
        # Fallback if specific imports fail or change in darts versions
        model = ExponentialSmoothing()
        model.fit(ts)

    # Generate 1000 paths projected 36 months forward
    samples_ts = model.predict(n=36, num_samples=1000)
    
    # Extract values: shape is (36, 1, 1000) -> squeeze to (36, 1000)
    samples_log = samples_ts.all_values().squeeze()
    
    # Convert back from log scale
    samples_exp = np.exp(samples_log)

    # Calculate percentiles
    p10 = np.percentile(samples_exp, 10, axis=1)
    p25 = np.percentile(samples_exp, 25, axis=1)
    p50 = np.percentile(samples_exp, 50, axis=1)
    p75 = np.percentile(samples_exp, 75, axis=1)
    p90 = np.percentile(samples_exp, 90, axis=1)
    mean_vals = np.mean(samples_exp, axis=1)

    # Prepare x-axis arrays
    hist_x = df_hist.index
    forecast_x = pd.date_range(start=hist_x[-1], periods=37, freq='ME')[1:]

    # Prepend last historical value to forecast arrays so lines connect seamlessly
    last_price = df_hist['Close'].iloc[-1]
    p10 = np.insert(p10, 0, last_price)
    p25 = np.insert(p25, 0, last_price)
    p50 = np.insert(p50, 0, last_price)
    p75 = np.insert(p75, 0, last_price)
    p90 = np.insert(p90, 0, last_price)
    mean_vals = np.insert(mean_vals, 0, last_price)
    fc_x = np.insert(forecast_x, 0, hist_x[-1])

    # ---------------------------
    # Export Forecast Data to CSV
    # ---------------------------
    df_export = pd.DataFrame({
        'Date': fc_x,
        'P10_Bear_Boundary': p10,
        'P25': p25,
        'Median_Forecast_P50': p50,
        'Mean_Path': mean_vals,
        'P75': p75,
        'P90_Bull_Boundary': p90
    })
    (GENERATED_DIR / 'data').mkdir(parents=True, exist_ok=True)
    df_export.to_csv(GENERATED_DIR / 'data' / 'CGR_monte_carlo_forecast.csv', index=False)
    print(f"Successfully exported Monte Carlo forecast data to {GENERATED_DIR / 'data' / 'CGR_monte_carlo_forecast.csv'}")

    # ---------------------------
    # Plotting: Loop through Light and Dark Themes
    # ---------------------------
    themes = [
        {'name': 'dark', 'bg': '#0d0d0d', 'text': 'white', 'grid': 'white', 'alpha_grid': 0.1, 'watermark_alpha': 0.4},
        {'name': 'light', 'bg': '#ffffff', 'text': 'black', 'grid': 'black', 'alpha_grid': 0.08, 'watermark_alpha': 0.3}
    ]

    for theme in themes:
        bg_color = theme['bg']
        text_color = theme['text']
        
        # Restore the larger physical dimensions to keep text properly proportioned
        # while using dpi=800 for a high-res 2x scale output
        fig, ax = plt.subplots(figsize=(1600/150, 800/150), dpi=800, edgecolor='#000000', linewidth=3)
        
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        # Axes colors
        ax.tick_params(colors=text_color, which='both')
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_color(text_color)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
            
        ax.grid(color=theme['grid'], alpha=theme['alpha_grid'], linestyle='-', linewidth=0.5)

        # 1. Forecast bands
        ax.fill_between(fc_x, p10, p90, color='#8e44ad', alpha=0.15, label='10th - 90th Percentile Band')
        ax.fill_between(fc_x, p25, p75, color='#8e44ad', alpha=0.35, label='25th - 75th Percentile Band')

        # 2. Historical Prices
        ax.plot(hist_x, df_hist['Close'], color='#9b59b6', linewidth=2.5, label='Historical Prices (60 months)')

        # 3. Forecast lines
        ax.plot(fc_x, p50, color='#FF8C00', linewidth=2, label='Median Forecast (P50)')
        ax.plot(fc_x, mean_vals, color='#FFD700', linestyle='--', linewidth=1.5, label='Mean Path')
        ax.plot(fc_x, p75, color='#2ecc71', linestyle=':', linewidth=1.0, alpha=0.7, label='P75')
        ax.plot(fc_x, p25, color='#e74c3c', linestyle=':', linewidth=1.0, alpha=0.7, label='P25')
        ax.plot(fc_x, p10, color='#e74c3c', linestyle=':', linewidth=1.5, label='P10 Bear Boundary')
        ax.plot(fc_x, p90, color='#2ecc71', linestyle=':', linewidth=1.5, label='P90 Bull Boundary')

        # 4. Separator
        sep_x = hist_x[-1]
        ax.axvline(x=sep_x, color=text_color, linestyle='--', alpha=0.6, linewidth=0.8)

        # Separator label: perfectly centering the pipe "|"
        y_max = ax.get_ylim()[1]
        
        # Increase offset to prevent bounding boxes from overlapping
        ax.text(sep_x - pd.DateOffset(days=20), y_max * 0.96, '◄ Historical', color=text_color, ha='right', va='center', 
                fontsize=10, fontweight='normal', zorder=6)
        
        # Draw the pipe precisely as a solid vertical line segment on top
        pipe_y_min = y_max * 0.945
        pipe_y_max = y_max * 0.975
        ax.plot([sep_x, sep_x], [pipe_y_min, pipe_y_max], color=text_color, lw=1.5, zorder=8)
        
        ax.text(sep_x + pd.DateOffset(days=20), y_max * 0.96, 'Forecast ►', color=text_color, ha='left', va='center', 
                fontsize=10, fontweight='normal', zorder=6)

        # White/Black dot at current price, with label pointing to it via arrow
        ax.plot(sep_x, last_price, marker='o', color=text_color, markersize=5, zorder=5)
        ax.annotate(f"{int(last_price)} ZAc", xy=(sep_x, last_price), xytext=(-35, 35), textcoords='offset points', 
                    color=text_color, ha='right', va='bottom', fontsize=11, fontweight='bold',
                    arrowprops=dict(arrowstyle="->", color=text_color, lw=1.2, relpos=(1.0, 0.0)), zorder=6)

        # 5. End values (Annotations)
        end_x = fc_x[-1]
        total_days = (end_x - hist_x[0]).days
        padding_days = int(total_days * 0.12)
        ax.set_xlim(hist_x[0], end_x + pd.DateOffset(days=padding_days))

        bbox_props = dict(alpha=1.0, edgecolor='none', boxstyle='round,pad=0.4')
        
        b90 = bbox_props.copy()
        b90['facecolor'] = '#2ecc71'
        ax.text(end_x, p90[-1], f" P90: {int(p90[-1])} ZAc ", color='#000000', va='center', ha='left', 
                fontsize=10, fontweight='bold', bbox=b90)
                
        b75 = bbox_props.copy()
        b75['facecolor'] = '#2ecc71'
        b75['alpha'] = 1.0
        ax.text(end_x, p75[-1], f" P75: {int(p75[-1])} ZAc ", color='#000000', va='center', ha='left', 
                fontsize=9, fontweight='bold', bbox=b75)
                
        b50 = bbox_props.copy()
        b50['facecolor'] = '#FF8C00'
        ax.text(end_x, p50[-1], f" Median: {int(p50[-1])} ZAc ", color='#000000', va='center', ha='left', 
                fontsize=10, fontweight='bold', bbox=b50)

        b25 = bbox_props.copy()
        b25['facecolor'] = '#e74c3c'
        b25['alpha'] = 1.0
        ax.text(end_x, p25[-1], f" P25: {int(p25[-1])} ZAc ", color='#ffffff', va='center', ha='left', 
                fontsize=9, fontweight='bold', bbox=b25)
                
        b10 = bbox_props.copy()
        b10['facecolor'] = '#e74c3c'
        ax.text(end_x, p10[-1], f" P10: {int(p10[-1])} ZAc ", color='#ffffff', va='center', ha='left', 
                fontsize=10, fontweight='bold', bbox=b10)

        # 7. Legend
        ax.legend(loc='upper left', frameon=True, facecolor=bg_color, edgecolor=text_color, labelcolor=text_color, framealpha=0.8)

        # Apply specific padding layout to prevent squishing
        plt.subplots_adjust(top=0.85, bottom=0.15, left=0.08, right=0.92)

        # 8. Titles (placed absolutely on the figure)
        fig.text(0.08, 0.94, 'CalgroM3 Holdings (CGR.JO) — Monte Carlo Probabilistic Forecast', color=text_color, fontsize=16, fontweight='bold', ha='left')
        fig.text(0.08, 0.90, '1,000 sample paths · 36-month horizon · ExponentialSmoothing on log-transformed monthly prices', color=text_color, fontsize=11, alpha=0.8, ha='left')

        # 6. Watermark (bottom right, below x-axis, smaller light grey)
        watermark_text = f"Generated {datetime.now().strftime('%Y-%m-%d')} · Data: yfinance · Model: darts ETS"
        fig.text(0.92, 0.05, watermark_text, color='#a0a0a0', fontsize=9, ha='right', va='center')
        
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        out_path = FIGURES_DIR / f'CGR_monte_carlo_forecast_{theme["name"]}.png'
        plt.savefig(out_path, facecolor=bg_color, bbox_inches='tight', dpi=800, edgecolor='#000000')
        plt.close(fig)
        print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    run()
