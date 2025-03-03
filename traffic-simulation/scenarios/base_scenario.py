"""
Base Scenario

This module defines the BaseScenario class that serves as a foundation for all
traffic simulation scenarios. It provides common functionality for setting up,
running, and analyzing traffic simulations.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import time


class BaseScenario:
    """Base class for all traffic simulation scenarios."""
    
    def __init__(self, model, name="BaseScenario"):
        """
        Initialize a base scenario.
        
        Args:
            model: Traffic model instance to use for simulation
            name: Name of the scenario
        """
        self.model = model
        self.name = name
        self.params = None
        self.results = None
        
        # Default parameters
        self.default_params = {
            'domain_length': 20.0,  # km
            'simulation_time': 1.0,  # hours
            'dx': 0.1,              # spatial step (km)
            'dt': None,             # time step (h), if None calculated from CFL
            'cfl_factor': 0.9,      # safety factor for CFL condition
            'output_dir': 'results'  # directory for output files
        }
    
    def get_initial_density(self, x):
        """
        Get initial density at position x.
        This method should be overridden by subclasses.
        
        Args:
            x: Position (km)
            
        Returns:
            float or array: Initial density at position x (veh/km)
            
        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError("Subclasses must implement get_initial_density")
    
    def get_road_quality(self):
        """
        Define road quality function.
        This method may be overridden by subclasses.
        
        Returns:
            function: A function that takes position x and returns quality coefficient
        """
        # Default: uniform road quality (perfect condition)
        return lambda x: 1.0
    
    def get_boundary_conditions(self):
        """
        Define boundary conditions.
        This method may be overridden by subclasses.
        
        Returns:
            tuple: (left_bc, right_bc) functions or values
        """
        # Default: zero-gradient (Neumann) boundary conditions
        return None, None
    
    def get_source_terms(self):
        """
        Define source terms (e.g., for intersections).
        This method may be overridden by subclasses.
        
        Returns:
            function: A function that takes (x, t) and returns source value
        """
        # Default: no sources or sinks
        return lambda x, t: 0.0
    
    def prepare_simulation(self, params=None):
        """
        Prepare the simulation by setting up parameters and initial conditions.
        
        Args:
            params: Dictionary of simulation parameters (optional)
            
        Returns:
            dict: Dictionary of prepared parameters
        """
        # Use provided params, fall back to defaults if needed
        if params is None:
            params = {}
        
        # Merge with default parameters
        merged_params = self.default_params.copy()
        merged_params.update(params)
        self.params = merged_params
        
        # Create output directory if needed
        os.makedirs(self.params['output_dir'], exist_ok=True)
        
        return self.params
    
    def run(self, params=None):
        """
        Run simulation for this scenario with specified parameters.
        
        Args:
            params: Dictionary of simulation parameters (optional)
                  
        Returns:
            Dictionary containing simulation results
        """
        # Ensure we have a valid parameters dictionary
        if params is None:
            self.params = self.default_params
        else:
            # Create a merged parameters dictionary (default values + provided values)
            # Start with defaults
            merged_params = self.default_params.copy()
            # Update with provided params
            merged_params.update(params)
            self.params = merged_params
        
        # Log the start of the simulation
        print(f"Running {self.name} simulation...")
        
        # Define initial density function
        initial_density = lambda x: self.get_initial_density(x)
        
        # Get road quality function if implemented
        road_quality_func = self.get_road_quality() if hasattr(self, 'get_road_quality') else None
        
        # Run the simulation
        results = self.model.simulate(
            initial_density=initial_density,
            domain_length=self.params['domain_length'],
            simulation_time=self.params['simulation_time'],
            dx=self.params['dx'],
            dt=self.params.get('dt', None),
            cfl_factor=self.params.get('cfl_factor', 0.9),
            road_quality_func=road_quality_func
        )
        
        # Add scenario information to results
        results['name'] = self.name
        if hasattr(self, 'description'):
            results['description'] = self.description
        else:
            results['description'] = f"Simulation of {self.name} scenario"
        
        return results
    
    def analyze(self):
        """
        Analyze simulation results.
        
        Returns:
            dict: Dictionary containing analysis results
            
        Raises:
            ValueError: If simulation has not been run yet
        """
        if self.results is None:
            raise ValueError("No simulation results available. Run simulation first.")
        
        analysis = {}
        
        # Extract basic metrics
        density = self.results['density']
        velocity = self.results['velocity']
        flow = self.results['flow']
        
        # Calculate global statistics
        analysis['mean_density'] = np.mean(density)
        analysis['max_density'] = np.max(density)
        analysis['mean_velocity'] = np.mean(velocity)
        analysis['mean_flow'] = np.mean(flow)
        analysis['max_flow'] = np.max(flow)
        
        # Find bottlenecks (locations with consistently high density)
        avg_density_profile = np.mean(density, axis=0)
        bottleneck_threshold = 0.7 * np.max(avg_density_profile)
        bottleneck_indices = np.where(avg_density_profile > bottleneck_threshold)[0]
        
        if len(bottleneck_indices) > 0:
            bottleneck_positions = [self.results['grid_x'][idx] for idx in bottleneck_indices]
            bottleneck_densities = [avg_density_profile[idx] for idx in bottleneck_indices]
            
            # Group adjacent bottlenecks
            bottleneck_groups = []
            current_group = [bottleneck_positions[0]]
            current_group_densities = [bottleneck_densities[0]]
            
            for i in range(1, len(bottleneck_positions)):
                if bottleneck_positions[i] - bottleneck_positions[i-1] <= 2 * self.params['dx']:
                    # Add to current group
                    current_group.append(bottleneck_positions[i])
                    current_group_densities.append(bottleneck_densities[i])
                else:
                    # Start new group
                    if current_group:
                        bottleneck_groups.append({
                            'positions': current_group,
                            'densities': current_group_densities,
                            'mean_position': np.mean(current_group),
                            'mean_density': np.mean(current_group_densities),
                            'length': current_group[-1] - current_group[0]
                        })
                    current_group = [bottleneck_positions[i]]
                    current_group_densities = [bottleneck_densities[i]]
            
            # Add last group
            if current_group:
                bottleneck_groups.append({
                    'positions': current_group,
                    'densities': current_group_densities,
                    'mean_position': np.mean(current_group),
                    'mean_density': np.mean(current_group_densities),
                    'length': current_group[-1] - current_group[0] if len(current_group) > 1 else 0
                })
                
            analysis['bottlenecks'] = bottleneck_groups
        else:
            analysis['bottlenecks'] = []
        
        # Travel time calculation (based on average velocity)
        grid_x = self.results['grid_x']
        dx = grid_x[1] - grid_x[0]
        travel_time = 0
        
        for i in range(len(grid_x) - 1):
            # Time to travel through segment = distance / average velocity
            segment_velocity = np.mean(velocity[:, i])
            if segment_velocity > 0:
                travel_time += dx / segment_velocity
                
        analysis['travel_time'] = travel_time  # hours
        
        self.analysis = analysis
        return analysis
    
    def save_results(self, filename=None):
        """
        Save simulation results to disk.
        
        Args:
            filename: Name of file to save results (default: scenario name)
            
        Returns:
            str: Path to saved file
            
        Raises:
            ValueError: If simulation has not been run yet
        """
        if self.results is None:
            raise ValueError("No simulation results available. Run simulation first.")
            
        if filename is None:
            filename = f"{self.name.lower().replace(' ', '_')}.npz"
            
        output_path = os.path.join(self.params['output_dir'], filename)
        
        # Save results as compressed numpy archive
        np.savez_compressed(
            output_path,
            density=self.results['density'],
            velocity=self.results['velocity'],
            flow=self.results['flow'],
            grid_x=self.results['grid_x'],
            grid_t=self.results['grid_t'],
            params=np.array([self.params], dtype=object)
        )
        
        print(f"Results saved to {output_path}")
        return output_path
    
    @staticmethod
    def load_results(filepath):
        """
        Load simulation results from disk.
        
        Args:
            filepath: Path to saved results file
            
        Returns:
            dict: Dictionary containing simulation results
        """
        data = np.load(filepath, allow_pickle=True)
        
        results = {
            'density': data['density'],
            'velocity': data['velocity'],
            'flow': data['flow'],
            'grid_x': data['grid_x'],
            'grid_t': data['grid_t'],
            'params': data['params'].item()
        }
        
        return results
