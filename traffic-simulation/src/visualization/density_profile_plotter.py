"""
Density Profile Plotter

This module provides specialized visualization tools for creating and comparing
spatial and temporal density profiles across different simulation scenarios.
"""

import numpy as np
import matplotlib.pyplot as plt
import os


class DensityProfilePlotter:
    """Class for creating and comparing density profile visualizations."""
    
    def __init__(self, output_dir="simulations/profiles"):
        """
        Initialize the plotter with an output directory.
        
        Args:
            output_dir: Directory for saving plots
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        # Default colors for different scenarios
        self.scenario_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
    def plot_spatial_profile(self, results_list, time_indices=None, labels=None, 
                           title="Density Profiles Comparison", show=False, save=True):
        """
        Plot spatial density profiles for multiple simulation results at selected times.
        
        Args:
            results_list: List of simulation result dictionaries
            time_indices: List of time indices to plot for each result
            labels: List of labels for each simulation result
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        if time_indices is None:
            # Default to middle time point for each result
            time_indices = [len(r['grid_t'])//2 for r in results_list]
            
        if labels is None:
            labels = [f"Scenario {i+1}" for i in range(len(results_list))]
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i, (results, t_idx) in enumerate(zip(results_list, time_indices)):
            color = self.scenario_colors[i % len(self.scenario_colors)]
            t_value = results['grid_t'][t_idx]
            ax.plot(results['grid_x'], results['density'][t_idx], 
                    label=f"{labels[i]} (t={t_value:.2f}h)", 
                    color=color, linewidth=2)
            
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Densité (véh/km)')
        ax.set_title(title)
        ax.grid(True)
        ax.legend()
        
        if save:
            filename = title.replace(" ", "_").lower() if title else "density_profiles"
            plt.savefig(f'{self.output_dir}/{filename}.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_temporal_profile(self, results_list, positions=None, labels=None,
                             title="Density Time Evolution", show=False, save=True):
        """
        Plot temporal density profiles for multiple simulation results at selected positions.
        
        Args:
            results_list: List of simulation result dictionaries
            positions: List of spatial positions (km) to plot for each result
            labels: List of labels for each simulation result
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        if positions is None:
            # Default to middle position for each result
            positions = [r['grid_x'][len(r['grid_x'])//2] for r in results_list]
            
        if labels is None:
            labels = [f"Scenario {i+1}" for i in range(len(results_list))]
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i, (results, pos) in enumerate(zip(results_list, positions)):
            color = self.scenario_colors[i % len(self.scenario_colors)]
            # Find closest grid point to requested position
            pos_idx = np.argmin(np.abs(results['grid_x'] - pos))
            actual_pos = results['grid_x'][pos_idx]
            
            # Extract time series at this position
            density_time_series = results['density'][:, pos_idx]
            
            ax.plot(results['grid_t'], density_time_series, 
                    label=f"{labels[i]} (x={actual_pos:.2f}km)", 
                    color=color, linewidth=2)
            
        ax.set_xlabel('Temps (h)')
        ax.set_ylabel('Densité (véh/km)')
        ax.set_title(title)
        ax.grid(True)
        ax.legend()
        
        if save:
            filename = title.replace(" ", "_").lower() if title else "density_time_evolution"
            plt.savefig(f'{self.output_dir}/{filename}.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def create_profiles_dashboard(self, results, show=False, save=True):
        """
        Create a comprehensive dashboard showing density profiles at different times and positions.
        
        Args:
            results: Simulation result dictionary
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        fig = plt.figure(figsize=(15, 10))
        
        # Setup grid
        gs = plt.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Density evolution space-time plot
        ax1 = fig.add_subplot(gs[0, :])
        X, T = np.meshgrid(results['grid_x'], results['grid_t'])
        c1 = ax1.pcolormesh(X, T, results['density'], cmap='viridis', shading='auto')
        plt.colorbar(c1, ax=ax1, label='Densité (véh/km)')
        ax1.set_xlabel('Position (km)')
        ax1.set_ylabel('Temps (h)')
        ax1.set_title('Évolution Spatio-Temporelle de la Densité')
        
        # 2. Spatial density profiles at different times
        ax2 = fig.add_subplot(gs[1, 0])
        nt = len(results['grid_t'])
        time_indices = [0, nt//4, nt//2, 3*nt//4, nt-1]
        for idx in time_indices:
            t = results['grid_t'][idx]
            ax2.plot(results['grid_x'], results['density'][idx], label=f't = {t:.2f}h')
        ax2.set_xlabel('Position (km)')
        ax2.set_ylabel('Densité (véh/km)')
        ax2.set_title('Profils de Densité à Différents Temps')
        ax2.grid(True)
        ax2.legend()
        
        # 3. Temporal density profiles at different positions
        ax3 = fig.add_subplot(gs[1, 1])
        nx = len(results['grid_x'])
        pos_indices = [0, nx//4, nx//2, 3*nx//4, nx-1]
        for idx in pos_indices:
            x = results['grid_x'][idx]
            ax3.plot(results['grid_t'], results['density'][:, idx], label=f'x = {x:.2f}km')
        ax3.set_xlabel('Temps (h)')
        ax3.set_ylabel('Densité (véh/km)')
        ax3.set_title('Évolution Temporelle à Différentes Positions')
        ax3.grid(True)
        ax3.legend()
        
        plt.suptitle(f"Analyse des Profils de Densité : {results.get('name', 'Simulation')}", fontsize=16)
        
        if save:
            plt.savefig(f'{self.output_dir}/profiles_dashboard.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def compare_multiclass_profiles(self, results1, results2, class_idx=0, time_idx=None,
                                   title="Comparison of Class Density Profiles", show=False, save=True):
        """
        Compare density profiles of a specific vehicle class between two multiclass simulation results.
        
        Args:
            results1: First simulation result dictionary
            results2: Second simulation result dictionary
            class_idx: Index of vehicle class to compare
            time_idx: Time index to compare (if None, use middle time point)
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        if not ('class_densities' in results1 and 'class_densities' in results2):
            raise ValueError("Both result sets must contain multiclass density data")
            
        if time_idx is None:
            time_idx1 = len(results1['grid_t'])//2
            time_idx2 = len(results2['grid_t'])//2
        else:
            time_idx1 = time_idx2 = time_idx
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Get class name
        class_names = ['Motorcycles', 'Cars', 'Trucks', 'Buses']
        class_name = class_names[class_idx] if class_idx < len(class_names) else f'Class {class_idx}'
        
        # Plot density profiles
        t1 = results1['grid_t'][time_idx1]
        t2 = results2['grid_t'][time_idx2]
        ax.plot(results1['grid_x'], results1['class_densities'][class_idx, time_idx1], 
                label=f"{results1.get('name', 'Scenario 1')} (t={t1:.2f}h)", 
                color='blue', linewidth=2)
        ax.plot(results2['grid_x'], results2['class_densities'][class_idx, time_idx2], 
                label=f"{results2.get('name', 'Scenario 2')} (t={t2:.2f}h)", 
                color='red', linewidth=2)
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel(f'Densité de {class_name} (véh/km)')
        ax.set_title(title)
        ax.grid(True)
        ax.legend()
        
        if save:
            filename = title.replace(" ", "_").lower() if title else "multiclass_comparison"
            plt.savefig(f'{self.output_dir}/{filename}.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
