from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy.interpolate import PchipInterpolator

# =====================================================================
# >>>>> USER ASSUMPTION DATA: MODIFY THESE VALUES AS TIME PASSES <<<<<
# =====================================================================
years = np.array([2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035])

bank_in = np.array([0, 0, 768000, 1152000, 1536000, 1728000, 2304000, 2496000, 2112000, 1920000])
bank_out = np.array([-145000, -80000, -699846, -1029770, -1361693, -1526654, -2027539, -2193501, -1857578, -1689616])

mem_in = np.array([105000, 117000, 127500, 135000, 142500, 150000, 150000, 150000, 150000, 150000])
mem_out = np.array([-68169, -77676, -85336, -91085, -94064, -96825, -94635, -91635, -88635, -85635])

other_in = np.array([834486, 1001383, 1084832, 1168280, 1084832, 917935, 751037, 584140, 500692, 417243])
other_out = np.array([-735274, -868719, -940738, -1012284, -947576, -812304, -675577, -538241, -456851, -389096])

cum_fcf = np.array([-8957, 83031, 337443, 659585, 1019583, 1379735, 1787020, 2193783, 2553412, 2876308])
# =====================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>> END OF USER DATA <<<<<<<<<<<<<<<<<<<<<<<<<<
# =====================================================================

labels = [str(y) for y in years]

# Interpolation for high fidelity smoothing
x_smooth = np.linspace(years[0], years[-1], 300)
pchip = PchipInterpolator(years, cum_fcf)
y_smooth = pchip(x_smooth)

# Break-even
cross_idx = -1
for i in range(1, len(cum_fcf)):
    if cum_fcf[i-1] < 0 and cum_fcf[i] >= 0:
        cross_idx = i
        break

if cross_idx != -1:
    y_prev = cum_fcf[cross_idx - 1]
    y_curr = cum_fcf[cross_idx]
    pct = (0 - y_prev) / (y_curr - y_prev)
    x_cross = years[cross_idx - 1] + pct * (years[cross_idx] - years[cross_idx - 1])
    be_whole_year = years[cross_idx]
else:
    x_cross = None
    be_whole_year = None

def fmtR(v, pos=None):
    if v == 0:
        return "R0"
    abs_v = abs(v)
    sign = '-' if v < 0 else ''
    if abs_v >= 1000000:
        return f"{sign}R{abs_v/1000000:.1f}B"
    elif abs_v >= 1000:
        return f"{sign}R{round(abs_v/1000)}M"
    else:
        return f"{sign}R{round(abs_v)}k"

