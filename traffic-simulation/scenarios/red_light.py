"""
Red Light Scenario

This module implements a traffic scenario with vehicles stopping at a red light
and then accelerating when the light turns green.
"""

import numpy as np
from .base_scenario import BaseScenario


class RedLightScenario(BaseScenario):
    """
    Red light scenario for traffic simulation.
    
    This scenario simulates traffic approaching a red light, forming a queue,
    and then accelerating when the light turns green.
    """
    
    def __init__(self, model, name="RedLight"):
        """
        Initialize the red light scenario.
        
        Args:
            model: Traffic model instance
            name: Name for this scenario
        """
        super().__init__(model, name)
        
        # Add description attribute
        self.description = "Simulation of traffic stopping at a red light and then accelerating when the light turns green. Shows the formation and dissipation of congestion at a signalized intersection."
        
        # Override default parameters
        self.default_params.update({
            'domain_length': 5.0,    # km
            'simulation_time': 0.25,  # hours
            'dx': 0.05,              # spatial step (km)
            'light_position': 3.0,   # position of the traffic light (km)
            'background_density': 0.2,  # background density ratio
            'jam_density': 0.9,      # jam density ratio at the light
            'jam_length': 0.5,       # length of the jam upstream of light (km)
            'green_time': 0.05       # time when the light turns green (h)
        })
    
    def get_initial_density(self, x):
        """
        Get initial density distribution with congestion at the traffic light.
        
        Args:
            x: Position (km)
            
        Returns:
            float or array: Initial density at position x
        """
        params = self.params if self.params is not None else self.default_params
        light_position = params['light_position']
        jam_length = params['jam_length']
        
        # Check if model is multiclass or single-class
        if hasattr(self.model, 'n_classes'):  # Multiclass model
            densities = []
            
            # Traffic jam upstream of the light
            if light_position - jam_length <= x <= light_position:
                # Traffic jam - higher density
                for i, vc in enumerate(self.model.vehicle_classes):
                    if i == 0:  # Motorcycles - accumulate at the front
                        # More motorcycles near the light (front of queue)
                        proximity_to_light = (x - (light_position - jam_length)) / jam_length
                        density_factor = params['jam_density'] * (1 + 0.3 * proximity_to_light)
                        densities.append(min(density_factor, 0.95) * vc.rho_max)
                    else:  # Other vehicles - uniform distribution in the jam
                        densities.append(params['jam_density'] * vc.rho_max)
            else:
                # Light background traffic
                for vc in self.model.vehicle_classes:
                    densities.append(params['background_density'] * vc.rho_max)
            
            return densities
        
        else:  # Single-class LWR model
            # Traffic jam upstream of the light
            if light_position - jam_length <= x <= light_position:
                # Simple traffic jam with uniform density
                return float(params['jam_density'] * self.model.rho_max)
            else:
                # Background traffic elsewhere
                return float(params['background_density'] * self.model.rho_max)
    
    def get_road_quality(self):
        """
        Get road quality coefficient (uniform quality for this scenario).
        
        Returns:
            function: A function that takes position x and returns quality coefficient
        """
        # Uniform road quality for this scenario
        return lambda x: 1.0
    
    def run(self, params=None):
        """
        Run the scenario simulation with a traffic light that turns green.
        
        Args:
            params: Dictionary of simulation parameters (optional)
                  
        Returns:
            Dictionary containing simulation results
        """
        results = super().run(params)
        green_time = self.params['green_time']
        
        # Add traffic light information to results
        results['traffic_light'] = {
            'position': self.params['light_position'],
            'green_time': green_time
        }
        
        # Add annotation to plot title
        results['name'] += f" (Light turns green at t={green_time:.2f}h)"
        
        return results
