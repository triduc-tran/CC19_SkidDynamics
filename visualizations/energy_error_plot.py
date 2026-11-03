import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
from pathlib import Path


def plot_energy_error(results_df, parameters):
    """
    Plot the fractional energy variation / numerical stability over time
    :param results_df: pandas Dataframe from run_simulation
    :param parameters: dict - parameters imported from initial_state.json
    :return: None (saves 'energy_error_plot.png' to disk)
    """

    t = results_df["time_s"]
    E = results_df["mechanical_energy_J"]
    E0 = E.iloc[0]

    fractional_error_percent = np.abs((E - E0) / E0) * 100

    fig, ax = plt.subplots(figsize = (8, 4.5))
    ax.plot(t, fractional_error_percent, color ="crimson", linewidth = 2, label ="Relative Energy Variation")
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.ticklabel_format(axis = "y", style = "plain")
    ax.set_xlabel("Simulation Time t (s)", fontsize = 11)
    ax.set_ylabel("Mechanical Energy Error (%)", fontsize = 11)
    ax.set_title("Numerical Energy Conservation & Dissipation\n(RK45 Integrator Stability)", fontsize = 12)
    ax.grid(True, which = "both", linestyle = "--", alpha = 0.5)
    ax.legend(loc = "upper left", fontsize = 10)
    plt.tight_layout()

    output_path = Path(__file__).parent / "energy_error_plot.png"
    plt.savefig(output_path, dpi = 300, bbox_inches = "tight")
    plt.close()

