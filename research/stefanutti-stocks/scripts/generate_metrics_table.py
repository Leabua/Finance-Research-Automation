from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import matplotlib.pyplot as plt
import os

def create_metrics_table():
    bg_color = '#ffffff'
    text_color = '#000000'
    
    # 1200 DPI, with thinner black border
    # Height adjusted for 4 rows
    fig, ax = plt.subplots(figsize=(10, 2.6), dpi=1200, facecolor=bg_color, edgecolor='#000000', linewidth=1.5)
    ax.set_facecolor(bg_color)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Data rows (4 columns) - Transcribed from Stefanutti Stocks (SSK) Key Metrics image
    headers = [
        ["MARKET PRICE", "TANGIBLE NAV/SHARE", "PRICE / TANGIBLE NAV", "EV/EBITDA (Reported)"],
        ["TOTAL DEBT", "NET CASH", "NET DEBT / EBITDA", "INTEREST COVERAGE"],
        ["CURRENT RATIO", "QUICK RATIO", "SECURED ORDER BOOK", "ORDER BOOK / TOTAL ASSETS"],
        ["HEADLINE P/E RATIO", "OPERATING MARGIN", "EBITDA MARGIN", "RETURN ON EQUITY"]
    ]
    
    values = [
        ["715 ZAc", "191.8 ZAc", "3.73x", "0.89x"],
        ["R667.6m", "R441.5m", "-0.52x", "4.51x"],
        ["0.97x", "0.80x", "R17.20bn", "3.00x"],
        ["1.99x", "8.8%", "10.9%", "104.4%"]
    ]
    
    x_pos = [0.02, 0.27, 0.52, 0.77]
    y_start = 0.82
    y_step = 0.22
    
    # Warning/Highlight color for key metrics (valuation premium, tight liquidity)
    warning_color = '#854F0B'
    
    for row in range(4):
        y_h = y_start - row * y_step
        y_v = y_h - 0.08
            
        for col in range(4):
            ax.text(x_pos[col], y_h, headers[row][col], fontsize=8, fontfamily='sans-serif', color='#111111', fontweight='bold', ha='left')
            
            val = values[row][col]
            v_color = text_color
            
            # Formatting logic: highlight tight current/quick ratios and key valuation metric
            if (row == 2 and col == 0) or (row == 2 and col == 1) or (row == 0 and col == 2):
                v_color = warning_color
                
            ax.text(x_pos[col], y_v, val, fontsize=12, fontfamily='sans-serif', color=v_color, fontweight='bold', ha='left')

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURES_DIR / 'ssk_key_metrics_table.png'
    plt.savefig(out_path, facecolor=bg_color, bbox_inches='tight', dpi=1200, edgecolor='#000000')
    plt.close(fig)
    print(f"Successfully generated {out_path}")

if __name__ == '__main__':
    create_metrics_table()
