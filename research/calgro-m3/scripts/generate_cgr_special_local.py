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

def plot_special_cgr_local():
    print(f"Fetching 6mo data for CGR.JO from local CSV...")
    df = pd.read_csv(DATA_DIR / 'CGR_close.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Get last 6 months (approx 126 trading days)
    df_hist = df.tail(126).copy()

    hist_x = df_hist.index
    y_vals = df_hist['Close'].values
    
    first_price = y_vals[0]
    last_price = y_vals[-1]
    
    # Calculate percentage change for the key
    pct_change = ((last_price / first_price) - 1) * 100
    change_color = '#2ecc71' if pct_change >= 0 else '#e74c3c'
    sign = "+" if pct_change >= 0 else ""
    pct_text = f"{sign}{pct_change:.2f}% Period Return"
    
    # ---------------------------
    # Plotting: Loop through Light and Dark Themes
    # ---------------------------
    themes = [
        {'name': 'dark', 'bg': '#0d0d0d', 'text': 'white', 'grid': 'white', 'alpha_grid': 0.1, 'line': '#1d4ed8'},
        {'name': 'light', 'bg': '#ffffff', 'text': 'black', 'grid': 'black', 'alpha_grid': 0.08, 'line': '#1d4ed8'}
    ]

    for theme in themes:
        bg_color = theme['bg']
        text_color = theme['text']
        line_color = theme['line'] # Dark Blue
        
        fig, ax = plt.subplots(figsize=(1600/150, 800/150), dpi=800, edgecolor='#000000', linewidth=3)
        
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        ax.tick_params(colors=text_color, which='both')
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_color(text_color)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
            
        ax.set_ylabel('South African cents (c)', color=text_color, fontsize=11, fontweight='bold')
            
        ax.grid(color=theme['grid'], alpha=theme['alpha_grid'], linestyle='-', linewidth=0.5)

        # Plot the main Blue line
        ax.plot(hist_x, y_vals, color=line_color, linewidth=2.5, label='Price Movement', zorder=5)

        # ---------------------------
        # Gradient Fill from line to the bottom
        # ---------------------------
        N_layers = 15
        ymin_data = y_vals.min() * 0.95
        ax.set_ylim(bottom=ymin_data)

        # Dark Blue RGB = 29/255, 78/255, 216/255
        e_r, e_g, e_b = 29/255, 78/255, 216/255
        
        max_alpha = 0.25 if theme['name'] == 'dark' else 0.20
        
        for k in range(1, N_layers + 1):
            f_low = (k - 1) / N_layers
            f_high = k / N_layers
            f_mid = (f_low + f_high) / 2
            
            # Non-linear fade: Darker near the line (f_mid -> 1), lighter near x-axis (f_mid -> 0)
            alpha_layer = max_alpha * (f_mid ** 1.73)
            
            y_bottom = ymin_data + f_low * (y_vals - ymin_data)
            y_top = ymin_data + f_high * (y_vals - ymin_data)
            
            ax.fill_between(hist_x, y_bottom, y_top, color=(e_r, e_g, e_b, alpha_layer), edgecolor='none', zorder=2)

        # ---------------------------
        # Annotations
        # ---------------------------
        may_date = hist_x[hist_x > pd.Timestamp('2026-05-17', tz=hist_x.tz)]
        if len(may_date) > 0:
            md = may_date[0]
            mp = df_hist.loc[md, 'Close']
            
            # Use white bbox for light mode to ensure max legibility
            bbox_fc = '#ffffff' if theme['name'] == 'light' else bg_color
            bbox_tc = '#000000' if theme['name'] == 'light' else text_color

            ax.annotate("FY2026 AFS released", 
                        xy=(md, mp), xytext=(0, 45), textcoords='offset points',
                        color=bbox_tc, ha='center', va='bottom', fontsize=12, fontweight='bold',
                        arrowprops=dict(arrowstyle="->", color='#3498db', lw=1.5),
                        bbox=dict(facecolor=bbox_fc, alpha=1.0, edgecolor='#3498db', pad=4), zorder=6)

        # Adjust limits
        total_days = (hist_x[-1] - hist_x[0]).days
        padding_days = int(total_days * 0.08)
        if padding_days < 1: padding_days = 1
        ax.set_xlim(hist_x[0], hist_x[-1] + pd.DateOffset(days=padding_days))
        
        # Plot percentage change as a standalone pseudo-key
        ax.text(0.03, 0.95, pct_text, transform=ax.transAxes,
                color=change_color, fontsize=12, fontweight='bold', ha='left', va='top',
                bbox=dict(facecolor=bg_color, alpha=0.9, edgecolor=change_color, pad=4, boxstyle='round,pad=0.3'), zorder=6)

        plt.subplots_adjust(top=0.92, bottom=0.15, left=0.08, right=0.92)

        watermark_text = f"Generated {datetime.now().strftime('%Y-%m-%d')} · Data: Local"
        fig.text(0.92, 0.05, watermark_text, color='#a0a0a0', fontsize=9, ha='right', va='center')
        
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        out_path = FIGURES_DIR / f'CGR_6mo_special_movement_{theme["name"]}.png'
        plt.savefig(out_path, facecolor=bg_color, bbox_inches='tight', dpi=800, edgecolor='#000000')
        plt.close(fig)
        print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    plot_special_cgr_local()
