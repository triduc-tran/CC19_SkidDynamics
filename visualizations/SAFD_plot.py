import matplotlib.pyplot as plt
from pathlib import Path
from physics_model import compute_coasting_acceleration, compute_critical_speed
import numpy as np

def plot_safd(safd_results_list, parameters, mu_values):
    """
    Plot SAFD boundary curves for multiple friction coefficients
    :param safd_results_list: list of dicts - one dict per mu value
    :param parameters: dict - simulation parameters from initial_state.json
    :param mu_values: list - values of friction coefficients used
    :return:  none (saves image 'safd_plot.png' to disk)
    """

    fig, ax = plt.subplots(figsize=(10,7))
    colors = ("red", "orange", "green", "blue")
    labels = (f"μ = {mu_values[0]} (black ice)",
              f"μ = {mu_values[1]} (wet ice)",
              f"μ = {mu_values[2]} (packed ice)",
              f"μ = {mu_values[3]} (rough ice)")
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
    ax.axvline(v_crit, linestyle="--",color="purple", label="Critical speed (F_y = 0)")
    ax.plot(v_line, a_coast, linestyle="--", color="magenta", label="Coasting (F_x = 0)")
    ax.set_xlabel("Velocity v (m/s)", fontsize=12)
    ax.set_ylabel("Longitudinal acceleration a_x (m/s²)", fontsize=12)
    ax.set_title("Speed - Acceleration Feasible Domain (SAFD)\n on Icy Curved Ramps", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(fontsize=10)

    output_path = Path(__file__).parent / "safd_plot.png"
    plt.savefig(output_path, dpi = 300, bbox_inches = 'tight')
    plt.close()