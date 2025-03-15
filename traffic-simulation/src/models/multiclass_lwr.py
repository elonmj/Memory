"""
Multi-Class Lighthill-Whitham-Richards (LWR) Traffic Model Implementation

Ce modèle étend le LWR standard pour supporter multiple classes de véhicules,
notamment les motos avec leurs comportements spécifiques dans le contexte béninois.

Le modèle implémente le système d'équations couplées :
    ∂ρᵢ/∂t + ∂(ρᵢvᵢ)/∂x = Sᵢ(x,t)    pour chaque classe i

avec la relation vitesse-densité étendue :
    vᵢ(ρ,ρₘ) = λᵢ⋅vᵢ_max⋅(1 - ρ/ρ_max)⋅fᵢ(ρₘ)

NOTE IMPORTANTE: Cette implémentation est une version simplifiée du modèle multi-classes.
Pour une implémentation plus complète et robuste avec davantage de fonctionnalités,
il est recommandé d'utiliser plutôt la classe MulticlassLWRModel du module 
multiclass_lwr_model.py.
"""

import numpy as np
from .base_model import BaseModel
from .fundamental_diagram import FundamentalDiagram

class VehicleClass:
    def __init__(self, name, v_max, mu_i=0.0, eta=0.0):
        """
        Initialize a vehicle class with its specific parameters.
        
        Args:
            name: Name of the vehicle class (e.g., "moto", "voiture")
            v_max: Maximum speed for this class (km/h)
            mu_i: Interweaving coefficient (sensitivity to motorcycles)
            eta: Gap-filling coefficient (for motorcycles only)
        """
        self.name = name
        self.v_max = v_max
        self.mu_i = mu_i
        self.eta = eta

class RoadCondition:
    def __init__(self, type_name, lambda_coefficients):
        """
        Initialize road condition with its impact on different vehicle classes.
        
        Args:
            type_name: Type of road (e.g., "bitume_bon", "terre")
            lambda_coefficients: Dict mapping vehicle class names to their λᵢ coefficients
        """
        self.type_name = type_name
        self.lambda_coefficients = lambda_coefficients

