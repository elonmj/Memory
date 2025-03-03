def godunov_flux(rho_left, rho_right, model):
    """
    Calculate the numerical flux at the interface between two cells using Godunov's scheme.
    
    Args:
        rho_left: Density in the left cell (vehicles/km)
        rho_right: Density in the right cell (vehicles/km)
        model: An instance of the traffic model containing necessary methods.
        
    Returns:
        Numerical flux at the interface (vehicles/h)
    """
    if rho_left <= rho_right:
        if rho_left <= model.densite_critique() and rho_right >= model.densite_critique():
            return model.capacite()
        else:
            return min(model.flux(rho_left), model.flux(rho_right))
    else:
        return min(model.flux(rho_left), model.flux(rho_right))


def cfl_condition(dt, dx, v_max):
    """
    Check the CFL condition for stability in the numerical scheme.
    
    Args:
        dt: Time step (h)
        dx: Space step (km)
        v_max: Maximum speed (km/h)
        
    Returns:
        bool: True if CFL condition is satisfied, False otherwise.
    """
    return dt * v_max / dx <= 1.0


def update_density(density, flux_left, flux_right, dt, dx):
    """
    Update the density using the conservative form of the traffic equations.
    
    Args:
        density: Current density array (vehicles/km)
        flux_left: Flux from the left cell (vehicles/h)
        flux_right: Flux from the right cell (vehicles/h)
        dt: Time step (h)
        dx: Space step (km)
        
    Returns:
        Updated density array (vehicles/km)
    """
    return density - dt / dx * (flux_right - flux_left)


def godunov_flux_multiclass(rho_left, rho_right, model):
    """
    Calculate the numerical flux at the interface between two cells for the multiclass model
    using Godunov's scheme.
    
    Args:
        rho_left: Array of densities for each class in the left cell
        rho_right: Array of densities for each class in the right cell
        model: An instance of the multiclass traffic model
        
    Returns:
        Array of numerical fluxes for each class at the interface
    """
    n_classes = len(rho_left)
    flux = np.zeros(n_classes)
    
    # Update speeds based on the total densities
    v_left = model.speed(rho_left)
    v_right = model.speed(rho_right)
    
    # Calculate the flux for each class separately
    for i in range(n_classes):
        if v_left[i] >= 0 and v_right[i] >= 0:
            # Both speeds positive, flux comes from left
            flux[i] = rho_left[i] * v_left[i]
        elif v_left[i] <= 0 and v_right[i] <= 0:
            # Both speeds negative, flux comes from right
            flux[i] = rho_right[i] * v_right[i]
        elif v_left[i] > 0 and v_right[i] < 0:
            # Speeds change sign, compare fluxes (shock)
            flux[i] = min(rho_left[i] * v_left[i], rho_right[i] * v_right[i])
        else:
            # Rarefaction with speeds changing from negative to positive
            flux[i] = 0
    
    return flux