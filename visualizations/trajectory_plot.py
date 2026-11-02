import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def plot_trajectories(run_data, parameters):
    """
    Plot the trajectory of the vehicle in simulation
    :param run_data: dict -
    :param parameters: dict - simulation parameters from initial_state.json
    :return: none (saves image 'trajectory_plot.png' to disk)
    """
    fig, ax = plt.subplots(figsize=(10,6))
    lane_half_width_m = parameters["simulation"]["lane_half_width_m"]
    colors = plt.cm.coolwarm(np.linspace(0, 1, len(run_data)))

    for i, (name, df) in enumerate(run_data.items()):
        labels = name
        color = colors[i]
        ax.plot(df["x_coord_m"], df["y_coord_m"], color = color, linewidth = 2, label = labels)
        ax.plot(df["x_coord_m"].iloc[-1], df["y_coord_m"].iloc[-1], marker = "o", color = color)
    ax.axhline(y = 0, color = "black", linewidth = 1, label = "Lane centerline")
    ax.axhline(y = lane_half_width_m, color = "gray", linestyle = "--", label = "Lane edge")
    ax.axhline(y =-lane_half_width_m, color = "gray", linestyle = "--")
    ax.set_xlabel("Longitudinal displacement x (m)", fontsize = 10)
    ax.set_ylabel("Lateral displacement y (m)", fontsize = 10)
    ax.set_title("Vehicle Trajectory During Skidding\n on an Icy Curved Ramp")
    ax.grid(True,linestyle = "--", alpha = 0.5)
    ax.legend(fontsize = 10)

    output_path = Path(__file__).parent / "trajectory_plot.png"
    plt.savefig(output_path, dpi = 300, bbox_inches = "tight")
    plt.close()




