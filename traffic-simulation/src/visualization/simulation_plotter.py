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
            filepath = f'{self.output_dir}/{filename}.png'
            plt.savefig(filepath, bbox_inches='tight', dpi=300)
            print(f"Figure saved as {os.path.abspath(filepath)}")
        
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
            filepath = f'{self.output_dir}/{filename}.png'
            plt.savefig(filepath, bbox_inches='tight', dpi=300)
            print(f"Figure saved as {os.path.abspath(filepath)}")
        
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
            filepath = f'{self.output_dir}/{filename}.png'
            plt.savefig(filepath, bbox_inches='tight', dpi=300)
            print(f"Figure saved as {os.path.abspath(filepath)}")
        
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
            filepath = f'{self.output_dir}/{filename}.png'
            plt.savefig(filepath, bbox_inches='tight', dpi=300)
            print(f"Figure saved as {os.path.abspath(filepath)}")
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig

    def plot_combined_evolution(self, density, velocity, flow, x_grid, t_grid, title=None, show=True, save=True):
        """
        Creates a combined visualization showing density, velocity, and flow evolution in a single figure.
        
        Parameters:
        -----------
        density : numpy.ndarray
            2D array of traffic density values (shape: time x space)
        velocity : numpy.ndarray
            2D array of traffic velocity values (shape: time x space)
        flow : numpy.ndarray
            2D array of traffic flow values (shape: time x space)
        x_grid : numpy.ndarray
            1D array of spatial grid points [km]
        t_grid : numpy.ndarray
            1D array of time grid points [h]
        title : str, optional
            Title for the plot. If None, a default title will be used.
        show : bool, optional
            If True, the plot will be displayed
        save : bool, optional
            If True, the plot will be saved to a file
        
        Returns:
        --------
        fig : matplotlib.figure.Figure
            The generated figure
        """
        # Input validation
        if not all(isinstance(arr, np.ndarray) for arr in [density, velocity, flow, x_grid, t_grid]):
            raise TypeError("Density, velocity, flow, x_grid, and t_grid must be numpy arrays")
        
        if not (density.shape == velocity.shape == flow.shape):
            raise ValueError("Density, velocity, and flow arrays must have the same shape")
        
        # Create a figure with 3 subplots (vertically stacked)
        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
        
        # Create 2D meshgrid for pcolormesh
        X, T = np.meshgrid(x_grid, t_grid)
        
        # Plot density evolution
        im1 = axs[0].pcolormesh(X, T, density, cmap='viridis', shading='auto')
        axs[0].set_title('Density Evolution')
        axs[0].set_ylabel('Time (h)')
        fig.colorbar(im1, ax=axs[0], label='Density (veh/km)')
        
        # Plot velocity evolution
        im2 = axs[1].pcolormesh(X, T, velocity, cmap='coolwarm', shading='auto')
        axs[1].set_title('Velocity Evolution')
        axs[1].set_ylabel('Time (h)')
        fig.colorbar(im2, ax=axs[1], label='Velocity (km/h)')
        
        # Plot flow evolution
        im3 = axs[2].pcolormesh(X, T, flow, cmap='plasma', shading='auto')
        axs[2].set_title('Flow Evolution')
        axs[2].set_xlabel('Position (km)')
        axs[2].set_ylabel('Time (h)')
        fig.colorbar(im3, ax=axs[2], label='Flow (veh/h)')
        
        # Set the main title if provided
        if title:
            fig.suptitle(title, fontsize=16)
        else:
            fig.suptitle(f'{self.model_name}: Combined Traffic Evolution', fontsize=16)
        
        plt.tight_layout()
        
        # Save figure if requested
        if save:
            save_title = title if title else f'{self.model_name}_combined_evolution'
            filepath = f"{self.output_dir}/{save_title.replace(' ', '_').lower()}.png"
            try:
                plt.savefig(filepath)
                print(f"Figure saved as {os.path.abspath(filepath)}")
            except Exception as e:
                print(f"Error saving figure: {e}")
        
        # Show figure if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
