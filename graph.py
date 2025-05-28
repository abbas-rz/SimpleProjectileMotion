import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from qbstyles import mpl_style # Correct import for qbstyles

# Apply the qbstyles dark theme - this sets the foundational dark mode
mpl_style(dark=True)

# NASA-inspired color palette (can be customized further)
# These colors are chosen for good contrast on a dark background and a "space" feel.
NASA_COLORS = {
    "blue": "#6495ED",       # Cornflower Blue - for primary data lines
    "light_blue": "#90CAF9", # Lighter Blue - for secondary data or displacement
    "orange": "#FFA000",     # Amber/Orange - for contrasting data lines (e.g., Velocity Y)
    "teal": "#4DD0E1",       # Teal - for energy or other distinct metrics
    "light_grey": "#E0E0E0", # Light Grey/White - for trajectories or neutral lines
    "accent_yellow": "#FFD700", # Gold/Yellow - for start markers
    "accent_red": "#FF6347",    # Tomato Red - for end markers
    "text_main": "white",
    "text_secondary": "lightgrey",
    "grid_line": "gray",
    "spine_color": "gray",
    "annotation_bg": "#1A1A1A" # Slightly off-black for annotation boxes
}

def calculate_kinetic_energy(vx: float, vy: float, mass: float = 1.0) -> float:
    """Calculate kinetic energy: KE = 0.5 * m * v²"""
    return 0.5 * mass * (vx**2 + vy**2)

def calculate_displacement(x: float, y: float, initial_x: float, initial_y: float) -> float:
    """Calculate total displacement from initial position"""
    return np.sqrt((x - initial_x)**2 + (y - initial_y)**2)

def load_data(csv_filename: str) -> pd.DataFrame | None:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(csv_filename)
        print(f"Loaded {len(df)} data points from {csv_filename}")
        return df
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_filename}")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

def plot_data(ax, x_data, y_data, title, xlabel, ylabel, color, marker=None, legend_label=None, linewidth=1.5):
    """Helper function to plot data on a given axes with NASA-inspired minimalist styling."""
    ax.plot(x_data, y_data, color=color, linewidth=linewidth, marker=marker, markersize=4 if marker else 0, label=legend_label) # Smaller markers if used
    ax.set_title(title, fontsize=12, fontweight='normal', color=NASA_COLORS["text_main"]) # Slightly smaller, normal weight for subplot titles
    ax.set_xlabel(xlabel, fontsize=10, color=NASA_COLORS["text_secondary"])
    ax.set_ylabel(ylabel, fontsize=10, color=NASA_COLORS["text_secondary"])

    # qbstyles handles tick colors, but we ensure consistency if needed
    ax.tick_params(colors=NASA_COLORS["text_secondary"], labelsize=9)

    # Minimalist grid
    ax.grid(True, linestyle=':', alpha=0.3, color=NASA_COLORS["grid_line"])

    # Cleaner spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(NASA_COLORS["spine_color"])
    ax.spines['bottom'].set_color(NASA_COLORS["spine_color"])

    if legend_label:
        ax.legend(fontsize=9, facecolor=NASA_COLORS["annotation_bg"], edgecolor=NASA_COLORS["grid_line"], labelcolor=NASA_COLORS["text_secondary"], framealpha=0.7)


