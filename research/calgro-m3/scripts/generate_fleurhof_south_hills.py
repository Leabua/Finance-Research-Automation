from config import DATA_DIR, FIGURES_DIR, GENERATED_DIR, PROJECT_DIR
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
from scipy.interpolate import PchipInterpolator

# =====================================================================
# >>>>> USER ASSUMPTION DATA: MODIFY THESE VALUES AS TIME PASSES <<<<<
# =====================================================================
years = np.array([2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035])
inflows = np.array([834486, 1001383, 1084832, 1168280, 1084832, 917935, 751037, 584140, 500692, 417243])
outflows = np.array([-735274, -868719, -940738, -1012284, -947576, -812304, -675577, -538241, -456851, -389096])
cumulative = np.array([99212, 231876, 375971, 531966, 669222, 774853, 850313, 896211, 940052, 968199])
# =====================================================================
# >>>>>>>>>>>>>>>>>>>>>>>>> END OF USER DATA <<<<<<<<<<<<<<<<<<<<<<<<<<
# =====================================================================

# X-axis ticks: use full four-digit year numbers (no FY prefix)
labels = [str(y) for y in years]

# Interpolation for high fidelity smoothing (Piecewise Cubic Hermite Interpolating Polynomial)
x_smooth = np.linspace(years[0], years[-1], 300)
pchip = PchipInterpolator(years, cumulative)
y_smooth = pchip(x_smooth)

# Mathematical exact zero-crossing for break-even
cross_idx = -1
for i in range(1, len(cumulative)):
    if cumulative[i-1] < 0 and cumulative[i] >= 0:
        cross_idx = i
        break

if cross_idx != -1:
    y_prev = cumulative[cross_idx - 1]
    y_curr = cumulative[cross_idx]
    pct = (0 - y_prev) / (y_curr - y_prev)
    x_cross = years[cross_idx - 1] + pct * (years[cross_idx] - years[cross_idx - 1])
    # The whole year in which cumulative cashflow turns positive
    be_whole_year = years[cross_idx]
else:
    x_cross = None
    be_whole_year = None

# Custom currency formatter
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

# Define phases and their boundary dividers
phases = [
    (2025.5, 2028.5, "DELIVER"),
    (2028.5, 2030.5, "PEAK"),
    (2030.5, 2031.5, "DECLINE"),
    (2031.5, 2035.5, "TAIL")
]

