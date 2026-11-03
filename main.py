import numpy as np
import json
from pathlib import Path
import pandas as pd
from solvers import run_simulation, compute_safd
from visualizations.SAFD_plot import plot_safd
from visualizations.trajectory_plot import plot_trajectories
from validation import validate_parameters
import copy
from physics_model import compute_critical_speed
from visualizations.energy_error_plot import plot_energy_error


if __name__ == '__main__':
    base_dir = Path(__file__).parent
    input_path = base_dir / "inputs" / "initial_state.json"
    output_path = base_dir / "data" / "simulation_results.csv"
    inward_output_path = base_dir / "data" / "results_inward.csv"
    outward_output_path = base_dir / "data" / "results_outward.csv"

    with open(input_path, "r") as file:
        parameters: dict = json.load(file)
        validate_parameters(parameters)

    np.random.seed(parameters["simulation"]["random_seed"])
    a_x = parameters["simulation"]["commanded_accel_m_s2"]

    results_df  = run_simulation(a_x, parameters)
    results_df.to_csv(output_path, index = False)

    mu_list = parameters["environment"]["pavement_friction_coeffs"]
    v_crit = compute_critical_speed(parameters)
    parameters_inward = copy.deepcopy(parameters)
    parameters_inward["simulation"]["initial_speed_m_s"] = 0.6 * v_crit
    parameters_outward = copy.deepcopy(parameters)
    parameters_outward["simulation"]["initial_speed_m_s"] = 2.5 * v_crit
    inward_df = run_simulation(a_x, parameters_inward)
    outward_df = run_simulation(a_x, parameters_outward)
    inward_df.to_csv(inward_output_path, index = False)
    outward_df.to_csv(outward_output_path, index=False)
    run_data = {"Inward skid (v < v_crit)": inward_df, "Outward skid (v > v_crit)": outward_df}

    safd_results = []

    for mu in mu_list:
        data = compute_safd(mu, parameters)
        safd_results.append(data)

    print(f"Simulation complete. Results are exported to {output_path}")
    plot_energy_error(results_df, parameters)
    print("Energy error plot successfully generated!")
    plot_trajectories(run_data, parameters)
    print("Trajectories plot successfully generated!")
    plot_safd(safd_results, parameters, mu_list)
    print("SAFD plot successfully generated!")



