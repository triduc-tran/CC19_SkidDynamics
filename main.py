import numpy as np
import json
from pathlib import Path
from solvers import run_simulation, compute_safd
from visualizations.SAFD_plot import plot_safd

if __name__ == '__main__':
    base_dir = Path(__file__).parent
    input_path = base_dir / "inputs" / "initial_state.json"
    output_path = base_dir / "data" / "simulation_results.csv"

    with open(input_path, "r") as file:
        parameters: dict = json.load(file)

    np.random.seed(parameters["simulation"]["random_seed"])

    a_x = parameters["simulation"]["commanded_accel_m_s2"]

    results_df  = run_simulation(a_x, parameters)

    results_df.to_csv(output_path, index = False)

    mu_list = parameters["environment"]["pavement_friction_coeffs"]
    safd_results = []
    for mu in mu_list:
        data = compute_safd(mu, parameters)
        safd_results.append(data)

    plot_safd(safd_results, parameters, mu_list)
    print("SAFD plot successfully generated!")

    print(f"Simulation complete. Results are exported to {output_path}")

