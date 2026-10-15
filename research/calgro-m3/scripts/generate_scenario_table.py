from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import matplotlib.pyplot as plt
import os

def create_scenario_table():
    bg_color = '#ffffff'
    
    # 1200 DPI
    fig, ax = plt.subplots(figsize=(5.5, 2.2), dpi=1200, facecolor=bg_color)
    ax.axis('off')
    
    headers = ["SCENARIO", "TERMINAL PRICE", "RETURN FROM CURRENT"]
    values = [
        ["P10 - Bear", "241 ZAc", "-44%"],
        ["P25", "364 ZAc", "-15%"],
        ["P50 - Base", "557 ZAc", "+29%"],
        ["P75", "853 ZAc", "+98%"],
        ["P90 - Bull", "1,265 ZAc", "+194%"]
    ]
    
    # Use Matplotlib's built-in table for perfect grid lines and column spacing
    table = ax.table(cellText=values, colLabels=headers, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.2) # Stretch rows to maintain good vertical spacing
    
    # Customize cells
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#000000') # Thin black lines
        cell.set_linewidth(0.8)
        
        text = cell.get_text()
        text.set_fontfamily('sans-serif')
        text.set_fontweight('bold')
        
        if row == 0:
            # Header styling
            text.set_fontsize(9)
            text.set_color('#111111')
            cell.set_facecolor('#f8f9fa') # Extremely subtle off-white for headers
        else:
            # Data row styling
            val = values[row-1][col]
            v_color = '#000000'
            
            # Color logic
            if "Bear" in val or "-" in val:
                v_color = '#A32D2D' # Red
            elif "Base" in val:
                v_color = '#185FA5' # Blue
            elif "Bull" in val or "+" in val:
                v_color = '#0F6E56' # Green
                
            # Neutralize P25 and P75 labels
            if col == 0 and val in ["P25", "P75"]:
                v_color = '#000000'
                
            text.set_color(v_color)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = FIGURES_DIR / 'cgr_scenario_table.png'
    # Tight bounding box to snap exactly to the table's edges
    plt.savefig(out_path, facecolor=bg_color, bbox_inches='tight', dpi=1200)
    plt.close(fig)
    print(f"Successfully generated {out_path}")

if __name__ == '__main__':
    create_scenario_table()