class MultiClassLWRModel(BaseModel):
    """
    Implementation of the multi-class LWR traffic model with specific
    considerations for motorcycle behavior and road conditions.
    """
    
    def __init__(self, vehicle_classes, rho_max=180):
        """
        Initialize the multi-class LWR model.
        
        Args:
            vehicle_classes: List of VehicleClass objects
            rho_max: Maximum total density (vehicles/km)
        """
        # Find maximum speed among all classes for base model
        v_max = max(vc.v_max for vc in vehicle_classes)
        super().__init__(rho_max, v_max)
        
        self.vehicle_classes = vehicle_classes
        self.num_classes = len(vehicle_classes)
        # Current road condition, can be updated during simulation
        self.road_condition = None
        
    def set_road_condition(self, road_condition):
        """Set the current road condition affecting vehicle speeds."""
        self.road_condition = road_condition
    
    def get_lambda(self, vehicle_class):
        """Get road condition coefficient for a vehicle class."""
        if self.road_condition is None:
            return 1.0  # Default to perfect conditions
        return self.road_condition.lambda_coefficients.get(vehicle_class.name, 1.0)
    
    def modulation_factor(self, vehicle_class, moto_density):
        """
        Calculate the modulation factor fᵢ(ρₘ) for a vehicle class.
        
        Args:
            vehicle_class: VehicleClass object
            moto_density: Current motorcycle density (vehicles/km)
        
        Returns:
            Modulation factor accounting for motorcycle interactions
        """
        if vehicle_class.name == "moto":
            # Gap-filling behavior for motorcycles
            return 1 + vehicle_class.eta * (moto_density / self.rho_max)
        else:
            # Interweaving impact on other vehicles
            return 1 - vehicle_class.mu_i * (moto_density / self.rho_max)
    
    def speed_for_class(self, vehicle_class, total_density, moto_density):
        """
        Calculate speed for a specific vehicle class considering road conditions
        and motorcycle interactions.
        
        Args:
            vehicle_class: VehicleClass object
            total_density: Total traffic density (vehicles/km)
            moto_density: Motorcycle density (vehicles/km)
            
        Returns:
            Speed for the vehicle class (km/h)
        """
        lambda_i = self.get_lambda(vehicle_class)
        f_i = self.modulation_factor(vehicle_class, moto_density)
        
        # Extended Greenshields model with road condition and motorcycle effects
        return lambda_i * vehicle_class.v_max * (1 - total_density/self.rho_max) * f_i
    
    def flow_for_class(self, vehicle_class, class_density, total_density, moto_density):
        """
        Calculate flow for a specific vehicle class.
        
        Args:
            vehicle_class: VehicleClass object
            class_density: Density of this vehicle class (vehicles/km)
            total_density: Total traffic density (vehicles/km)
            moto_density: Motorcycle density (vehicles/km)
            
        Returns:
            Flow for the vehicle class (vehicles/h)
        """
        return class_density * self.speed_for_class(vehicle_class, total_density, moto_density)
    
    def solve_multiclass(self, initial_densities, domain_length, simulation_time, dx, dt):
        """
        Solve the multi-class LWR model using Godunov's scheme.
        
        Args:
            initial_densities: List of functions, each taking position x and returning
                             initial density for a vehicle class
            domain_length: Length of the road segment (km)
            simulation_time: Total simulation duration (h)
            dx: Spatial step (km)
            dt: Time step (h)
            
        Returns:
            Tuple of (densities, grid_x, grid_t) where densities is a list of 2D arrays,
            one per vehicle class
        """
        # CFL condition check using maximum speed among all classes
        max_speed = max(vc.v_max for vc in self.vehicle_classes)
        cfl = dt * max_speed / dx
        if cfl > 1.0:
            raise ValueError(f"CFL condition not satisfied: {cfl} > 1.0")
        
        nx = int(domain_length / dx) + 1
        nt = int(simulation_time / dt) + 1
        grid_x = np.linspace(0, domain_length, nx)
        grid_t = np.linspace(0, simulation_time, nt)
        
        # Initialize densities for each class
        densities = [np.zeros((nt, nx)) for _ in range(self.num_classes)]
        
        # Set initial conditions
        for i, init_dens in enumerate(initial_densities):
            densities[i][0, :] = [init_dens(x) for x in grid_x]
        
        # Time evolution using Godunov scheme
        for n in range(nt-1):
            # Current total and motorcycle densities
            total_density = sum(d[n, :] for d in densities)
            moto_density = next(d[n, :] for i, d in enumerate(densities) 
                              if self.vehicle_classes[i].name == "moto")
            
            # Update each class
            for i, vehicle_class in enumerate(self.vehicle_classes):
                for j in range(1, nx-1):
                    # Calculate fluxes
                    flux_left = self.flow_for_class(
                        vehicle_class,
                        densities[i][n, j-1],
                        total_density[j-1],
                        moto_density[j-1]
                    )
                    flux_right = self.flow_for_class(
                        vehicle_class,
                        densities[i][n, j],
                        total_density[j],
                        moto_density[j]
                    )
                    
                    # Update density
                    densities[i][n+1, j] = densities[i][n, j] - \
                        dt/dx * (flux_right - flux_left)
                
                # Boundary conditions (zero gradient)
                densities[i][n+1, 0] = densities[i][n+1, 1]
                densities[i][n+1, -1] = densities[i][n+1, -2]
        
        return densities, grid_x, grid_t
        for n in range(nt-1):
            # Main space loop
            for j in range(1, nx-1):
                # Update road quality for current cell
                self.lambda_mat = lambda_values[j]
                
                # Get densities at relevant positions
                rho_left = densities[:, n, j-1]
                rho_center = densities[:, n, j]
                rho_right = densities[:, n, j+1]
                
                # Calculate fluxes
                flux_left = godunov_flux_multiclass(rho_left, rho_center, self)
                flux_right = godunov_flux_multiclass(rho_center, rho_right, self)
                
                # Update each class
                for i in range(self.n_classes):
                    densities[i, n+1, j] = densities[i, n, j] - dt/dx * (flux_right[i] - flux_left[i])
            
            # Boundary conditions (zero gradient)
            densities[:, n+1, 0] = densities[:, n+1, 1]
            densities[:, n+1, -1] = densities[:, n+1, -2]
        
        return densities, grid_x, grid_t
