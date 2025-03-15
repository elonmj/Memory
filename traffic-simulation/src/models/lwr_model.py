"""
LWR Traffic Model Implementation

This module implements the classic Lighthill-Whitham-Richards (LWR) traffic flow model,
including numerical solvers and fundamental diagrams.
"""

import numpy as np
from numpy.typing import ArrayLike

class LWRModel:
    """
    Implementation of the Lighthill-Whitham-Richards (LWR) traffic flow model.
    
    This class provides methods to solve the LWR traffic flow equations using
    the Godunov finite volume method.
    """
    
    def __init__(self, v_max=100.0, rho_max=180.0):
        """
        Initialize the LWR model with parameters.
        
        Args:
            v_max: Maximum velocity in free flow (km/h)
            rho_max: Maximum density (vehicles/km)
        """
        self.v_max = v_max
        self.rho_max = rho_max
        
    def get_velocity(self, rho):
        """
        Calculate the velocity based on density using the fundamental relation.
        
        Args:
            rho: Traffic density (veh/km)
            
        Returns:
            float or array: Velocity (km/h)
        """
        # Simplify: Just use the core Greenshields formula without shape handling
        # Let NumPy automatically handle broadcasting between scalars and arrays
        ratio = np.asarray(rho) / self.rho_max
        return np.maximum(0, self.v_max * (1 - ratio))
    
    def get_flow(self, rho):
        """
        Calculate flow for a given density using Greenshields model.
        
        Args:
            rho: Traffic density (vehicles/km)
            
        Returns:
            Flow (vehicles/h)
        """
        # Simply multiply density by velocity - NumPy handles broadcasting
        return np.asarray(rho) * self.get_velocity(rho)
    
    def critical_density(self):
        """
        Calculate critical density where flow is maximum.
        
        Returns:
            Critical density (vehicles/km)
        """
        return self.rho_max / 2.0
    
    def godunov_flux(self, rho_left, rho_right):
        """
        Calculate numerical flux using Godunov scheme.
        
        Args:
            rho_left: Density on the left side of interface
            rho_right: Density on the right side of interface
            
        Returns:
            Numerical flux (vehicles/h)
        """
        # Convert inputs to arrays for consistent handling
        rho_left_arr = np.asarray(rho_left)
        rho_right_arr = np.asarray(rho_right)
        rho_c = self.critical_density()
        
        # Calculate flows using vectorized operations
        f_left = self.get_flow(rho_left_arr)
        f_right = self.get_flow(rho_right_arr)
        f_critical = self.get_flow(rho_c)
        
        # Initialize result array
        if rho_left_arr.shape == rho_right_arr.shape:
            result = np.zeros_like(rho_left_arr, dtype=float)
        else:
            # Handle broadcasting - create output with broadcast shape
            result = np.zeros(np.broadcast(rho_left_arr, rho_right_arr).shape, dtype=float)
        
        # Apply Godunov flux logic using NumPy's where function
        # Case 1: rho_left <= rho_right
        mask1 = rho_left_arr <= rho_right_arr
        
        # Case 1a: rho_left >= rho_c
        mask1a = np.logical_and(mask1, rho_left_arr >= rho_c)
        result = np.where(mask1a, f_left, result)
        
        # Case 1b: rho_right <= rho_c
        mask1b = np.logical_and(mask1, rho_right_arr <= rho_c)
        result = np.where(mask1b, f_right, result)
        
        # Case 1c: rho_left < rho_c < rho_right
        mask1c = np.logical_and(mask1, 
                              np.logical_and(rho_left_arr < rho_c, rho_right_arr > rho_c))
        result = np.where(mask1c, f_critical, result)
        
        # Case 2: rho_left > rho_right
        mask2 = rho_left_arr > rho_right_arr
        
        # Case 2a: rho_left <= rho_c
        mask2a = np.logical_and(mask2, rho_left_arr <= rho_c)
        result = np.where(mask2a, f_left, result)
        
        # Case 2b: rho_right >= rho_c
        mask2b = np.logical_and(mask2, rho_right_arr >= rho_c)
        result = np.where(mask2b, f_right, result)
        
        # Case 2c: rho_right < rho_c < rho_left
        mask2c = np.logical_and(mask2, 
                              np.logical_and(rho_right_arr < rho_c, rho_left_arr > rho_c))
        result = np.where(mask2c, f_critical, result)
        
        # Handle scalar inputs - return scalar output
        if np.isscalar(rho_left) and np.isscalar(rho_right):
            return float(result.item()) if result.size == 1 else float(result[0])
            
        return result
    
    def calculate_dt(self, rho, dx, cfl_factor=0.9):
        """
        Calculate time step based on CFL condition using maximum wave speed.
        
        Args:
            rho: Current density array
            dx: Spatial step size (km)
            cfl_factor: Safety factor for CFL condition (0-1)
            
        Returns:
            Time step (h)
        """
        # Calculate the maximum wave speed as max|dq/dρ| across the domain
        # For the Greenshields model, the derivative of the flux function is:
        # dq/dρ = v_max*(1 - 2*ρ/ρ_max)
        # This reaches its maximum absolute value at either ρ=0 or ρ=ρ_max
        
        # Convert input to array for consistent handling
        rho_array = np.asarray(rho)
        
        # Calculate wave speeds at each point
        wave_speed = self.v_max * (1 - 2 * rho_array / self.rho_max)
        
        # Maximum absolute wave speed across the domain
        max_wave_speed = max(
            self.v_max,  # Wave speed at ρ=0
            abs(np.min(wave_speed))  # Maximum negative wave speed
        )
        
        # Apply CFL condition: dt ≤ dx / max_wave_speed
        dt = cfl_factor * dx / max_wave_speed
        
        return float(dt)  # Ensure scalar output
    
    def simulate(self, initial_density, domain_length, simulation_time, dx, dt=None, 
                cfl_factor=0.9, road_quality_func=None):
        """
        Solve the LWR model using Godunov's scheme.
        
        Args:
            initial_density: Initial density distribution (array or function)
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
        
        # Initialize density
        if callable(initial_density):
            rho = np.array([initial_density(xi) for xi in x])
        else:
            rho = np.array(initial_density)
        
        # Apply road quality if provided - simplified to avoid over-complicating v_max
        v_max_original = None
        if road_quality_func is not None:
            # Store original v_max (always scalar)
            v_max_original = self.v_max
            # Calculate road quality at each point
            road_quality = np.array([road_quality_func(xi) for xi in x])
            # Scalar multiplication distributes correctly
            self.v_max = v_max_original * float(np.mean(road_quality))
        
        # Calculate time step if not provided
        if dt is None:
            dt = self.calculate_dt(rho, dx, cfl_factor)
        
        # Create time grid
        nt = int(simulation_time / dt) + 1
        t = np.linspace(0, simulation_time, nt)
        
        # Initialize result arrays
        density = np.zeros((nt, nx))
        velocity = np.zeros((nt, nx))
        flow = np.zeros((nt, nx))
        
        # Set initial conditions
        density[0] = rho
        velocity[0] = self.get_velocity(rho)
        flow[0] = self.get_flow(rho)
        
        # Main time integration loop - simplified to just process one interface at a time
        for n in range(nt - 1):
            flux = np.zeros(nx + 1)
            
            # Process each interface individually
            for j in range(1, nx):
                try:
                    # Simple scalar values for this interface
                    flux[j] = self.godunov_flux(rho[j-1], rho[j])
                except Exception as e:
                    print(f"Error at timestep {n}, cell {j}: {e}")
                    # Fallback: take minimum of left and right flows
                    flux[j] = min(self.get_flow(rho[j-1]), self.get_flow(rho[j]))
            
            # Boundary conditions
            flux[0] = flux[1]
            flux[nx] = flux[nx-1]
            
            # Update density using conservative formula
            rho = rho - dt / dx * (flux[1:] - flux[:-1])
            
            # Ensure non-negative density
            rho = np.maximum(0, rho)
            
            # Store results
            density[n+1] = rho
            velocity[n+1] = self.get_velocity(rho)
            flow[n+1] = self.get_flow(rho)
        
        # Restore original v_max before returning
        if v_max_original is not None:
            self.v_max = v_max_original
        
        # Return results as dictionary
        return {
            'density': density,
            'velocity': velocity,
            'flow': flow,
            'grid_x': x,
            'grid_t': t,
            'parameters': {
                'v_max': self.v_max,
                'rho_max': self.rho_max,
                'dx': dx,
                'dt': dt,
                'domain_length': domain_length,
                'simulation_time': simulation_time
            }
        }
