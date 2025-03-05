"""
Simulation Plotter for Traffic Models

This module provides visualization tools for plotting simulation results
from traffic models, showing the evolution of traffic variables over time and space.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import os


class SimulationPlotter:
    """Class for creating and saving visualizations of simulation results."""
    
    def __init__(self, model_name="LWR", output_dir="simulations"):
        """
        Initialize the plotter with model name and output directory.
        
        Args:
            model_name: Name of the model (e.g., 'LWR', 'MulticlassLWR')
            output_dir: Directory for saving plots
        """
        self.model_name = model_name
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_density_evolution(self, density, grid_x, grid_t, title=None, show=False, save=True):
        """
        Generate a space-time plot of traffic density evolution.
        
        Args:
            density: 2D array of density values [time, space]
            grid_x: Spatial grid points
            grid_t: Time grid points
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Convert grids to meshgrid for pcolormesh
        X, T = np.meshgrid(grid_x, grid_t)
        
        # Create a colormap
        im = ax.pcolormesh(X, T, density, cmap='viridis', shading='auto')
        
        # Add colorbar and labels
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Densité (véh/km)')
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Temps (h)')
        
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f"{self.model_name} - Évolution de la densité")
        
        if save:
            filename = title.replace(" ", "_").lower() if title else "density_evolution"
            plt.savefig(f'{self.output_dir}/{filename}.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_velocity_evolution(self, velocity, grid_x, grid_t, title=None, show=False, save=True):
        """
        Generate a space-time plot of traffic velocity evolution.
        
        Args:
            velocity: 2D array of velocity values [time, space]
            grid_x: Spatial grid points
            grid_t: Time grid points
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Convert grids to meshgrid for pcolormesh
        X, T = np.meshgrid(grid_x, grid_t)
        
        # Create a colormap
        im = ax.pcolormesh(X, T, velocity, cmap='coolwarm', shading='auto')
        
        # Add colorbar and labels
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Vitesse (km/h)')
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Temps (h)')
        
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f"{self.model_name} - Évolution de la vitesse")
        
        if save:
            filename = title.replace(" ", "_").lower() if title else "velocity_evolution"
            plt.savefig(f'{self.output_dir}/{filename}.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_flow_evolution(self, flow, grid_x, grid_t, title=None, show=False, save=True):
        """
        Generate a space-time plot of traffic flow evolution.
        
        Args:
            flow: 2D array of flow values [time, space]
            grid_x: Spatial grid points
            grid_t: Time grid points
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Convert grids to meshgrid for pcolormesh
        X, T = np.meshgrid(grid_x, grid_t)
        
        # Create a colormap
        im = ax.pcolormesh(X, T, flow, cmap='plasma', shading='auto')
        
        # Add colorbar and labels
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Flux (véh/h)')
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Temps (h)')
        
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f"{self.model_name} - Évolution du flux")
        
        if save:
            filename = title.replace(" ", "_").lower() if title else "flow_evolution"
            plt.savefig(f'{self.output_dir}/{filename}.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_space_profiles(self, density, velocity, flow, grid_x, times, time_indices=None, show=False, save=True):
        """
        Plot spatial profiles of density, velocity, and flow at selected times.
        
        Args:
            density: 2D array of density values [time, space]
            velocity: 2D array of velocity values [time, space]
            flow: 2D array of flow values [time, space]
            grid_x: Spatial grid points
            times: Time values corresponding to rows in arrays
            time_indices: Optional list of time indices to plot, if None selected automatically
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        if time_indices is None:
            # Select 5 evenly spaced times
            n_times = len(times)
            time_indices = [0, n_times//4, n_times//2, 3*n_times//4, n_times-1]
        
        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
        
        for idx in time_indices:
            t = times[idx]
            axs[0].plot(grid_x, density[idx], label=f't = {t:.2f}h')
            axs[1].plot(grid_x, velocity[idx], label=f't = {t:.2f}h')
            axs[2].plot(grid_x, flow[idx], label=f't = {t:.2f}h')
        
        axs[0].set_ylabel('Densité (véh/km)')
        axs[0].set_title('Profils de Densité')
        axs[0].grid(True)
        axs[0].legend()
        
        axs[1].set_ylabel('Vitesse (km/h)')
        axs[1].set_title('Profils de Vitesse')
        axs[1].grid(True)
        
        axs[2].set_ylabel('Flux (véh/h)')
        axs[2].set_xlabel('Position (km)')
        axs[2].set_title('Profils de Flux')
        axs[2].grid(True)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/space_profiles.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def create_interactive_visualization(self, results):
        """
        Create an interactive visualization of simulation results with time slider.
        
        Args:
            results: Dictionary containing simulation results
            
        Returns:
            Matplotlib figure and animation objects
        """
        density = results['density']
        velocity = results['velocity']
        flow = results['flow']
        grid_x = results['grid_x']
        grid_t = results['grid_t']
        
        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
        
        # Initial plots
        den_line, = axs[0].plot(grid_x, density[0], 'b-', lw=2)
        axs[0].set_ylabel('Densité (véh/km)')
        axs[0].set_title('Profil de Densité')
        axs[0].grid(True)
        
        vel_line, = axs[1].plot(grid_x, velocity[0], 'r-', lw=2)
        axs[1].set_ylabel('Vitesse (km/h)')
        axs[1].set_title('Profil de Vitesse')
        axs[1].grid(True)
        
        flow_line, = axs[2].plot(grid_x, flow[0], 'g-', lw=2)
        axs[2].set_ylabel('Flux (véh/h)')
        axs[2].set_xlabel('Position (km)')
        axs[2].set_title('Profil de Flux')
        axs[2].grid(True)
        
        # Set y-axis limits
        axs[0].set_ylim(0, np.max(density) * 1.1)
        axs[1].set_ylim(0, np.max(velocity) * 1.1)
        axs[2].set_ylim(0, np.max(flow) * 1.1)
        
        # Add time annotation
        time_text = axs[0].text(0.02, 0.95, 't = 0.00h', transform=axs[0].transAxes)
        
        def update(frame):
            den_line.set_ydata(density[frame])
            vel_line.set_ydata(velocity[frame])
            flow_line.set_ydata(flow[frame])
            time_text.set_text(f't = {grid_t[frame]:.2f}h')
            return den_line, vel_line, flow_line, time_text
        
        ani = FuncAnimation(
            fig, update, frames=len(grid_t), 
            interval=100, blit=True
        )
        
        plt.tight_layout()
        return fig, ani
    
    def plot_multiclass_comparison(self, class_densities, class_names, grid_x, time_idx, title=None, show=False, save=True):
        """
        Plot density profiles for multiple vehicle classes at a specific time.
        
        Args:
            class_densities: List of 2D arrays containing density values for each class
            class_names: List of names for each class
            grid_x: Spatial grid points
            time_idx: Time index to plot
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i, (density, name) in enumerate(zip(class_densities, class_names)):
            ax.plot(grid_x, density[time_idx], label=name, linewidth=2)
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Densité (véh/km)')
        
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f"{self.model_name} - Comparaison des Classes de Véhicules")
        
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

    def plot_combined_evolution(self, density, velocity, flow, grid_x, grid_t, title=None, show=False, save=True):
        """
        Generate a combined space-time plot with density, velocity, and flow evolution.
        
        Args:
            density: 2D array of density values [time, space]
            velocity: 2D array of velocity values [time, space]
            flow: 2D array of flow values [time, space]
            grid_x: Spatial grid points
            grid_t: Time grid points
            title: Base title for the plot
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure object
        """
        # Create figure with 3 subplots arranged vertically
        fig, axes = plt.subplots(3, 1, figsize=(12, 15))
        
        # Convert grids to meshgrid for pcolormesh
        X, T = np.meshgrid(grid_x, grid_t)
        
        # Plot density evolution
        im1 = axes[0].pcolormesh(X, T, density, cmap='viridis', shading='auto')
        cbar1 = fig.colorbar(im1, ax=axes[0])
        cbar1.set_label('Densité (véh/km)')
        axes[0].set_xlabel('Position (km)')
        axes[0].set_ylabel('Temps (h)')
        if title:
            axes[0].set_title(f"(a) {title} - Évolution de la densité")
        else:
            axes[0].set_title(f"(a) {self.model_name} - Évolution de la densité")
        
        # Plot velocity evolution
        im2 = axes[1].pcolormesh(X, T, velocity, cmap='coolwarm', shading='auto')
        cbar2 = fig.colorbar(im2, ax=axes[1])
        cbar2.set_label('Vitesse (km/h)')
        axes[1].set_xlabel('Position (km)')
        axes[1].set_ylabel('Temps (h)')
        if title:
            axes[1].set_title(f"(b) {title} - Évolution de la vitesse")
        else:
            axes[1].set_title(f"(b) {self.model_name} - Évolution de la vitesse")
        
        # Plot flow evolution
        im3 = axes[2].pcolormesh(X, T, flow, cmap='plasma', shading='auto')
        cbar3 = fig.colorbar(im3, ax=axes[2])
        cbar3.set_label('Flux (véh/h)')
        axes[2].set_xlabel('Position (km)')
        axes[2].set_ylabel('Temps (h)')
        if title:
            axes[2].set_title(f"(c) {title} - Évolution du flux")
        else:
            axes[2].set_title(f"(c) {self.model_name} - Évolution du flux")
        
        plt.tight_layout()
        
        # Save figure if requested
        if save:
            filename = title.replace(" ", "_").lower() if title else "combined_evolution"
            plt.savefig(f'{self.output_dir}/{filename}_combined.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