def render_chart(is_dark):
    # Styling colors
    if is_dark:
        bg_color = '#121212'
        text_color = '#ffffff'
        sub_text = '#a0a0a0'
        grid_color = '#262626'           # Consistent solid dark grey gridline
        zero_line_color = '#404040'       # Axis line dark grey
        border_color = '#2d2d2d'          # Spine/divider color
        line_color = '#1D9E75'            # Line color
        break_even_color = '#3b82f6'      # Nice, highly legible bright blue for break even!
        break_even_border = '#121212'
        
        # Max fill opacities
        max_alpha_pos = 0.50
        max_alpha_neg = 0.25
        inflow_bar_color = (29/255, 158/255, 117/255, 0.85)
        outflow_bar_color = (226/255, 75/255, 74/255, 0.85)
    else:
        bg_color = '#ffffff'
        text_color = '#000000'            # Pure black for maximum contrast
        sub_text = '#222222'              # Very dark grey for subtext
        grid_color = '#e2e8f0'           # Consistent solid light grey gridline
        zero_line_color = '#000000'       # Axis line black
        border_color = '#000000'          # Spine/divider color black
        line_color = '#1D9E75'            # Line color
        break_even_color = '#1d4ed8'      # Nice, highly legible rich dark blue for break even!
        break_even_border = '#ffffff'
        
        # Max fill opacities
        max_alpha_pos = 0.50
        max_alpha_neg = 0.25
        inflow_bar_color = (29/255, 158/255, 117/255, 0.85)
        outflow_bar_color = (226/255, 75/255, 74/255, 0.85)

    # Create a single subplot, beautifully proportioned
    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=800, facecolor=bg_color, edgecolor='#000000', linewidth=3)
    ax.set_facecolor(bg_color)

    # Put gridlines behind the bars
    ax.set_axisbelow(True)

    # Set exact vertical scale bounds to leave a designated "buffer zone" at the very bottom
    # for phase labels. Minimum outflow is -1.01B. Setting min to -1.5B leaves ~500M of bottom spacing.
    ymin, ymax = -1500000, 1500000
    ax.set_ylim(ymin, ymax)

    # 1. Plot Phase vertical dividers (subtle dashed lines spanning the entire grid)
    for start, end, label in phases:
        if start > 2025.5:
            ax.axvline(x=start, color=border_color, linestyle='--', linewidth=0.6, zorder=1)

    # 2. Render Phase Text Labels inside the grid but completely below all data plots
    # Plotted at y = -1250000. Outflows end at -1.01B, leaving coordinate padding above and below.
    y_phase_label = -1250000
    for start, end, label in phases:
        mid_x = (start + end) / 2
        ax.text(mid_x, y_phase_label, label, color=sub_text, fontsize=9, 
                fontweight='bold', ha='center', va='center', alpha=0.8, zorder=2)

    # 3. Plot Side-by-Side Inflow & Outflow Bars
    bar_width = 0.32
    ax.bar(years - bar_width/2, inflows, width=bar_width, color=inflow_bar_color, 
           edgecolor='none', label='Annual Inflow', zorder=3)
    ax.bar(years + bar_width/2, outflows, width=bar_width, color=outflow_bar_color, 
           edgecolor='none', label='Annual Outflow', zorder=3)

    # 4. Plot smoothed Cumulative FCF J-curve and multi-layered gradient shadow
    ax.plot(x_smooth, y_smooth, color=line_color, linewidth=2.5, label='Cumulative FCF', zorder=5)
    
    # Render non-linear vertical gradient fill that closely hugs the curve.
    # We use 15 layers with a power of 1.73.
    N_layers = 15
    teal_r, teal_g, teal_b = 29/255, 158/255, 117/255
    red_r, red_g, red_b = 226/255, 75/255, 74/255

    for k in range(1, N_layers + 1):
        f_low = (k - 1) / N_layers
        f_high = k / N_layers
        f_mid = (f_low + f_high) / 2
        
        # Calculate power-law alphas
        layer_alpha_pos = max_alpha_pos * (f_mid ** 1.73)
        layer_alpha_neg = max_alpha_neg * (f_mid ** 1.73)
        
        # Positive curve gradient fill (Teal)
        ax.fill_between(x_smooth, y_smooth * f_low, y_smooth * f_high, 
                        where=(y_smooth >= 0),
                        color=(teal_r, teal_g, teal_b, layer_alpha_pos), 
                        edgecolor='none', interpolate=True, zorder=4)
        
        # Negative curve gradient fill (Red)
        ax.fill_between(x_smooth, y_smooth * f_low, y_smooth * f_high, 
                        where=(y_smooth < 0),
                        color=(red_r, red_g, red_b, layer_alpha_neg), 
                        edgecolor='none', interpolate=True, zorder=4)

    # 5. Plot exact Break-Even intersection point
    if x_cross is not None:
        legend_label = f"Break-even ({be_whole_year})" if be_whole_year else "Break-even"
        ax.plot(x_cross, 0, marker='o', color=break_even_color, markersize=8, 
                markeredgecolor=break_even_border, markeredgewidth=1.5, 
                label=legend_label, zorder=6)

    # 6. Styling scales and baselines
    ax.axhline(0, color=zero_line_color, linewidth=1.2, zorder=2)
    ax.set_xlim(years[0] - 0.6, years[-1] + 0.6)
    
    # Configure main X-axis ticks
    ax.set_xticks(years)
    ax.set_xticklabels(labels, fontsize=9, color=sub_text)
    
    # Major ticks (labeled and gridlines) every 500,000 (0.5B)
    ax.yaxis.set_major_locator(MultipleLocator(500000))
    ax.yaxis.set_major_formatter(FuncFormatter(fmtR))
    
    # Minor ticks (gridlines only) every 250,000 (0.25B)
    ax.yaxis.set_minor_locator(MultipleLocator(250000))
    
    # Configure Y-axis tick mark visibility
    ax.tick_params(axis='y', which='major', colors=sub_text, labelsize=9)
    ax.tick_params(axis='y', which='minor', left=False)
    
    # Visual Gridline Hierarchy:
    ax.grid(axis='y', which='major', color=grid_color, linestyle='-', linewidth=0.6, zorder=1)
    ax.grid(axis='y', which='minor', color=grid_color, linestyle='-', linewidth=0.4, alpha=0.5, zorder=1)

    # 7. Make X and Y Axis Spines Distinct and Solid
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    ax.spines['left'].set_visible(True)
    ax.spines['left'].set_color(zero_line_color)
    ax.spines['left'].set_linewidth(1.0)
    
    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_color(zero_line_color)
    ax.spines['bottom'].set_linewidth(1.0)

    # 8. Set Axis Labels
    ax.set_xlabel("Financial Year", fontsize=10, fontweight='semibold', color=sub_text, labelpad=12)
    ax.set_ylabel("Yearly FCF's & Cumulative Flows", fontsize=10, fontweight='semibold', color=sub_text, labelpad=12)

    # 9. Title and Subtitle Alignment
    ax.set_title("Fleurhof, South Hills & Belhar — cumulative CGR FCF (R'000)", 
                 loc='left', fontsize=14, fontweight='bold', color=text_color, pad=32)
    
    ax.text(0.0, 1.04, "Active IRD Projects · Remaining revenue R8.3B · Pipeline scaled & extended to FY2035", 
            transform=ax.transAxes, fontsize=10, color=sub_text, ha='left', va='bottom')

    # Legend placement
    legend = ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=4, frameon=False)
    for text in legend.get_texts():
        text.set_color(sub_text)
        text.set_fontsize(9)

    plt.tight_layout()
    
    # Save the output PNG
    output_dir = str(FIGURES_DIR)
    os.makedirs(output_dir, exist_ok=True)
    suffix = "dark" if is_dark else "light"
    file_path = os.path.join(output_dir, f"fleurhof_south_hills_jcurve_{suffix}.png")
    plt.savefig(file_path, bbox_inches='tight', facecolor=bg_color, edgecolor='#000000')
    plt.close()
    print(f"Generated {file_path} successfully.")

if __name__ == "__main__":
    render_chart(is_dark=True)
    render_chart(is_dark=False)
