"""
Traffic Simulation Plotter

This module provides visualization tools for traffic simulation results,
with support for density, velocity, and flow plots.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

class TrafficPlotter:
    """Class for creating traffic simulation visualizations."""
    
    def __init__(self, output_dir='simulations', model_name=None):
        """
        Initialize the plotter.
        
        Args:
            output_dir: Base directory for saving plots
            model_name: Name of the model (e.g., 'LWR', 'Extended')
        """
        self.output_dir = output_dir
        self.model_name = model_name if model_name else "default"
    
    def plot_density(self, results, save=True, show=False):
        """
        Create density evolution plot.
        
        Args:
            results: Dictionary containing simulation results
            save: Whether to save the plot to file
            show: Whether to display the plot
        """
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(
            results['grid_x'],
            results['grid_t'],
            results['density'],
            shading='auto',
            cmap='hot'
        )
        plt.colorbar(label='Densité (véhicules/km)')
        plt.xlabel('Position (km)')
        plt.ylabel('Temps (h)')
        plt.title(f'Évolution de la Densité - {results["name"]}')
        
        if save:
            output_path = f'{self.output_dir}/{self.model_name}/density/{results["name"]}_density.png'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
        if show:
            plt.show()
        plt.close()
    
    def plot_velocity(self, results, save=True, show=False):
        """
        Create velocity evolution plot.
        
        Args:
            results: Dictionary containing simulation results
            save: Whether to save the plot to file
            show: Whether to display the plot
        """
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(
            results['grid_x'],
            results['grid_t'],
            results['velocity'],
            shading='auto',
            cmap='viridis'
        )
        plt.colorbar(label='Vitesse (km/h)')
        plt.xlabel('Position (km)')
        plt.ylabel('Temps (h)')
        plt.title(f'Évolution de la Vitesse - {results["name"]}')
        
        if save:
            output_path = f'{self.output_dir}/{self.model_name}/velocity/{results["name"]}_velocity.png'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
        if show:
            plt.show()
        plt.close()
    
    def plot_flow(self, results, save=True, show=False):
        """
        Create flow evolution plot.
        
        Args:
            results: Dictionary containing simulation results
            save: Whether to save the plot to file
            show: Whether to display the plot
        """
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(
            results['grid_x'],
            results['grid_t'],
            results['flow'],
            shading='auto',
            cmap='plasma'
        )
        plt.colorbar(label='Flux (véhicules/h)')
        plt.xlabel('Position (km)')
        plt.ylabel('Temps (h)')
        plt.title(f'Évolution du Flux - {results["name"]}')
        
        if save:
            output_path = f'{self.output_dir}/{self.model_name}/flow/{results["name"]}_flow.png'
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
        if show:
            plt.show()
        plt.close()
    
    def plot_all(self, results, save=True, show=False):
        """
        Create all three plots (density, velocity, flow).
        
        Args:
            results: Dictionary containing simulation results
            save: Whether to save the plots to files
            show: Whether to display the plots
        """
        self.plot_density(results, save, show)
        self.plot_velocity(results, save, show)
        self.plot_flow(results, save, show)
