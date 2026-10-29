
import numpy as np

def compute_normal_force(v, parameters):
    """
    Compute the normal force acting on the vehicle
    :param v: float - vehicle speed (m/s)
    :param parameters: dict - simulation parameters from initial_state.json
    :return:f_normal: float - the normal force (N) perpendicular to the road surface
    """
    m = parameters["vehicle_parameters"]["mass_kg"]
    g = parameters["environment"]["gravitational_acceleration_m_s2"]
    theta = parameters["road_geometry"]["longitudinal_slope_rad"]
    phi = parameters["road_geometry"]["cross_slope_rad"]
    r = parameters["road_geometry"]["radius_horizontal_m"]

    f_normal = m*g*np.cos(theta)*np.cos(phi)+m*v**2*np.sin(phi)*np.cos(theta)**2/r

    return f_normal

def compute_aerodynamic_drag(v, parameters):
    """
    Compute the aerodynamic drag force acting on the vehicle, opposing motion
    :param v: float - vehicle speed (m/s)
    :param parameters: dict - simulation parameters from initial_state.json
    :return: f_drag: float - the aerodynamic drag force (N), always positive
    """
    c_d = parameters["vehicle_parameters"]["aerodynamic_drag_coeff"]
    rho = parameters["environment"]["air_density_kg_m3"]
    s = parameters["vehicle_parameters"]["frontal_area_m2"]

    f_drag = 0.5*c_d*rho*s*v**2

    return f_drag

def compute_rolling_resistance(f_normal, parameters):
    """
    Compute rolling resistance on tires
    :param f_normal: float - normal force (N)
    :param parameters: dict - simulation parameters from initial_state.json
    :return: f_roll - float - rolling resistance force (N)
    """
    c_r = parameters["vehicle_parameters"]["tire_rolling_resistance"]

    f_roll = c_r * f_normal

    return f_roll

def compute_lateral_force(v, parameters):
    """
    Compute the required lateral force on the vehicle
    :param v: float - vehicle speed (m/s)
    :param parameters: dict - simulation parameters from initial_state.json
    :return: f_lateral: float - net lateral force (N)
    """
    m = parameters["vehicle_parameters"]["mass_kg"]
    theta = parameters["road_geometry"]["longitudinal_slope_rad"]
    phi = parameters["road_geometry"]["cross_slope_rad"]
    r = parameters["road_geometry"]["radius_horizontal_m"]
    g = parameters["environment"]["gravitational_acceleration_m_s2"]

    f_centrifugal = m*v**2*np.cos(theta)**2*np.cos(phi)/r
    f_gravity_lateral = m*g*np.cos(theta)*np.sin(phi)
    f_lateral = f_gravity_lateral - f_centrifugal

    return f_lateral

def compute_longitudinal_force(v, a_x, f_normal, parameters):
    """
    Compute the required longitudinal force acting on the vehicle
    :param v: float - vehicle speed (m/s)
    :param a_x: float - vehicle's longitudinal acceleration(m/s^2)
    :param f_normal: float - the normal force (N) perpendicular to the road surface
    :param parameters: dict - simulation parameters from initial_state.json
    :return: f_x: float - net longitudinal force (N)
    """

    m = parameters["vehicle_parameters"]["mass_kg"]
    g = parameters["environment"]["gravitational_acceleration_m_s2"]
    theta = parameters["road_geometry"]["longitudinal_slope_rad"]
    phi = parameters["road_geometry"]["cross_slope_rad"]
    f_drag = compute_aerodynamic_drag(v, parameters)
    f_roll = compute_rolling_resistance(f_normal, parameters)

    f_x = m*a_x + f_drag + f_roll + m*g*np.sin(theta)*np.cos(phi)

    return f_x

def required_friction(f_x, f_y, f_z):
    """
    Compute the required friction coefficient to keep the vehicle from skidding
    :param f_x: float - longitudinal net force (N)
    :param f_y: float - lateral net force (N)
    :param f_z: float - normal force (N)
    :return: mu_req
    """

    mu_req = np.sqrt(f_x**2 + f_y**2)/f_z

    return mu_req

def compute_coasting_acceleration(v, parameters):
    """
    Vehicle's acceleration when neither throttle nor brake is applied
    :param v: float - vehicle speed (m/s)
    :param parameters: dict - simulation parameters from initial_state.json
    :return: a_coasting: float - coasting acceleration (m/s^2)
    """

    m = parameters["vehicle_parameters"]["mass_kg"]
    f_normal = compute_normal_force(v, parameters)
    a_coasting = compute_longitudinal_force(v, 0, f_normal, parameters)/-m

    return a_coasting

def compute_critical_speed(parameters):
    """
    Computing the speed at which the road has to supply no sideways friction
    :param parameters: dict - simulation parameters from initial_state.json
    :return: v_crit: float - critical speed (m/s)
    """

    g = parameters["environment"]["gravitational_acceleration_m_s2"]
    theta = parameters["road_geometry"]["longitudinal_slope_rad"]
    phi = parameters["road_geometry"]["cross_slope_rad"]
    r = parameters["road_geometry"]["radius_horizontal_m"]

    v_crit = np.sqrt(g*r*np.tan(phi)/np.cos(theta))

    return v_crit