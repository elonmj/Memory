"""
Fundamental Diagram for Traffic Flow

This module defines the fundamental diagram for traffic flow, including relationships
between density, speed, and flow.
"""

import numpy as np

class FundamentalDiagram:
    """
    Class to represent the fundamental diagram of traffic flow.
    """

    def __init__(self, rho_max=180, v_max=100):
        """
        Initializes the fundamental diagram with maximum density and speed.

        Args:
            rho_max: Maximum density (vehicles/km)
            v_max: Maximum speed (km/h)
        """
        self.rho_max = rho_max  # Maximum density (vehicles/km)
        self.v_max = v_max      # Maximum speed (km/h)

    def speed(self, rho):
        """
        Speed-density relationship (Greenshields model):
        v(ρ) = v_max * (1 - ρ/ρ_max)
        
        Cette relation linéaire décrite à l'équation \ref{eq:greenshields_vitesse}
        représente la décroissance de la vitesse avec l'augmentation de la densité.

        Args:
            rho: Traffic density (vehicles/km)

        Returns:
            Speed of traffic (km/h)
        """
        return self.v_max * (1 - np.clip(rho / self.rho_max, 0, 1))

    def flow(self, rho):
        """
        Flow-density relationship (Diagramme fondamental):
        q(ρ) = ρ * v(ρ) = v_max * ρ * (1 - ρ/ρ_max)
        
        Cette relation parabolique décrite à l'équation \ref{eq:greenshields_flux}
        donne le flux en fonction de la densité. Elle est nulle pour ρ = 0 et ρ = ρ_max,
        et atteint son maximum à la densité critique ρ_c = ρ_max/2.

        Args:
            rho: Traffic density (vehicles/km)

        Returns:
            Traffic flow (vehicles/h)
        """
        return rho * self.speed(rho)

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
