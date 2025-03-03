"""
Vehicle Class Modulation Functions

This module provides functions to model the specific behaviors of different
vehicle classes, especially the interactions between motorcycles and other vehicles
like gap-filling and interweaving.
"""

import numpy as np


def gap_filling_modulation(rho_moto, rho_max_moto, gamma=0.3):
    """
    Calculate the gap-filling modulation factor for motorcycles.
    
    This function models how motorcycles can effectively utilize the gaps
    between larger vehicles, potentially increasing their effective velocity.
    
    Args:
        rho_moto: Motorcycle density (veh/km)
        rho_max_moto: Maximum motorcycle density (veh/km)
        gamma: Gap-filling coefficient (0-1)
        
    Returns:
        float: Modulation factor for motorcycle velocity
    """
    # Ensure parameters are within valid ranges
    gamma = max(0.0, min(1.0, gamma))
    
    # Basic gap-filling formula from Benin research
    modulation = 1.0 + gamma * (rho_moto / rho_max_moto)
    
    return modulation


def interweaving_modulation(rho_moto, rho_max_moto, beta=0.3):
    """
    Calculate the interweaving modulation factor for non-motorcycle vehicles.
    
    This function models how the presence of motorcycles can negatively impact
    the flow of larger vehicles due to their zigzag movements.
    
    Args:
        rho_moto: Motorcycle density (veh/km)
        rho_max_moto: Maximum motorcycle density (veh/km)
        beta: Interweaving sensitivity coefficient (0-1)
        
    Returns:
        float: Modulation factor for non-motorcycle velocity
    """
    # Ensure parameters are within valid ranges
    beta = max(0.0, min(1.0, beta))
    
    # Basic interweaving formula from Benin research
    modulation = 1.0 - beta * (rho_moto / rho_max_moto)
    
    # Ensure modulation doesn't go negative
    return max(0.1, modulation)


def calculate_modulation(class_idx, rho_moto, rho_max_moto, params):
    """
    Calculate the appropriate modulation factor based on vehicle class.
    
    Args:
        class_idx: Index of the vehicle class (0 for motorcycles)
        rho_moto: Motorcycle density (veh/km)
        rho_max_moto: Maximum motorcycle density (veh/km)
        params: Dictionary of modulation parameters
        
    Returns:
        float: Modulation factor for velocity
    """
    if class_idx == 0:  # Motorcycle class
        gamma = params.get('gamma', 0.3)
        return gap_filling_modulation(rho_moto, rho_max_moto, gamma)
    else:  # Other vehicle classes
        beta = params.get(f'beta_{class_idx}', 0.3)
        return interweaving_modulation(rho_moto, rho_max_moto, beta)


def road_quality_coefficient(road_type, vehicle_class):
    """
    Determine road quality coefficient for different road types and vehicle classes.
    
    Args:
        road_type: String indicating road type ('bitumen', 'gravel', 'dirt', etc.)
        vehicle_class: Vehicle class index or name
        
    Returns:
        float: Road quality coefficient (0-1)
    """
    # Define baseline coefficients for each road type
    coefficients = {
        'bitumen_good': 1.0,
        'bitumen_poor': 0.8,
        'paved': 0.9,
        'gravel': 0.7,
        'dirt': 0.5,
        'damaged': 0.4
    }
    
    # Define class-specific modifiers (motorcycles are less affected)
    class_modifiers = {
        0: 0.2,  # Motorcycles
        1: 0.0,  # Cars
        2: -0.1  # Trucks/buses
    }
    
    # Get the base coefficient, default to 0.5 if not found
    base_coef = coefficients.get(road_type, 0.5)
    
    # Apply class modifier, default to 0.0 if class not found
    modifier = class_modifiers.get(vehicle_class, 0.0)
    
    # Calculate final coefficient, ensuring it stays within [0.1, 1.0]
    final_coef = min(1.0, max(0.1, base_coef + modifier))
    
    return final_coef
