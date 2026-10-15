from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import matplotlib.pyplot as plt
import os

def create_header_table():
    bg_color = '#ffffff'
    text_color = '#000000'
    grid_color = '#e2e8f0'
    
    # 1200 DPI, with thinner black border
    # Height reduced to 3.8 to remove empty space left by the removed title
    fig, ax = plt.subplots(figsize=(10, 3.8), dpi=1200, facecolor=bg_color, edgecolor='#000000', linewidth=1.5)
    ax.set_facecolor(bg_color)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Data rows (4 columns)
    headers = [
        ["TICKER", "SECTOR", "MARKET CAP", "RECOMMENDATION"],
        ["CURRENT PRICE", "TANGIBLE NAV/SHARE", "DISCOUNT TO NAV", "TIME HORIZON"],
        ["52-WEEK HIGH", "52-WEEK LOW", "P/E RATIO", "EV/EBITDA"],
        ["EPS (FY2026)", "NET DEBT", "NET DEBT / EBITDA", "INTEREST COVERAGE"]
    ]
    
    values = [
        ["CGR | JSE", "Real Estate", "~R480m", "BUY"],
        ["430 ZAc", "1,262 ZAc", "65.9%", "3–5 Years"],
        ["570 ZAc", "417 ZAc", "2.57x", "11.79x"],
        ["167.4 ZAc", "R1.20bn", "5.77x", "3.93x"]
    ]
    
    x_pos = [0.02, 0.27, 0.52, 0.77]
    y_start = 0.90
    y_step = 0.17
    
    for row in range(4):
        y_h = y_start - row * y_step
        y_v = y_h - 0.05
            
        for col in range(4):
            ax.text(x_pos[col], y_h, headers[row][col], fontsize=8, fontfamily='sans-serif', color='#111111', fontweight='bold', ha='left')
            
            val = values[row][col]
            v_color = text_color
            
            # Formatting logic
            if val == "BUY": v_color = '#0F6E56'
            elif "CGR" in val and "JSE" in val: v_color = text_color
            elif "65.9%" in val or "5.77x" in val: v_color = '#854F0B'
                
            ax.text(x_pos[col], y_v, val, fontsize=12, fontfamily='sans-serif', color=v_color, fontweight='bold', ha='left')

    # Probabilistic targets row (4 columns)
    row_idx = 4
    y_h = y_start - row_idx * y_step
    y_v = y_h - 0.05
    
    # Divider for prob targets
    ax.plot([0.02, 0.98], [y_h + 0.07, y_h + 0.07], color=grid_color, lw=1)
    ax.text(0.02, y_h + 0.03, "PROBABILISTIC PRICE TARGETS - 36-MONTH MONTE CARLO (1,000 PATHS)", fontsize=8, fontfamily='sans-serif', color='#111111', fontweight='bold', ha='left')
    y_h -= 0.02
    y_v -= 0.02
    
    prob_headers = ["P10 - BEAR CASE", "P50 - BASE CASE", "P75 - TARGET", "P90 - BULL CASE"]
    prob_values = ["241 ZAc", "557 ZAc", "853 ZAc", "1,265 ZAc"]
    
    for col in range(4):
        ax.text(x_pos[col], y_h, prob_headers[col], fontsize=8, fontfamily='sans-serif', color='#111111', fontweight='bold', ha='left')
        
        v_color = text_color
        if col == 0: v_color = '#A32D2D'
        elif col == 1: v_color = '#185FA5'
        elif col == 2 or col == 3: v_color = '#3B6D11'
            
        ax.text(x_pos[col], y_v, prob_values[col], fontsize=12, fontfamily='sans-serif', color=v_color, fontweight='bold', ha='left')

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURES_DIR / 'cgr_research_header_table.png'
    plt.savefig(out_path, facecolor=bg_color, bbox_inches='tight', dpi=1200, edgecolor='#000000')
    plt.close(fig)
    print(f"Successfully generated {out_path}")

if __name__ == '__main__':
    create_header_table()
