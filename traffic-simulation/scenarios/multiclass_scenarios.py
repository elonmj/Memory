"""
Multiclass Traffic Scenarios

This module implements various scenarios specifically designed to demonstrate
the capabilities of the multiclass traffic model, with particular focus on
motorcycle behavior.
"""

import numpy as np
from .base_scenario import BaseScenario


class MulticlassRedLightScenario(BaseScenario):
    """
    Red light scenario for multiclass traffic.
    
    This scenario simulates traffic stopping at a red light and then
    reaccelerating when the light turns green, with different classes
    of vehicles showing distinctive behaviors.
    """
    
    def __init__(self, model, name="MulticlassRedLight"):
        """
        Initialize the red light scenario.
        
        Args:
            model: Multiclass traffic model instance
            name: Name for this scenario
        """
        super().__init__(model, name)
        
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
            array: Initial densities for each vehicle class at position x
        """
        params = self.params if self.params is not None else self.default_params
        light_position = params['light_position']
        jam_length = params['jam_length']
        
        # Check if multiclass model
        if not hasattr(self.model, 'n_classes'):
            raise ValueError("MulticlassRedLightScenario requires a multiclass model")
        
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


class DegradedRoadScenario(BaseScenario):
    """
    Scenario with varying road quality along the domain.
    
    This scenario demonstrates how different vehicle classes react
    to changes in road quality (potholes, unpaved sections, etc.).
    """
    
    def __init__(self, model, name="DegradedRoad"):
        """
        Initialize the degraded road scenario.
        
        Args:
            model: Multiclass traffic model instance
            name: Name for this scenario
        """
        super().__init__(model, name)
        
        # Override default parameters
        self.default_params.update({
            'domain_length': 10.0,   # km
            'simulation_time': 0.2,  # hours
            'dx': 0.05,              # spatial step (km)
            'density': 0.3,          # uniform density ratio
            'degraded_start': 3.0,   # start of degraded section (km)
            'degraded_end': 7.0,     # end of degraded section (km)
            'quality_good': 1.0,     # road quality coefficient for good sections
            'quality_bad': 0.6       # road quality coefficient for degraded section
        })
    
    def get_initial_density(self, x):
        """
        Get uniform initial density distribution.
        
        Args:
            x: Position (km)
            
        Returns:
            array: Initial densities for each vehicle class at position x
        """
        params = self.params if self.params is not None else self.default_params
        
        # Check if multiclass model
        if not hasattr(self.model, 'n_classes'):
            raise ValueError("DegradedRoadScenario requires a multiclass model")
        
        # Uniform initial density for all classes
        densities = []
        for vc in self.model.vehicle_classes:
            densities.append(params['density'] * vc.rho_max)
        
        return densities
    
    def get_road_quality(self):
        """
        Define road quality function with a degraded section.
        
        Returns:
            function: A function that takes position x and returns quality coefficient
        """
        params = self.params if self.params is not None else self.default_params
        
        def road_quality(x):
            if params['degraded_start'] <= x <= params['degraded_end']:
                return params['quality_bad']
            else:
                return params['quality_good']
        
        return road_quality


class GapFillingScenario(BaseScenario):
    """
    Gap filling scenario to test motorcycle interweaving behavior.
    
    This scenario simulates a section of road where motorcycles can fill gaps
    between larger vehicles, demonstrating the gap-filling behavior of motorcycles
    in mixed traffic.
    """
    
    def __init__(self, model, name="GapFilling"):
        """Initialize the gap filling scenario."""
        super().__init__(model, name)
        
        # Override default parameters with all required parameters
        self.default_params.update({
            'domain_length': 20.0,  # km
            'simulation_time': 1.0,  # hours
            'dx': 0.1,              # spatial step (km)
            'upstream_density': 0.4, # Ratio of maximum density
            'downstream_density': 0.3, # Ratio of maximum density
            'transition_point': 0.5,  # Position of density jump (ratio of domain)
            'buffer_length': 2.0,     # Buffer zone length (km)
            'car_factor': 0.7,        # Car density factor
            'moto_factor': 1.2,       # Motorcycle density factor
            'car_density_ratio': 0.5,  # Default car density ratio
            'moto_density_ratios': [0.2, 0.4, 0.6, 0.8]  # Default motorcycle density ratios
        })
        
        # Description of the scenario
        self.description = "This scenario tests how motorcycles fill gaps between cars."
    
    def get_initial_density(self, x):
        """
        Get initial density with different motorcycle densities in segments.
        """
        params = self.params if self.params is not None else self.default_params
        
        # CRITICAL FIX: Make sure all required parameters are defined with fallbacks
        required_params = ['buffer_length', 'transition_point', 'domain_length', 
                          'upstream_density', 'downstream_density', 'car_factor', 'moto_factor']
        
        # Clone params if we need to add any missing parameters
        if any(param not in params for param in required_params):
            params = params.copy()
            
        # Add any missing parameters with default values
        for param in required_params:
            if param not in params:
                params[param] = self.default_params[param]
        
        # Use a transition point approach rather than segments
        transition_point = params['transition_point'] * params['domain_length']
        
        # Initialize densities for each class
        densities = []
        for i, vc in enumerate(self.model.vehicle_classes):
            if i == 0:  # Motorcycles
                if x <= transition_point:
                    # Upstream section - higher motorcycle density
                    densities.append(params['upstream_density'] * params['moto_factor'] * vc.rho_max)
                else:
                    # Downstream section - lower motorcycle density
                    densities.append(params['downstream_density'] * params['moto_factor'] * vc.rho_max)
            else:  # Cars and other vehicles
                if x <= transition_point:
                    # Upstream section
                    densities.append(params['upstream_density'] * params['car_factor'] * vc.rho_max)
                else:
                    # Downstream section
                    densities.append(params['downstream_density'] * params['car_factor'] * vc.rho_max)
        
        return densities

    def run(self, params=None):
        """Run the scenario and add segment information to results."""
        # CRITICAL FIX: Ensure all required parameters are included
        if params is None:
            params = {}
        
        # Make a copy of params to avoid modifying the original
        params = params.copy()
        
        # Add all required parameters that might be missing
        required_params = ['buffer_length', 'transition_point', 'domain_length', 
                          'upstream_density', 'downstream_density', 'car_factor', 'moto_factor']
        
        # Add any missing parameters with default values
        for param in required_params:
            if param not in params and param in self.default_params:
                params[param] = self.default_params[param]
        
        # Call the parent class run method
        results = super().run(params)
        
        # Add segment information to results for visualization
        transition_point = self.params['transition_point'] * self.params['domain_length']
        results['segments'] = [
            {
                'start': 0,
                'end': transition_point,
                'name': 'Upstream (higher density)',
                'moto_factor': self.params['moto_factor'],
                'car_factor': self.params['car_factor']
            },
            {
                'start': transition_point,
                'end': self.params['domain_length'],
                'name': 'Downstream (lower density)',
                'moto_factor': self.params['moto_factor'],
                'car_factor': self.params['car_factor']
            }
        ]
        
        return results
