from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import os
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

def plot_stock(ticker, period, name_full, current_price_override=None):
    print(f"Fetching {period} data for {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    if df.empty:
        print(f"No data for {ticker}")
        return

    # Use the close prices
    df_hist = df[['Close']].copy()

    if current_price_override is not None:
        df_hist.iloc[-1, df_hist.columns.get_loc('Close')] = current_price_override

    first_price = df_hist['Close'].iloc[0]
    last_price = df_hist['Close'].iloc[-1]
    last_date = df_hist.index[-1]
    
    # Calculate percentage change
    pct_change = ((last_price / first_price) - 1) * 100
    change_color = '#2ecc71' if pct_change >= 0 else '#e74c3c'
    sign = "+" if pct_change >= 0 else ""
    pct_text = f"{sign}{pct_change:.2f}% Period Return"
    
    # ---------------------------
    # Plotting: Loop through Light and Dark Themes
    # ---------------------------
    themes = [
        {'name': 'dark', 'bg': '#0d0d0d', 'text': 'white', 'grid': 'white', 'alpha_grid': 0.1, 'line': '#9b59b6'},
        {'name': 'light', 'bg': '#ffffff', 'text': 'black', 'grid': 'black', 'alpha_grid': 0.08, 'line': '#8e44ad'}
    ]

    for theme in themes:
        bg_color = theme['bg']
        text_color = theme['text']
        line_color = theme['line']
        
        fig, ax = plt.subplots(figsize=(1600/150, 800/150), dpi=800, edgecolor='#000000', linewidth=3)
        
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        ax.tick_params(colors=text_color, which='both')
        for spine in ['bottom', 'left']:
            ax.spines[spine].set_color(text_color)
        for spine in ['top', 'right']:
            ax.spines[spine].set_visible(False)
            
        ax.grid(color=theme['grid'], alpha=theme['alpha_grid'], linestyle='-', linewidth=0.5)

        hist_x = df_hist.index
        ax.plot(hist_x, df_hist['Close'], color=line_color, linewidth=2.5, label='Price Movement')

        # Current price dot and arrow
        ax.plot(last_date, last_price, marker='o', color=text_color, markersize=5, zorder=5)
        ax.annotate(f"{int(last_price)} ZAc", xy=(last_date, last_price), xytext=(-35, 35), textcoords='offset points', 
                    color=text_color, ha='right', va='bottom', fontsize=11, fontweight='bold',
                    arrowprops=dict(arrowstyle="->", color=text_color, lw=1.2, relpos=(1.0, 0.0)), zorder=6)

        # ---------------------------
        # Annotations for 6-Month charts
        # ---------------------------
        if period == "6mo":
            if ticker.startswith("SSK"):
                # SSK March/May Events
                # 1. May Trading Statement (mid-May)
                may_date = hist_x[hist_x > pd.Timestamp('2026-05-14', tz=hist_x.tz)]
                if len(may_date) > 0:
                    md = may_date[0]
                    mp = df_hist.loc[md, 'Close']
                    ax.annotate("May 15: Positive Trading Statement\n(195-215% HEPS forecast jump)", 
                                xy=(md, mp), xytext=(-10, 60), textcoords='offset points',
                                color=text_color, ha='center', va='bottom', fontsize=9,
                                arrowprops=dict(arrowstyle="->", color='#3498db', lw=1.5),
                                bbox=dict(facecolor=bg_color, alpha=1.0, edgecolor='#3498db', pad=3))
                
                # 2. March/Eskom Context (Early March/late Feb surge)
                mar_date = hist_x[(hist_x >= pd.Timestamp('2026-03-01', tz=hist_x.tz)) & (hist_x <= pd.Timestamp('2026-03-15', tz=hist_x.tz))]
                if len(mar_date) > 0:
                    md2 = mar_date[0]
                    mp2 = df_hist.loc[md2, 'Close']
                    ax.annotate("March Momentum:\nDelayed Eskom Settlement & Debt Reduction Impact", 
                                xy=(md2, mp2), xytext=(-60, 40), textcoords='offset points',
                                color=text_color, ha='center', va='bottom', fontsize=9,
                                arrowprops=dict(arrowstyle="->", color='#e67e22', lw=1.5),
                                bbox=dict(facecolor=bg_color, alpha=1.0, edgecolor='#e67e22', pad=3))

            elif ticker.startswith("CGR"):
                # CGR Bankenveld / May results
                may_date = hist_x[hist_x > pd.Timestamp('2026-05-17', tz=hist_x.tz)]
                if len(may_date) > 0:
                    md = may_date[0]
                    mp = df_hist.loc[md, 'Close']
                    ax.annotate("May 18: FY26 Results &\nBankenveld R18bn Development", 
                                xy=(md, mp), xytext=(-30, 50), textcoords='offset points',
                                color=text_color, ha='right', va='bottom', fontsize=9,
                                arrowprops=dict(arrowstyle="->", color='#3498db', lw=1.5),
                                bbox=dict(facecolor=bg_color, alpha=1.0, edgecolor='#3498db', pad=3))

        # Adjust limits
        total_days = (hist_x[-1] - hist_x[0]).days
        padding_days = int(total_days * 0.08)
        if padding_days < 1: padding_days = 1
        ax.set_xlim(hist_x[0], hist_x[-1] + pd.DateOffset(days=padding_days))
        
        # Plot percentage change as a standalone pseudo-key
        ax.text(0.03, 0.95, pct_text, transform=ax.transAxes,
                color=change_color, fontsize=12, fontweight='bold', ha='left', va='top',
                bbox=dict(facecolor=bg_color, alpha=1.0, edgecolor=change_color, pad=4, boxstyle='round,pad=0.3'))

        plt.subplots_adjust(top=0.85, bottom=0.15, left=0.08, right=0.92)

        period_text = "3-Month" if period == "3mo" else "6-Month"
        fig.text(0.08, 0.94, f'{name_full} ({ticker}) — {period_text} Price Movement', color=text_color, fontsize=16, fontweight='bold', ha='left')
        fig.text(0.08, 0.90, f'Historical daily closing prices indicating recent trend and current price', color=text_color, fontsize=11, alpha=0.8, ha='left')

        watermark_text = f"Generated {datetime.now().strftime('%Y-%m-%d')} · Data: yfinance"
        fig.text(0.92, 0.05, watermark_text, color='#a0a0a0', fontsize=9, ha='right', va='center')
        
        base_folder = (PROJECT_DIR.parent / 'stefanutti-stocks' / 'generated' / 'figures') if ticker.startswith('SSK') else FIGURES_DIR
        os.makedirs(base_folder, exist_ok=True)
        out_path = f'{base_folder}/{ticker.split(".")[0]}_{period}_movement_{theme["name"]}.png'
        plt.savefig(out_path, facecolor=bg_color, bbox_inches='tight', dpi=800, edgecolor='#000000')
        plt.close(fig)
        print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    plot_stock("CGR.JO", "3mo", "Calgro M3 Holdings", current_price_override=430.0)
    plot_stock("CGR.JO", "6mo", "Calgro M3 Holdings", current_price_override=430.0)
    plot_stock("SSK.JO", "3mo", "Stefanutti Stocks")
    plot_stock("SSK.JO", "6mo", "Stefanutti Stocks")