def generate_physics_graphs(csv_filename: str, save_plots: bool = True):
    """
    Generate physics graphs from CSV data with a professional, minimalist, NASA-inspired dark theme.
    """
    df = load_data(csv_filename)
    if df is None:
        return

    time = df['Time'].values
    x_pos = df['X_Position'].values
    y_pos = df['Y_Position'].values
    vx = df['Velocity_X'].values
    vy = df['Velocity_Y'].values

    initial_x, initial_y = x_pos[0], y_pos[0]
    kinetic_energy = np.array([calculate_kinetic_energy(vx[i], vy[i]) for i in range(len(vx))])
    displacement = np.array([calculate_displacement(x_pos[i], y_pos[i], initial_x, initial_y) for i in range(len(x_pos))])

    fig, axes = plt.subplots(2, 2, figsize=(12, 9)) # Slightly adjusted figsize for better proportions
    fig.suptitle(f'Projectile Motion Analysis: {os.path.basename(csv_filename)}', fontsize=15, fontweight='bold', color=NASA_COLORS["text_main"])
    # qbstyles should set the fig facecolor, ensure it's dark. If needed: fig.set_facecolor('#0a0f1a')

    ax1, ax2, ax3, ax4 = axes.flatten()

    # Common text annotation style
    annotation_bbox_style = dict(boxstyle='round,pad=0.3', facecolor=NASA_COLORS["annotation_bg"], alpha=0.6, edgecolor=NASA_COLORS["grid_line"])
    annotation_text_color = NASA_COLORS["text_secondary"]
    annotation_fontsize = 8

    # 1. Kinetic Energy vs Time
    plot_data(ax1, time, kinetic_energy, 'Kinetic Energy vs Time', 'Time (s)', 'Kinetic Energy (J)', NASA_COLORS["teal"])
    ax1.text(0.03, 0.97, f'Max KE: {kinetic_energy.max():.2f} J\nMin KE: {kinetic_energy.min():.2f} J',
             transform=ax1.transAxes, verticalalignment='top', color=annotation_text_color,
             bbox=annotation_bbox_style, fontsize=annotation_fontsize)

    # 2. Trajectory (Y vs X)
    plot_data(ax2, x_pos, y_pos, 'Trajectory (Y vs X Position)', 'X Position (m)', 'Y Position (m)', NASA_COLORS["light_grey"])
    # ax2.scatter(x_pos[0], y_pos[0], color=NASA_COLORS["accent_yellow"], s=60, marker='o', label='Start', zorder=5, edgecolors='black', linewidth=0.5)
    # ax2.scatter(x_pos[-1], y_pos[-1], color=NASA_COLORS["accent_red"], s=60, marker='s', label='End', zorder=5, edgecolors='black', linewidth=0.5)
    ax2.set_aspect('equal', adjustable='box')
    ax2.legend(fontsize=9, facecolor=NASA_COLORS["annotation_bg"], edgecolor=NASA_COLORS["grid_line"], labelcolor=NASA_COLORS["text_secondary"], framealpha=0.7)
    ax2.text(0.03, 0.97, f'Max Height: {y_pos.max():.2f} m\nRange: {x_pos.max() - x_pos.min():.2f} m',
             transform=ax2.transAxes, verticalalignment='top', color=annotation_text_color,
             bbox=annotation_bbox_style, fontsize=annotation_fontsize)

    # 3. Velocity Components vs Time
    plot_data(ax3, time, vx, 'Velocity Components vs Time', 'Time (s)', 'Velocity (m/s)', NASA_COLORS["blue"], legend_label='Velocity X')
    # For the second plot on the same axis, we don't want to repeat title and labels
    ax3.plot(time, vy, color=NASA_COLORS["orange"], linewidth=1.5, label='Velocity Y')
    ax3.axhline(y=0, color=NASA_COLORS["grid_line"], linestyle='--', alpha=0.5)
    ax3.legend(fontsize=9, facecolor=NASA_COLORS["annotation_bg"], edgecolor=NASA_COLORS["grid_line"], labelcolor=NASA_COLORS["text_secondary"], framealpha=0.7)
    ax3.text(0.03, 0.97, f'Vx (initial): {vx[0]:.2f} m/s\nVy range: [{vy.min():.2f}, {vy.max():.2f}] m/s',
             transform=ax3.transAxes, verticalalignment='top', color=annotation_text_color,
             bbox=annotation_bbox_style, fontsize=annotation_fontsize)

    # 4. Total Displacement vs Time
    plot_data(ax4, time, displacement, 'Displacement from Origin vs Time', 'Time (s)', 'Displacement (m)', NASA_COLORS["light_blue"])
    ax4.text(0.03, 0.97, f'Max Disp: {displacement.max():.2f} m\nFinal Disp: {displacement[-1]:.2f} m',
             transform=ax4.transAxes, verticalalignment='top', color=annotation_text_color,
             bbox=annotation_bbox_style, fontsize=annotation_fontsize)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    if save_plots:
        output_filename = f"{os.path.splitext(csv_filename)[0]}_analysis_nasa_themed.png"
        # Ensure the figure facecolor from qbstyles is used for saving
        plt.savefig(output_filename, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
        print(f"Graphs saved as: {output_filename}")

    plt.show()
    display_summary_statistics(time, x_pos, y_pos, vx, vy, kinetic_energy, displacement)


def display_summary_statistics(time, x_pos, y_pos, vx, vy, kinetic_energy, displacement):
    """Prints a summary of the physics analysis."""
    print("\n" + "=" * 50)
    print("PHYSICS ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Simulation Duration: {time[-1]:.3f} seconds")
    print(f"Data Points: {len(time)}")
    print(f"Initial Position: ({x_pos[0]:.3f}, {y_pos[0]:.3f}) m")
    print(f"Final Position: ({x_pos[-1]:.3f}, {y_pos[-1]:.3f}) m")
    print(f"Initial Velocity: ({vx[0]:.3f}, {vy[0]:.3f}) m/s")
    print(f"Final Velocity: ({vx[-1]:.3f}, {vy[-1]:.3f}) m/s")
    print(f"Maximum Height: {y_pos.max():.3f} m")
    print(f"Range: {x_pos.max() - x_pos.min():.3f} m")
    print(f"Maximum Kinetic Energy: {kinetic_energy.max():.3f} J")
    print(f"Minimum Kinetic Energy: {kinetic_energy.min():.3f} J")
    print(f"Maximum Displacement: {displacement.max():.3f} m")
    print("=" * 50)


def find_latest_csv() -> str | None:
    """Find the most recent projectile data CSV file."""
    csv_files = glob.glob("projectile_data_*.csv")
    if not csv_files:
        print("No projectile data CSV files found in the current directory.")
        return None
    return max(csv_files, key=os.path.getmtime)

def get_csv_filename_from_user(latest_csv: str | None) -> str:
    """Prompts the user for a CSV filename, offering the latest found file as default."""
    if latest_csv:
        use_latest = input(f"Found latest CSV file: '{latest_csv}'. Use this file? (y/n, default=y): ").strip().lower()
        if use_latest in ('y', ''):
            return latest_csv
    
    filename = input("Enter the CSV filename (e.g., 'data.csv'): ").strip()
    return filename if filename.endswith('.csv') else f"{filename}.csv"


def main():
    """Main function to run the graph generator."""
    print("--- Physics Graph Generator (NASA Themed) ---")
    latest_csv = find_latest_csv()
    csv_file = get_csv_filename_from_user(latest_csv)
    generate_physics_graphs(csv_file, save_plots=True)


if __name__ == "__main__":
    main()