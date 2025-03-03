"""
Base Model for Traffic Simulation

This module provides the base implementation of the traffic simulation model,
including fundamental methods for traffic flow.
"""

import numpy as np

class BaseModel:
    """
    Base class for traffic simulation models.
    
    This class provides fundamental methods for traffic flow calculations.
    """
    
    def __init__(self, rho_max=180, v_max=100):
        """
        Initializes the base model with maximum density and speed.
        
        Args:
            rho_max: Maximum density (vehicles/km)
            v_max: Maximum speed (km/h)
        """
        self.rho_max = rho_max  # Maximum density (vehicles/km)
        self.v_max = v_max      # Maximum speed (km/h)

    def speed(self, rho):
        """
        Calculates the speed based on density.
        
        Args:
            rho: Density of traffic (vehicles/km)
            
        Returns:
            Speed of traffic (km/h)
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def flow(self, rho):
        """
        Calculates the flow based on density.
        
        Args:
            rho: Density of traffic (vehicles/km)
            
        Returns:
            Flow of traffic (vehicles/h)
        """
        raise NotImplementedError("This method should be implemented by subclasses.")

    def critical_density(self):
        """
        Calculates the critical density (density at maximum flow).
        
        Returns:
            Critical density (vehicles/km)
        """
        return self.rho_max / 2

    def capacity(self):
        """
        Calculates the capacity of the road (maximum flow).
        
        Returns:
            Maximum flow (vehicles/h)
        """
        return self.flow(self.critical_density())