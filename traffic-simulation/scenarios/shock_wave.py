"""
Shock Wave Scenario

This module implements a scenario with a shock wave, where traffic
transitions from a free-flow state to a congested state.
"""

import numpy as np
from .base_scenario import BaseScenario


class ShockWaveScenario(BaseScenario):
    """
    Shock wave scenario where initially free-flowing traffic becomes congested.
    
    This scenario simulates the formation of a shock wave when vehicles
    transition from free flow to congested conditions. It's the opposite
    of a rarefaction wave and is commonly observed in real traffic when
    vehicles encounter sudden slowdowns.
    """
    
    def __init__(self, model, name="ShockWave"):
        """
        Initialize the shock wave scenario.
        
        Args:
            model: Traffic model instance
            name: Name for this scenario
        """
        super().__init__(model, name)
        
        # Add description attribute to fix error in BaseScenario.run()
        self.description = "Simulation of a shock wave where traffic transitions from a free-flow state (density ratio 0.1) to a congested state (density ratio 0.7). This scenario demonstrates how traffic compresses when lighter traffic meets denser traffic ahead."
        
        # Override default parameters for this specific scenario
        self.default_params.update({
            'domain_length': 20.0,  # km
            'simulation_time': 0.5,  # hours
            'dx': 0.1,              # spatial step (km)
            'upstream_density': 0.1, # Ratio of maximum density (light)
            'downstream_density': 0.7, # Ratio of maximum density (dense)
            'transition_point': 0.5  # Position of density jump (ratio of domain)
        })
    
    def get_initial_density(self, x):
        """
        Get initial density distribution with a low-to-high transition.
        
        Args:
            x: Position (km)
            
        Returns:
            float: Initial density at position x (veh/km)
        """
        # Get parameters with defaults if not provided
        params = self.params if self.params is not None else self.default_params
        
        # Make sure transition_point exists in params
        if 'transition_point' not in params:
            params = params.copy()
            params['transition_point'] = self.default_params.get('transition_point', 0.5)
        
        transition_point = params['transition_point'] * params['domain_length']
        
        # Upstream (left) is light, downstream (right) is dense - opposite of rarefaction
        if hasattr(self.model, 'n_classes'):  # Multiclass model
            # Handle multiclass model (similar to rarefaction but densities swapped)
            if x <= transition_point:
                # Light upstream condition
                densities = []
                for i, vc in enumerate(self.model.vehicle_classes):
                    densities.append(params['upstream_density'] * vc.rho_max)
                return densities
            else:
                # Dense downstream condition
                densities = []
                for i, vc in enumerate(self.model.vehicle_classes):
                    # Different distribution for different classes
                    ratio = params['downstream_density']
                    if i == 0:  # First class (motorcycles) even denser
                        ratio *= 1.2
                    densities.append(ratio * vc.rho_max)
                return densities
        else:
            # Single class model
            if x <= transition_point:
                return float(params['upstream_density'] * self.model.rho_max)
            else:
                return float(params['downstream_density'] * self.model.rho_max)
    
    def get_road_quality(self):
        """
        Get road quality coefficient (uniform quality for this scenario).
        
        Returns:
            function: A function that takes position x and returns quality coefficient
        """
        # Uniform road quality for this basic scenario
        return lambda x: 1.0
