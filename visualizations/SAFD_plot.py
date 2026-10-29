import matplotlib.pyplot as plt
from pathlib import Path
from physics_model import compute_coasting_acceleration, compute_critical_speed
import numpy as np
from matplotlib.patches import Patch

def plot_safd(safd_results_list, parameters, mu_values):
    """
    Plot SAFD boundary curves for multiple friction coefficients
    :param safd_results_list: list of dicts - one dict per mu value
    :param parameters: dict - simulation parameters from initial_state.json
    :param mu_values: list - values of friction coefficients used
    :return:  none (saves image 'safd_plot.png' to disk)
    """

    fig, ax = plt.subplots(figsize=(10,7))
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(mu_values)))
    labels = (f"μ = {mu_values[0]:.2f} (black ice)",
              f"μ = {mu_values[1]:.2f} (wet ice)",
              f"μ = {mu_values[2]:.2f} (packed ice)",
              f"μ = {mu_values[3]:.2f} (rough ice)")
    for (safd_data, color, label) in zip(safd_results_list, colors, labels):
        v_grid = safd_data["v"]
        acceleration_grid = safd_data["a_x"]
        mu_margin = safd_data["mu_margin"]

        ax.contour(v_grid, acceleration_grid, mu_margin,
                             levels=[0],
                             colors=[color],
                             linewidths=2)
        ax.plot([],[], color=color, label=label)

    v_line = safd_results_list[0]["v"][0,:]
    v_crit = compute_critical_speed(parameters)
    a_coast = compute_coasting_acceleration(v_line, parameters)

    x = v_crit / 2
    y = 0.85 * parameters["simulation"]["accel_range_m_s2"][0]
    ax.text(x, y, "B", ha = "left", va = "center", fontsize = 13, fontweight='bold')

    x = 0.7 * parameters["simulation"]["speed_range_m_s"][1]
    y = 0
    ax.text(x, y , "A", ha = "center", va = "top", fontsize = 13, fontweight='bold')

    x = v_crit / 2
    y = compute_coasting_acceleration(x, parameters)
    ax.text(x, y + 0.17, "B'", ha = "center", va = "center", fontsize = 13, fontweight = "bold",
            bbox=dict(boxstyle = "round", facecolor = "white", alpha = 0.7))

    x = v_crit * 1.2
    y = compute_coasting_acceleration(x, parameters)
    ax.text(x, y + 0.17, "A'", ha = "center", va = "center", fontsize = 13, fontweight = "bold",
            bbox=dict(boxstyle = "round", facecolor = "white", alpha = 0.7))

    ax.contourf(v_grid, acceleration_grid, mu_margin, levels = [-100, 0, 100], colors = ["lightcoral", "lightgreen"], alpha = 0.3)
    ax.axvline(v_crit, linestyle = "--",color = "turquoise", label = "Critical speed (F_y = 0)")
    ax.plot(v_line, a_coast, linestyle = "--", color = "magenta", label = "Coasting (F_x = 0)")
    ax.set_xlabel("Velocity v (m/s)", fontsize = 12)
    ax.set_ylabel("Longitudinal acceleration a_x (m/s²)", fontsize = 12)
    ax.set_title("Speed - Acceleration Feasible Domain (SAFD)\n on Icy Curved Ramps", fontsize = 14)
    ax.grid(True, linestyle = '--', alpha = 0.5)
    ax.legend(fontsize=10)
    ax.annotate("SAFD boundary (μ_margin = 0)", xy = (10.8, 0.5), xytext = (12, 1.5), arrowprops = dict(arrowstyle="->"))
    Patch(facecolor = "lightgreen", alpha = 0.4, label = "Feasible, μ_margin > 0 (μ = 0.20)")
    Patch(facecolor="lightcoral", alpha=0.4, label="Infeasible, μ_margin < 0 (μ = 0.20)")


    output_path = Path(__file__).parent / "safd_plot.png"
    plt.savefig(output_path, dpi = 300, bbox_inches = 'tight')
    plt.close()