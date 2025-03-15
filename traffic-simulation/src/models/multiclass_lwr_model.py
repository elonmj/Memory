"""
Multiclass LWR Traffic Model Implementation

This module implements an extension of the classic LWR model to handle
multiple vehicle classes with different characteristics and interactions.
"""

import numpy as np
from .lwr_model import LWRModel


class VehicleClass:
    """Class representing a type of vehicle with its specific parameters."""
    
    def __init__(self, name, v_max, rho_max, eta=0.0, beta=0.0, lambda_min=0.6):
        """
        Initialize a vehicle class with its specific traffic behavior parameters.
        
        Args:
            name: Name of the vehicle class (e.g., 'car', 'moto', 'bus', 'truck')
            v_max: Maximum velocity in free flow conditions (km/h)
                   Typical values: 80-120 for cars, 90-110 for motorcycles,
                   60-90 for trucks/buses
            rho_max: Maximum density of this vehicle class (vehicles/km)
                    Typical values: 180-220 for cars, 200-300 for motorcycles,
                    120-150 for trucks/buses
            eta: Gap-filling coefficient (0-1)
                 Only relevant for motorcycles (typically 0.2-0.4)
                 Higher values represent more aggressive gap-filling behavior
                 where motorcycles can better utilize spaces between vehicles
            beta: Sensitivity coefficient to motorcycle presence (0-1)
                  How much this vehicle class is negatively affected by motorcycles
                  Typical values: 0.2-0.4 for cars, 0.3-0.5 for larger vehicles
                  Higher values mean more sensitivity to motorcycle interference
            lambda_min: Minimum road quality coefficient (0-1)
                      The minimum multiplier applied to velocity on the worst roads
                      Lower values make this vehicle class more sensitive to poor roads
                      Typical values: 0.8-0.9 for motorcycles, 0.5-0.7 for cars,
                      0.4-0.6 for larger vehicles
        """
        self.name = name
        self.v_max = v_max
        self.rho_max = rho_max
        self.eta = eta  # Gap-filling parameter (motorcycles)
        self.beta = beta  # Sensitivity to motorcycles
        self.lambda_min = lambda_min  # Minimum quality coefficient
        
        
