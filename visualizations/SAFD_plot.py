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
    colors = plt.cm.coolwarm(np.linspace(0, 0.95, len(mu_values)))
    mu_names = {"0.01": "(black ice)",
                "0.05": "(wet ice)",
                "0.15": "(packed ice)",
                "0.20": "(rough ice)"}

    highlighted_mu = parameters["simulation"]["highlight_mu"]
    idx = mu_values.index(highlighted_mu)
    chosen = safd_results_list[idx]

    for i, (safd_data, color) in enumerate(zip(safd_results_list, colors)):
        mu = mu_values[i]
        key = f"{mu:.2f}"
        name = mu_names.get(key, "")
        label = f"μ = {key} {name}"
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

    ax.contourf(chosen["v"], chosen["a_x"], chosen["mu_margin"], levels = [-100, 0, 100], colors = ["lightcoral", "lightgreen"], alpha = 0.3)
    ax.axvline(v_crit, linestyle = "--",color = "turquoise", label = "Critical speed (F_y = 0)")
    ax.plot(v_line, a_coast, linestyle = "--", color = "magenta", label = "Coasting (F_x = 0)")
    ax.set_xlabel("Velocity v (m/s)", fontsize = 12)
    ax.set_ylabel("Longitudinal acceleration a_x (m/s²)", fontsize = 12)
    ax.set_title("Speed - Acceleration Feasible Domain (SAFD)\n on Icy Curved Ramps", fontsize = 14)
    ax.grid(True, linestyle = '--', alpha = 0.5)
    ax.annotate("SAFD boundary (μ_margin = 0)", xy = (10.8, 0.5), xytext = (12, 1.5), arrowprops = dict(arrowstyle="->"))
    feasible_patch = Patch(facecolor = "lightgreen", alpha = 0.4, label =f"Feasible, μ_margin > 0 (μ = {highlighted_mu:.2f})")
    infeasible_patch = Patch(facecolor ="lightcoral", alpha = 0.4, label =f"Infeasible, μ_margin < 0 (μ = {highlighted_mu:.2f})")
    handles, name = ax.get_legend_handles_labels()
    handles = handles + [feasible_patch, infeasible_patch]
    ax.legend(handles = handles, fontsize = 10)

    output_path = Path(__file__).parent / "safd_plot.png"
    plt.savefig(output_path, dpi = 300, bbox_inches = 'tight')
    plt.close()