def render_chart(is_dark):
    if is_dark:
        bg_color = '#121212'
        text_color = '#ffffff'
        sub_text = '#a0a0a0'
        grid_color = '#262626'
        zero_line_color = '#404040'
        border_color = '#2d2d2d'
        line_color = '#1D9E75'
        break_even_color = '#3b82f6'
        break_even_border = '#121212'
        
        alpha = 0.85
        max_alpha_pos = 0.50
        max_alpha_neg = 0.25
    else:
        bg_color = '#ffffff'
        text_color = '#000000'            # Pure black for maximum contrast
        sub_text = '#222222'              # Very dark grey for subtext
        grid_color = '#e2e8f0'           # Consistent solid light grey gridline
        zero_line_color = '#000000'       # Axis line black
        border_color = '#000000'          # Spine/divider color black
        line_color = '#1D9E75'
        break_even_color = '#1d4ed8'
        break_even_border = '#ffffff'
        
        alpha = 0.85
        max_alpha_pos = 0.50
        max_alpha_neg = 0.25

    # IN colors (Other, Memorial, Bankenveld) - Blue, Purple, Green
    c_in_1 = (59/255, 130/255, 246/255, alpha)   # Blue
    c_in_2 = (139/255, 92/255, 246/255, alpha)   # Purple
    c_in_3 = (29/255, 158/255, 117/255, alpha)   # Green
    
    # OUT colors (Other, Memorial, Bankenveld) - Yellow, Orange, Red
    c_out_1 = (251/255, 191/255, 36/255, alpha)  # Yellow
    c_out_2 = (249/255, 115/255, 22/255, alpha)  # Orange
    c_out_3 = (226/255, 75/255, 74/255, alpha)   # Red

    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=800, facecolor=bg_color, edgecolor='#000000', linewidth=3)
    ax.set_facecolor(bg_color)
    ax.set_axisbelow(True)

    # Set exact vertical scale bounds 
    ymin, ymax = -3500000, 4000000
    ax.set_ylim(ymin, ymax)

    # Plot Side-by-Side Inflow & Outflow Bars (Stacked)
    bar_width = 0.32
    
    # Inflows
    ax.bar(years - bar_width/2, other_in, width=bar_width, color=c_in_1, edgecolor='none')
    ax.bar(years - bar_width/2, mem_in, width=bar_width, bottom=other_in, color=c_in_2, edgecolor='none')
    ax.bar(years - bar_width/2, bank_in, width=bar_width, bottom=other_in + mem_in, color=c_in_3, edgecolor='none')

    # Outflows
    ax.bar(years + bar_width/2, other_out, width=bar_width, color=c_out_1, edgecolor='none')
    ax.bar(years + bar_width/2, mem_out, width=bar_width, bottom=other_out, color=c_out_2, edgecolor='none')
    ax.bar(years + bar_width/2, bank_out, width=bar_width, bottom=other_out + mem_out, color=c_out_3, edgecolor='none')

    # Cumulative FCF J-curve and gradient shadow
    ax.plot(x_smooth, y_smooth, color=line_color, linewidth=2.5, label='Cumulative FCF', zorder=5)
    
    N_layers = 15
    teal_r, teal_g, teal_b = 29/255, 158/255, 117/255
    red_r, red_g, red_b = 226/255, 75/255, 74/255

    for k in range(1, N_layers + 1):
        f_low = (k - 1) / N_layers
        f_high = k / N_layers
        f_mid = (f_low + f_high) / 2
        
        layer_alpha_pos = max_alpha_pos * (f_mid ** 1.73)
        layer_alpha_neg = max_alpha_neg * (f_mid ** 1.73)
        
        ax.fill_between(x_smooth, y_smooth * f_low, y_smooth * f_high, 
                        where=(y_smooth >= 0),
                        color=(teal_r, teal_g, teal_b, layer_alpha_pos), 
                        edgecolor='none', interpolate=True, zorder=4)
        
        ax.fill_between(x_smooth, y_smooth * f_low, y_smooth * f_high, 
                        where=(y_smooth < 0),
                        color=(red_r, red_g, red_b, layer_alpha_neg), 
                        edgecolor='none', interpolate=True, zorder=4)

    # Break-Even
    if x_cross is not None:
        legend_label = f"Break-even ({be_whole_year})" if be_whole_year else "Break-even"
        ax.plot(x_cross, 0, marker='o', color=break_even_color, markersize=8, 
                markeredgecolor=break_even_border, markeredgewidth=1.5, 
                label=legend_label, zorder=6)

    # Custom Legend Box in top left
    rect = patches.FancyBboxPatch((2025.45, 2350000), 2.45, 1450000,
                                  boxstyle="round,pad=0.05", 
                                  linewidth=1, edgecolor=border_color, facecolor=bg_color, zorder=6, alpha=0.9)
    ax.add_patch(rect)

    x_left = 2025.55
    x_in = 2027.25
    x_out = 2027.70

    y_header = 3550000
    y_bank = 3200000
    y_mem = 2850000
    y_other = 2500000

    ax.text(x_left, y_header, "Business segment", color=text_color, fontweight='bold', fontsize=9, va='center', zorder=7)
    ax.text(x_in, y_header, "IN", color=text_color, fontweight='bold', fontsize=9, va='center', ha='center', zorder=7)
    ax.text(x_out, y_header, "OUT", color=text_color, fontweight='bold', fontsize=9, va='center', ha='center', zorder=7)

    def plot_legend_row(y_pos, label, c_in, c_out):
        ax.text(x_left, y_pos, label, color=sub_text, fontsize=9, va='center', zorder=7)
        c_in_solid = (*c_in[:3], 1.0)
        c_out_solid = (*c_out[:3], 1.0)
        ax.scatter(x_in, y_pos, color=c_in_solid, s=60, zorder=7, edgecolor='none')
        ax.scatter(x_out, y_pos, color=c_out_solid, s=60, zorder=7, edgecolor='none')

    plot_legend_row(y_bank, "Bankenveld", c_in_3, c_out_3)
    plot_legend_row(y_mem, "Memorial Parks", c_in_2, c_out_2)
    plot_legend_row(y_other, "Other IRD", c_in_1, c_out_1)

    # Styling
    ax.axhline(0, color=zero_line_color, linewidth=1.2, zorder=2)
    ax.set_xlim(years[0] - 0.6, years[-1] + 0.6)
    
    ax.set_xticks(years)
    ax.set_xticklabels(labels, fontsize=9, color=sub_text)
    
    ax.yaxis.set_major_locator(MultipleLocator(1000000))
    ax.yaxis.set_major_formatter(FuncFormatter(fmtR))
    ax.yaxis.set_minor_locator(MultipleLocator(500000))
    
    ax.tick_params(axis='y', which='major', colors=sub_text, labelsize=9)
    ax.tick_params(axis='y', which='minor', left=False)
    
    ax.grid(axis='y', which='major', color=grid_color, linestyle='-', linewidth=0.6, zorder=1)
    ax.grid(axis='y', which='minor', color=grid_color, linestyle='-', linewidth=0.4, alpha=0.5, zorder=1)

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    ax.spines['left'].set_visible(True)
    ax.spines['left'].set_color(zero_line_color)
    ax.spines['left'].set_linewidth(1.0)
    
    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_color(zero_line_color)
    ax.spines['bottom'].set_linewidth(1.0)

    ax.set_xlabel("Financial Year", fontsize=10, fontweight='semibold', color=sub_text, labelpad=12)
    ax.set_ylabel("Yearly FCF's & Cumulative Flows", fontsize=10, fontweight='semibold', color=sub_text, labelpad=12)

    ax.set_title("Cumulative 10-year CGR Outlay", loc='left', fontsize=14, fontweight='bold', color=text_color, pad=32)
    ax.text(0.0, 1.04, "Combined Project Flows: Bankenveld, Memorial Parks, and Active IRD", transform=ax.transAxes, fontsize=10, color=sub_text, ha='left', va='bottom')

    legend = ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
    for text in legend.get_texts():
        text.set_color(sub_text)
        text.set_fontsize(9)

    plt.tight_layout()
    
    output_dir = str(FIGURES_DIR)
    os.makedirs(output_dir, exist_ok=True)
    suffix = "dark" if is_dark else "light"
    file_path = os.path.join(output_dir, f"combined_jcurve_{suffix}.png")
    plt.savefig(file_path, bbox_inches='tight', facecolor=bg_color, edgecolor='#000000')
    plt.close()
    print(f"Generated {file_path} successfully.")

if __name__ == "__main__":
    render_chart(is_dark=True)
    render_chart(is_dark=False)
