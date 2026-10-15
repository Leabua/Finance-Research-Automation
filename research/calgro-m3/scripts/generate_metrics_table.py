from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import matplotlib.pyplot as plt
import os

def create_metrics_table():
    bg_color = '#ffffff'
    text_color = '#000000'
    grid_color = '#e2e8f0'
    
    # 1200 DPI, with thinner black border
    # Height adjusted for 4 rows
    fig, ax = plt.subplots(figsize=(10, 2.6), dpi=1200, facecolor=bg_color, edgecolor='#000000', linewidth=1.5)
    ax.set_facecolor(bg_color)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Data rows (4 columns)
    headers = [
        ["MARKET PRICE", "TANGIBLE NAV/SHARE", "DISCOUNT TO NAV", "EV/EBITDA"],
        ["TOTAL DEBT", "NET DEBT", "NET DEBT / EBITDA", "INTEREST COVERAGE"],
        ["CURRENT RATIO", "QUICK RATIO", "DEV ASSETS", "DEV ASSETS / TOTAL"],
        ["P/E RATIO", "OPERATING MARGIN", "GROSS MARGIN", "RETURN ON EQUITY"]
    ]
    
    values = [
        ["430 ZAc", "1,262 ZAc", "65.9%", "11.79x"],
        ["R1.38bn", "R1.20bn", "5.77x", "3.93x"],
        ["2.02x", "0.87x", "R2.56bn", "69.5%"],
        ["2.57x", "19.1%", "27.2%", "10.7%"]
    ]
    
    x_pos = [0.02, 0.27, 0.52, 0.77]
    y_start = 0.82
    y_step = 0.22
    
    for row in range(4):
        y_h = y_start - row * y_step
        y_v = y_h - 0.08
            
        for col in range(4):
            ax.text(x_pos[col], y_h, headers[row][col], fontsize=8, fontfamily='sans-serif', color='#111111', fontweight='bold', ha='left')
            
            val = values[row][col]
            v_color = text_color
            
            # Formatting logic based on text context
            if "65.9%" in val or "5.77x" in val or "0.87x" in val:
                v_color = '#854F0B' # Warning color for elevated debt, high discount, tight quick ratio
                
            ax.text(x_pos[col], y_v, val, fontsize=12, fontfamily='sans-serif', color=v_color, fontweight='bold', ha='left')

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURES_DIR / 'cgr_key_metrics_table.png'
    plt.savefig(out_path, facecolor=bg_color, bbox_inches='tight', dpi=1200, edgecolor='#000000')
    plt.close(fig)
    print(f"Successfully generated {out_path}")

if __name__ == '__main__':
    create_metrics_table()