class MulticlassLWRModel:
    """
    Implementation of an extended LWR model for multiple vehicle classes.
    
    This class handles interactions between different vehicle classes,
    particularly focusing on the special behaviors of motorcycles.
    """
    
    def __init__(self, vehicle_classes=None, n_classes=2):
        """
        Initialize the multiclass LWR traffic model with specific vehicle classes.
        
        This model extends the classic LWR framework to handle multiple vehicle classes
        with different characteristics and inter-class interactions. It is particularly
        designed to model the unique traffic dynamics in West African contexts where
        motorcycles interact with cars and other vehicles.
        
        Args:
            vehicle_classes: List of dictionaries or VehicleClass objects defining each class.
                           If None, default classes (motorcycles and cars) will be created.
                           Each dictionary should contain parameters for VehicleClass.
                           
            n_classes: Number of vehicle classes to model (default: 2 - motorcycles and cars)
        
        Examples:
            # Create a model with default classes (motorcycles and cars)
            model = MulticlassLWRModel()
            
            # Create a model with custom vehicle classes
            classes = [
                VehicleClass("moto", v_max=100, rho_max=250, eta=0.35, beta=0, lambda_min=0.85),
                VehicleClass("car", v_max=90, rho_max=180, eta=0, beta=0.25, lambda_min=0.6),
                VehicleClass("truck", v_max=70, rho_max=120, eta=0, beta=0.4, lambda_min=0.5)
            ]
            model = MulticlassLWRModel(vehicle_classes=classes, n_classes=3)
            
            # Create a model with dictionaries
            classes = [
                {"name": "moto", "v_max": 100, "rho_max": 250, "eta": 0.35},
                {"name": "car", "v_max": 90, "rho_max": 180, "beta": 0.25}
            ]
            model = MulticlassLWRModel(vehicle_classes=classes)
        """
        self.n_classes = n_classes
        
        # Default parameters if none provided
        if vehicle_classes is None:
            # Default: motorcycles and cars
            self.vehicle_classes = [
                VehicleClass("moto", v_max=90, rho_max=200, eta=0.3, beta=0.0, lambda_min=0.8),
                VehicleClass("car", v_max=100, rho_max=180, eta=0.0, beta=0.3, lambda_min=0.6)
            ]
        else:
            # Convert dictionaries to VehicleClass objects if needed
            self.vehicle_classes = []
            for vc in vehicle_classes:
                if isinstance(vc, dict):
                    self.vehicle_classes.append(
                        VehicleClass(
                            name=vc.get("name", f"class_{len(self.vehicle_classes)}"),
                            v_max=vc.get("v_max", 100.0),
                            rho_max=vc.get("rho_max", 180.0),
                            eta=vc.get("eta", 0.0),
                            beta=vc.get("beta", 0.0),
                            lambda_min=vc.get("lambda_min", 0.6)
                        )
                    )
                else:
                    self.vehicle_classes.append(vc)
            
            # Ensure we have exactly n_classes
            if len(self.vehicle_classes) < n_classes:
                # Add generic classes if needed
                for i in range(len(self.vehicle_classes), n_classes):
                    self.vehicle_classes.append(
                        VehicleClass(f"class_{i}", v_max=100.0, rho_max=180.0)
                    )
            elif len(self.vehicle_classes) > n_classes:
                # Truncate if too many
                self.vehicle_classes = self.vehicle_classes[:n_classes]
        
        # For convenience, calculate max values
        self.v_max = max(vc.v_max for vc in self.vehicle_classes)
        self.rho_max = max(vc.rho_max for vc in self.vehicle_classes)
        
    def critical_density(self):
        """
        Calculate critical density where flow is maximum.
        
        Returns:
            Critical density (vehicles/km)
        """
        # For simplicity, just use the average of all classes
        return sum(vc.rho_max for vc in self.vehicle_classes) / (2 * self.n_classes)
    
    def get_velocity(self, rho, class_idx=0, rho_moto=None):
        """
        Calculate velocity for a given density using extended Greenshields model.
        
        Args:
            rho: Total traffic density (vehicles/km)
            class_idx: Index of the vehicle class
            rho_moto: Motorcycle density (if None, assumes motorcycles are class 0)
            
        Returns:
            Velocity (km/h)
        """
        vc = self.vehicle_classes[class_idx]
        
        # Basic velocity calculation (Greenshields)
        v_basic = vc.v_max * (1.0 - rho / vc.rho_max)
        
        # Apply class-specific modulation based on motorcycle density
        if rho_moto is not None:
            # Motorcycles benefit from gap-filling
            if class_idx == 0:  # Assuming motorcycles are class 0
                # Gap-filling effect
                v_modulation = 1.0 + vc.eta * (rho_moto / vc.rho_max)
                return max(0, v_basic * v_modulation)
            else:
                # Other vehicles suffer from motorcycle interweaving
                v_modulation = 1.0 - vc.beta * (rho_moto / vc.rho_max)
                return max(0, v_basic * v_modulation)
        
        return max(0, v_basic)
    
    def get_flow(self, rho, class_idx=0, rho_moto=None):
        """
        Calculate flow for a given density.
        
        Args:
            rho: Total traffic density (vehicles/km)
            class_idx: Index of the vehicle class
            rho_moto: Motorcycle density (if applicable)
            
        Returns:
            Flow (vehicles/h)
        """
        return rho * self.get_velocity(rho, class_idx, rho_moto)
    
    def godunov_flux(self, rho_left, rho_right, class_idx=0, rho_moto_left=None, rho_moto_right=None):
        """
        Calculate numerical flux using Godunov scheme for multiclass model.
        
        Args:
            rho_left: Density on the left side of interface
            rho_right: Density on the right side of interface
            class_idx: Index of the vehicle class
            rho_moto_left: Motorcycle density on the left (if applicable)
            rho_moto_right: Motorcycle density on the right (if applicable)
            
        Returns:
            Numerical flux (vehicles/h)
        """
        # Critical density where flow is maximum
        rho_c = self.vehicle_classes[class_idx].rho_max / 2.0
        
        # Get intermediate values for flux calculation
        if rho_moto_left is not None:
            flow_left = self.get_flow(rho_left, class_idx, rho_moto_left)
            flow_right = self.get_flow(rho_right, class_idx, rho_moto_right)
            vel_left = self.get_velocity(rho_left, class_idx, rho_moto_left)
            vel_right = self.get_velocity(rho_right, class_idx, rho_moto_right)
        else:
            flow_left = self.get_flow(rho_left, class_idx)
            flow_right = self.get_flow(rho_right, class_idx)
            vel_left = self.get_velocity(rho_left, class_idx)
            vel_right = self.get_velocity(rho_right, class_idx)
        
        # Standard Godunov flux determination
        if rho_left <= rho_right:
            # Case 1: rho_left <= rho_right
            if rho_left >= rho_c:
                return flow_left
            elif rho_right <= rho_c:
                return flow_right
            else:
                # Maximum flow at critical density
                return self.get_flow(rho_c, class_idx)
        else:
            # Case 2: rho_left > rho_right
            if vel_left >= 0 and vel_right >= 0:
                return flow_left
            elif vel_left <= 0 and vel_right <= 0:
                return flow_right
            else:
                return 0  # Vacuum state
    
    def calculate_dt(self, rho_array, dx, cfl_factor=0.9):
        """
        Calculate time step based on CFL condition for multiclass model.
        
        Args:
            rho_array: Array of densities for all classes [n_classes, nx]
            dx: Spatial step size (km)
            cfl_factor: Safety factor for CFL condition (0-1)
            
        Returns:
            Time step (h)
        """
        # Calculate total density
        total_density = np.sum(rho_array, axis=0)
        
        # Motorcycle density (class 0)
        motorcycle_density = rho_array[0]
        
        # Initialize maximum wave speed
        max_wave_speed = 0
        
        for i in range(self.n_classes):
            vc = self.vehicle_classes[i]
            
            # For each position in the domain
            for j in range(total_density.shape[0]):
                # Current densities at this position
                rho_total = total_density[j]
                rho_moto = motorcycle_density[j]
                
                # Base flux derivative for class i
                base_derivative = vc.v_max * (1 - 2 * rho_total / vc.rho_max)
                
                # Additional modulation effects (for both gap-filling and interweaving)
                if i == 0:  # Motorcycle class
                    # Gap-filling effect modifies wave speed
                    modulation = 1 + vc.eta * (rho_moto / vc.rho_max)
                    wave_speed = base_derivative * modulation
                    
                    # Additional wave speed component from gap-filling function derivative
                    if rho_total > 0:
                        gap_filling_derivative = vc.v_max * vc.eta * (1 - rho_total / vc.rho_max) / vc.rho_max
                        wave_speed += rho_moto * gap_filling_derivative
                else:
                    # Interweaving effect for other vehicle classes
                    modulation = 1 - vc.beta * (rho_moto / vc.rho_max)
                    wave_speed = base_derivative * modulation
                    
                    # Additional wave speed component from interweaving function derivative
                    if rho_total > 0:
                        interweaving_derivative = -vc.v_max * vc.beta * (1 - rho_total / vc.rho_max) / vc.rho_max
                        wave_speed += rho_array[i, j] * interweaving_derivative
                
                # Update maximum wave speed
                max_wave_speed = max(max_wave_speed, abs(wave_speed))
        
        # Ensure we don't miss the free-flow wave speed
        for i in range(self.n_classes):
            max_wave_speed = max(max_wave_speed, self.vehicle_classes[i].v_max)
        
        # CFL condition: dt ≤ dx / max_wave_speed
        dt = cfl_factor * dx / max_wave_speed
        
        return dt
    
    def compute_road_quality(self, road_quality_func, x, class_idx):
        """
        Compute road quality coefficient for a specific vehicle class.
        
        Args:
            road_quality_func: Function that returns base road quality at position x
            x: Position (km)
            class_idx: Index of the vehicle class
            
        Returns:
            Effective road quality coefficient for this class
        """
        if road_quality_func is None:
            return 1.0
            
        base_quality = road_quality_func(x)
        vc = self.vehicle_classes[class_idx]
        
        # Scale the quality coefficient based on vehicle class parameters
        # Each class has a minimum quality threshold
        scaled_quality = vc.lambda_min + (1.0 - vc.lambda_min) * base_quality
        
        return scaled_quality
    
    def simulate(self, initial_density, domain_length, simulation_time, dx, dt=None, 
                cfl_factor=0.9, road_quality_func=None):
        """
        Solve the multiclass LWR model using Godunov's scheme.
        
        Args:
            initial_density: Initial density distribution (array [n_classes, nx] or function)
            domain_length: Length of the spatial domain (km)
            simulation_time: Total simulation time (h)
            dx: Spatial step size (km)
            dt: Time step size (h), if None calculated from CFL
            cfl_factor: Safety factor for CFL condition (0-1)
            road_quality_func: Function returning road quality coefficient at position x
            
        Returns:
            Dictionary containing simulation results
        """
        # Create spatial grid
        nx = int(domain_length / dx) + 1
        x = np.linspace(0, domain_length, nx)
        
        # Initialize densities for all classes
        rho = np.zeros((self.n_classes, nx))
        
        # If initial_density is a function, call it for each position
        if callable(initial_density):
            for j in range(nx):
                density_at_x = initial_density(x[j])
                if isinstance(density_at_x, (list, tuple, np.ndarray)):
                    for i in range(self.n_classes):
                        if i < len(density_at_x):
                            rho[i, j] = density_at_x[i]
                else:
                    # If scalar, assign to first class
                    rho[0, j] = density_at_x
        else:
            # If array is provided directly
            if isinstance(initial_density, np.ndarray):
                if initial_density.ndim == 1:
                    # Single class initial condition
                    rho[0] = initial_density
                elif initial_density.ndim == 2:
                    # Multiple class initial conditions
                    for i in range(min(self.n_classes, initial_density.shape[0])):
                        rho[i] = initial_density[i]
            else:
                # Scalar value, assign to first class
                rho[0] = float(initial_density)
        
        # Calculate time step if not provided
        if dt is None:
            dt = self.calculate_dt(rho, dx, cfl_factor)
        
        # Create time grid
        nt = int(simulation_time / dt) + 1
        t = np.linspace(0, simulation_time, nt)
        
        # Initialize result arrays for all classes
        densities = np.zeros((self.n_classes, nt, nx))
        velocities = np.zeros((self.n_classes, nt, nx))
        flows = np.zeros((self.n_classes, nt, nx))
        
        # Set initial conditions for all classes
        for i in range(self.n_classes):
            densities[i, 0] = rho[i]
        
        # Calculate initial velocities and flows based on initial densities
        total_density = np.sum(rho, axis=0)
        
        for i in range(self.n_classes):
            for j in range(nx):
                # Apply road quality if provided
                quality = self.compute_road_quality(road_quality_func, x[j], i) if road_quality_func else 1.0
                
                # Calculate velocity with road quality factor
                velocities[i, 0, j] = quality * self.get_velocity(
                    total_density[j], i, rho[0, j] if i > 0 else None
                )
                
                flows[i, 0, j] = rho[i, j] * velocities[i, 0, j]
        
        # Main time integration loop
        for n in range(nt - 1):
            # Update density for each class
            for i in range(self.n_classes):
                # Calculate fluxes at cell interfaces
                flux = np.zeros(nx + 1)
                
                for j in range(1, nx):
                    # For fluxes that depend on motorcycle density
                    if i > 0:  # Non-motorcycle classes
                        flux[j] = self.godunov_flux(
                            rho[i, j-1], rho[i, j], i, 
                            rho[0, j-1], rho[0, j]
                        )
                    else:  # Motorcycle class
                        flux[j] = self.godunov_flux(rho[i, j-1], rho[i, j], i)
                
                # Boundary conditions: zero gradient
                flux[0] = flux[1]
                flux[nx] = flux[nx-1]
                
                # Update density using conservative formula
                rho[i] = rho[i] - dt / dx * (flux[1:] - flux[:-1])
                
                # Ensure non-negative density
                rho[i] = np.maximum(0, rho[i])
            
            # Recalculate total density
            total_density = np.sum(rho, axis=0)
            
            # Calculate velocities and flows for this time step
            for i in range(self.n_classes):
                for j in range(nx):
                    # Apply road quality if provided
                    quality = self.compute_road_quality(road_quality_func, x[j], i) if road_quality_func else 1.0
                    
                    # Calculate velocity with road quality factor
                    velocities[i, n+1, j] = quality * self.get_velocity(
                        total_density[j], i, rho[0, j] if i > 0 else None
                    )
                    
                    flows[i, n+1, j] = rho[i, j] * velocities[i, n+1, j]
            
            # Store results for this time step
            for i in range(self.n_classes):
                densities[i, n+1] = rho[i]
        
        # Calculate aggregate measures
        total_density = np.sum(densities, axis=0)
        total_flow = np.sum(flows, axis=0)
        
        # Calculate average velocity weighted by density
        with np.errstate(divide='ignore', invalid='ignore'):
            avg_velocity = np.sum(densities * velocities, axis=0) / np.maximum(total_density, 1e-10)
            avg_velocity = np.nan_to_num(avg_velocity)  # Replace NaNs with zeros
        
        # Return results as dictionary
        return {
            'density': total_density,
            'velocity': avg_velocity,
            'flow': total_flow,
            'class_densities': densities,
            'class_velocities': velocities,
            'class_flows': flows,
            'grid_x': x,
            'grid_t': t,
            'n_classes': self.n_classes,
            'parameters': {
                'vehicle_classes': [vc.__dict__ for vc in self.vehicle_classes],
                'dx': dx,
                'dt': dt,
                'domain_length': domain_length,
                'simulation_time': simulation_time
            }
        }
