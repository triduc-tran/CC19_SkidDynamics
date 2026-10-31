import pandas as pd
import matplotlib as plt
from pathlib import Path

from sympy.printing.pretty.pretty_symbology import line_width


def plot_trajectories(run_files, labels, color, lane_half_width_m, output_path):
    """
    Plot the trajectory of the vehicle in simulation
    :param run_files: list - paths to the csv file
    :param labels: list - legend texts
    :param color: list - a list of color names
    :param lane_half_width_m: float - half of a predetermined lane's width
    :param output_path: str - Path to the generated image
    :return:
    """
    fig, ax = plt.subplots(figsize=(10,6))

    for path, label, color in zip(run_files, labels, colors):
        df = pd.read_csv(path)
        ax.plot(df["x_coord_m"], df["y_coord_m"], color = color, linewidth = 2, label = label)
        ax.plot(df["x_coord_m"].iloc[-1], df["y_coord_m"].iloc[-1], marker = "o", color = color)
        ax.axhline(y = 0, color = "black", linewidth = 1, label = "Lane centerline")
        ax.axhline(y = lane_half_width_m, color = "gray", linestyle = "--", label = "Lane edge")
        ax.axhline(y =-lane_half_width_m, color = "gray", linestyle = "--")
        ax.set_xlabel("Longitudinal displacement x (m)", fontsize = 10)
        ax.set_xlabel("Lateral displacement y (m)", fontsize = 10)
        ax.set_title("Vehicle Trajectory During Skidding\n on an Icy Curved Ramp")
        ax.grid(True,linestyle = "--", alpha = 0.5)
        ax.legend(fontsize = 10)

        plt.savefig(output_path, dpi = 300, bbox_inches = "tight")
        plt.close()




