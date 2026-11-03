from scipy.integrate import solve_ivp
import numpy as np
import pandas as pd
from physics_model import (compute_longitudinal_force, compute_lateral_force, compute_normal_force, required_friction)


def equations_of_motion(t, state, a_x, parameters):
    """
    Define the system of ODEs for vehicle motion on the road
    :param t: float - time (s)
    :param state: longitudinal and lateral position, velocity
    :param a_x: float - longitudinal acceleration (m/s^2)
    :param parameters: dict - simulation parameters from initial_state.json
    :return: list - [dx/dt, dy/dt, dv_x/dt, dv_y/dt]
    """

    x = state[0]
    y = state[1]
    v_x = state[2]
    v_y = state[3]

    mu = parameters["simulation"]["mu_simulation"]
    m = parameters["vehicle_parameters"]["mass_kg"]
    theta = parameters["road_geometry"]["longitudinal_slope_rad"]

    f_normal = compute_normal_force(v_x,parameters)
    f_lateral = compute_lateral_force(v_x,parameters)
    f_long = compute_longitudinal_force(v_x,a_x,f_normal, parameters)

    dx_dt = v_x * np.cos(theta)
    dy_dt = v_y
    dv_x_dt = a_x

    friction_limit = mu * f_normal
    friction_demand = np.sqrt(f_long**2 + f_lateral**2)

    if friction_demand <= friction_limit:
        dv_y_dt = 0
    else:
        f_lateral_max = np.sqrt(np.maximum(friction_limit**2 - f_long**2, 0))
        excess = np.abs(f_lateral) - f_lateral_max
        dv_y_dt = np.sign(f_lateral)*excess/m

    return [dx_dt, dy_dt, dv_x_dt, dv_y_dt]

def run_simulation(a_x, parameters):
    t_start = parameters["simulation"]["time_span_s"][0]
    t_end = parameters["simulation"]["time_span_s"][1]

    x0 = 0.0
    y0 = 0.0
    vx0 = parameters["simulation"]["initial_speed_m_s"]
    vy0 = 0.0

    solution = solve_ivp(
        fun= equations_of_motion,
        t_span= (t_start, t_end),
        y0= [x0, y0, vx0, vy0],
        method= "RK45",
        t_eval= np.linspace(t_start, t_end, 1000),
        args= (a_x, parameters),
        events=car_stopped
    )
    time = solution.t
    x = solution.y[0]
    y = solution.y[1]
    vx = solution.y[2]
    vy = solution.y[3]

    m = parameters["vehicle_parameters"]["mass_kg"]
    g = parameters["environment"]["gravitational_acceleration_m_s2"]
    theta = parameters["road_geometry"]["longitudinal_slope_rad"]

    kinetic_energy = 0.5 * m * (vx**2 + vy**2)
    height = x * np.sin(theta)
    potential_energy = m * g * height
    mechanical_energy = kinetic_energy + potential_energy

    df = pd.DataFrame({
        "time_s": time,
        "x_coord_m": x,
        "y_coord_m": y,
        "velocity_x_m_s": vx,
        "velocity_y_m_s": vy,
        "kinetic_energy_J": kinetic_energy,
        "potential_energy_J": potential_energy,
        "mechanical_energy_J": mechanical_energy
    })

    return df

def compute_safd(mu_available, parameters):
    """
    Compute the Speed-Acceleration Feasible Domain for a given friction coefficient
    :param mu_available: float - available friction coefficient
    :param parameters: dict - simulation parameters from initial_state.json
    :return: dictionary containing speed grid, acceleration grid, mu_required grid, margin grid.
    """
    v_min = parameters["simulation"]["speed_range_m_s"][0]
    v_max = parameters["simulation"]["speed_range_m_s"][1]
    ax_min = parameters["simulation"]["accel_range_m_s2"][0]
    ax_max = parameters["simulation"]["accel_range_m_s2"][1]
    resolution = parameters["simulation"]["grid_resolution"]

    v_array = np.linspace(v_min, v_max, resolution)
    ax_array = np.linspace(ax_min, ax_max, resolution)

    v, ax = np.meshgrid(v_array, ax_array)

    f_normal = compute_normal_force(v, parameters)
    f_lateral = compute_lateral_force(v, parameters)
    f_long = compute_longitudinal_force(v, ax, f_normal, parameters)

    mu_req = required_friction(f_long, f_lateral, f_normal)
    mu_margin = mu_available - mu_req

    return {
        "v": v,
        "a_x": ax,
        "mu_required": mu_req,
        "mu_margin": mu_margin
    }
def car_stopped(t, state, a_x, parameters):
    """
    Define the stoppage of the car
    :param t: float - time (s)
    :param state: longitudinal and lateral position, velocity
    :param a_x: float - longitudinal acceleration (m/s^2)
    :param parameters: dict - simulation parameters from initial_state.json
    :return: float - speed (m/s)
    """
    return state[2]

car_stopped.terminal = True