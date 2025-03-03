"""
Rarefaction Wave Scenario

This module implements a scenario with a rarefaction wave, where traffic
transitions from a congested state to a free-flow state.
"""

import numpy as np
from .base_scenario import BaseScenario


class RarefactionWaveScenario(BaseScenario):
    """
    Rarefaction wave scenario where initially congested traffic disperses.
    
    This scenario simulates the formation of a rarefaction wave when vehicles
    transition from congested to free flow conditions. It's a fundamental
    traffic pattern that emerges when denser upstream traffic meets lighter
    downstream traffic.
    """
    
    def __init__(self, model, name="RarefactionWave"):
        """
        Initialize the rarefaction wave scenario.
        
        Args:
            model: Traffic model instance
            name: Name for this scenario
        """
        super().__init__(model, name)
        
        # Add description attribute to fix error in BaseScenario.run()
        self.description = "Simulation of a rarefaction wave where traffic transitions from a congested state (density ratio 0.7) to a free-flow state (density ratio 0.1). This scenario demonstrates how traffic disperses when higher density traffic meets lower density traffic ahead."
        
        # Override default parameters for this specific scenario
        self.default_params.update({
            'domain_length': 20.0,  # km
            'simulation_time': 0.5,  # hours
            'dx': 0.1,              # spatial step (km)
            'upstream_density': 0.7, # Ratio of maximum density
            'downstream_density': 0.1, # Ratio of maximum density
            'transition_point': 0.5  # Position of density jump (ratio of domain)
        })
    
    def get_initial_density(self, x):
        """
        Get initial density distribution with a high-to-low transition.
        
        Args:
            x: Position (km)
            
        Returns:
            float: Initial density at position x (veh/km)
        """
        # Get parameters with defaults if not provided
        params = self.params if self.params is not None else self.default_params
        
        # CRITICAL FIX: Make sure transition_point exists in params
        if 'transition_point' not in params:
            params = params.copy()  # Create a copy to avoid modifying the original
            params['transition_point'] = self.default_params.get('transition_point', 0.5)
        
        transition_point = params['transition_point'] * params['domain_length']
        
        # Upstream (left) is dense, downstream (right) is light
        if hasattr(self.model, 'n_classes'):  # Multiclass model
            # For multiclass, return array of densities
            if x <= transition_point:
                # Dense upstream condition
                densities = []
                for i, vc in enumerate(self.model.vehicle_classes):
                    # Different distribution for different classes
                    ratio = params['upstream_density']
                    if i == 0:  # First class (motorcycles) even denser
                        ratio *= 1.2
                    densities.append(ratio * vc.rho_max)
                return densities
            else:
                # Light downstream condition
                densities = []
                for vc in self.model.vehicle_classes:
                    densities.append(params['downstream_density'] * vc.rho_max)
                return densities
        else:
            # Single class model - ensure scalar output
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
