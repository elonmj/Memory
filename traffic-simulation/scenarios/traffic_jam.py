"""
Traffic Jam Scenario

This module implements a scenario that simulates a traffic jam formation
by having different densities in different regions of the domain.
"""

import numpy as np
from .base_scenario import BaseScenario


class TrafficJamScenario(BaseScenario):
    """
    Traffic Jam scenario that simulates congestion formation.
    
    This scenario creates a traffic jam by setting different initial densities
    in different regions of the road. It demonstrates the formation and
    propagation of traffic waves.
    """
    
    def __init__(self, model, name="TrafficJam"):
        """
        Initialize the traffic jam scenario.
        
        Args:
            model: Traffic model instance
            name: Name for this scenario
        """
        super().__init__(model, name)
        
        # Add description attribute
        self.description = "Simulation of traffic jam formation and propagation caused by density differences across road segments. Shows how congestion waves move through traffic."
        
        # Override default parameters
        self.default_params.update({
            'domain_length': 10.0,    # km
            'simulation_time': 0.5,   # hours
            'dx': 0.05,               # spatial step (km)
            'left_density': 0.7,      # Ratio of maximum density (left side)
            'right_density': 0.1,     # Ratio of maximum density (right side)
            'transition_width': 1.0,  # Width of the transition zone (km)
            'transition_point': 0.5,  # Position of density change (ratio of domain)
            'smooth_transition': True # Whether to use smooth transition or sharp
        })
    
    def get_initial_density(self, x):
        """
        Get initial density distribution with a traffic jam pattern.
        
        Args:
            x: Position (km)
            
        Returns:
            float or array: Initial density at position x
        """
        params = self.params if self.params is not None else self.default_params
        
        # Get parameters with defaults if not provided
        left_density = params.get('left_density', 0.7)
        right_density = params.get('right_density', 0.1)
        transition_point = params.get('transition_point', 0.5) * params['domain_length']
        transition_width = params.get('transition_width', 1.0)
        smooth_transition = params.get('smooth_transition', True)
        
        # Convert density ratios to actual densities
        if hasattr(self.model, 'n_classes'):  # Multiclass model
            # For multiclass, we'll return an array of densities
            if smooth_transition:
                # Smooth transition for each class
                densities = []
                for i, vc in enumerate(self.model.vehicle_classes):
                    # Apply class-specific adjustments
                    left_factor = left_density
                    right_factor = right_density
                    
                    # Motorcycles can squeeze through, so slightly higher density
                    if i == 0:  # Assuming first class is motorcycles
                        left_factor *= 1.2
                    
                    # Calculate density with smooth transition
                    if x < transition_point - transition_width/2:
                        densities.append(left_factor * vc.rho_max)
                    elif x > transition_point + transition_width/2:
                        densities.append(right_factor * vc.rho_max)
                    else:
                        # Linear interpolation in the transition zone
                        t = (x - (transition_point - transition_width/2)) / transition_width
                        density_factor = left_factor + t * (right_factor - left_factor)
                        densities.append(density_factor * vc.rho_max)
                return densities
            else:
                # Sharp transition
                densities = []
                for i, vc in enumerate(self.model.vehicle_classes):
                    left_factor = left_density
                    right_factor = right_density
                    
                    # Motorcycles adjustment
                    if i == 0:
                        left_factor *= 1.2
                        
                    densities.append((left_factor if x <= transition_point else right_factor) * vc.rho_max)
                return densities
        else:
            # Single-class LWR model - return a single density value
            if smooth_transition:
                if x < transition_point - transition_width/2:
                    return float(left_density * self.model.rho_max)
                elif x > transition_point + transition_width/2:
                    return float(right_density * self.model.rho_max)
                else:
                    # Linear interpolation in the transition zone
                    t = (x - (transition_point - transition_width/2)) / transition_width
                    density_factor = left_density + t * (right_density - left_density)
                    return float(density_factor * self.model.rho_max)
            else:
                # Sharp transition
                return float((left_density if x <= transition_point else right_density) * self.model.rho_max)
    
    def get_road_quality(self):
        """
        Get road quality coefficient (uniform quality for this scenario).
        
        Returns:
            function: A function that takes position x and returns quality coefficient
        """
        # Uniform road quality for this scenario
        return lambda x: 1.0