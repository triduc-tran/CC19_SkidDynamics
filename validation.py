def validate_parameters(parameters):
    """
    Checks for errors in parameters then prints a warning message
    :param parameters: dict - parameters imported from initial_state.json
    :return: print warning message
    """
    mass = parameters["vehicle_parameters"]["mass_kg"]
    radius = parameters["road_geometry"]["radius_horizontal_m"]
    mu_list = parameters["environment"]["pavement_friction_coeffs"]
    mu_simulation = parameters["simulation"]["mu_simulation"]
    highlight_mu = parameters["simulation"]["highlight_mu"]
    air_density = parameters["environment"]["air_density_kg_m3"]
    gravitational_accel = parameters["environment"]["gravitational_acceleration_m_s2"]
    drag_coeff = parameters["vehicle_parameters"]["aerodynamic_drag_coeff"]
    rolling_resistance_coeff = parameters["vehicle_parameters"]["tire_rolling_resistance"]
    frontal_area = parameters["vehicle_parameters"]["frontal_area_m2"]
    grid_res = parameters["simulation"]["grid_resolution"]
    speed_range = parameters["simulation"]["speed_range_m_s"]
    accel_range = parameters["simulation"]["accel_range_m_s2"]
    time_span = parameters["simulation"]["time_span_s"]
    ini_speed = parameters["simulation"]["initial_speed_m_s"]
    lane_half_width = parameters["simulation"]["lane_half_width_m"]
    long_slope = parameters["road_geometry"]["longitudinal_slope_rad"]
    cross_slope = parameters["road_geometry"]["cross_slope_rad"]
    commanded_accel = parameters["simulation"]["commanded_accel_m_s2"]

    if mass <= 0:
        raise ValueError("Vehicle's mass must be a positive value!")
    if radius <= 0:
        raise ValueError("Road's curve radius must be a positive value!")
    for mu in mu_list:
        if mu <= 0 or mu > 1:
            raise ValueError(f"{mu} is not a valid value for μ!")
    if frontal_area <= 0:
        raise ValueError("Vehicle's frontal area must be a positive value!")
    if drag_coeff < 0:
        raise ValueError("Vehicle's aerodynamic drag coefficient cannot be a negative value!")
    if rolling_resistance_coeff < 0:
        raise ValueError("Vehicle's tire resistance coefficient cannot be a negative value!")
    if air_density <= 0:
        raise ValueError("Air density must be a positive value!")
    if gravitational_accel <= 0:
        raise ValueError("Gravitational acceleration must be a positive value!")
    if highlight_mu not in mu_list:
        raise ValueError(f"{highlight_mu} must equal a value in mu_list")
    if mu_simulation <= 0 or mu_simulation > 1:
        raise ValueError("Friction coefficient used in simulation is invalid!")
    if speed_range[0] >= speed_range[1] or speed_range[0] < 0:
        raise ValueError("Invalid speed range!")
    if accel_range[0] >= accel_range[1]:
        raise ValueError("Invalid acceleration range!")
    if time_span[1] <= time_span[0]:
        raise ValueError("Invalid time span!")
    if lane_half_width <= 0:
        raise ValueError("Lane's half width in simulation must be a positive value!")
    if abs(long_slope) > 1 or abs(cross_slope) > 1:
        raise ValueError("Invalid value for slope angle!")
    if abs(long_slope) > 0.2 or abs(cross_slope) > 0.2:
        print("Slope is unusually steep, check your units")
    if grid_res < 2:
        raise ValueError("Resolution too low!")
    if ini_speed < 0:
        raise ValueError("Initial speed must not be a negative value!")
    if commanded_accel > accel_range[1] or commanded_accel < accel_range[0]:
        raise ValueError(f"{commanded_accel} is out of predetermined acceleration range!")




