"""
Multiclass Visualization for Traffic Models

This module provides specialized visualization tools for multiclass traffic models,
showing the relationships between different vehicle classes.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
from matplotlib import cm
import os

from .simulation_plotter import SimulationPlotter


class MulticlassPlotter(SimulationPlotter):
    """Class for creating visualizations of multiclass simulation results."""
    
    def __init__(self, model_name="MulticlassLWR", output_dir="simulations"):
        """
        Initialize the multiclass plotter.
        
        Args:
            model_name: Name of the model
            output_dir: Directory for saving plots
        """
        super().__init__(model_name, output_dir)
        self.class_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        self.class_names = ['Motorcycles', 'Cars', 'Trucks', 'Buses', 'Other']
    
    def plot_all(self, results, save=True, show=False):
        """
        Generate a complete set of visualizations for multiclass results.
        
        Args:
            results: Dictionary containing simulation results
            save: Whether to save the plots to files
            show: Whether to display the plots
            
        Returns:
            List of generated figures
        """
        figures = []
        
        # Standard plots (density, velocity, flow)
        figures.append(self.plot_density_evolution(
            results['density'], results['grid_x'], results['grid_t'], 
            title=f"{results['name']} - Total Density",
            show=show, save=save
        ))
        
        figures.append(self.plot_velocity_evolution(
            results['velocity'], results['grid_x'], results['grid_t'], 
            title=f"{results['name']} - Average Velocity",
            show=show, save=save
        ))
        
        figures.append(self.plot_flow_evolution(
            results['flow'], results['grid_x'], results['grid_t'], 
            title=f"{results['name']} - Total Flow",
            show=show, save=save
        ))
        
        # Class-specific plots
        n_classes = results['n_classes']
        class_densities = results['class_densities']
        class_velocities = results['class_velocities']
        class_flows = results['class_flows']
        
        # Make sure we have proper class names
        if len(self.class_names) < n_classes:
            self.class_names = [f'Class {i}' for i in range(n_classes)]
        else:
            self.class_names = self.class_names[:n_classes]
        
        # Plot individual class densities
        for i in range(n_classes):
            figures.append(self.plot_density_evolution(
                class_densities[i], results['grid_x'], results['grid_t'],
                title=f"{results['name']} - {self.class_names[i]} Density",
                show=show, save=save
            ))
        
        # Plot class comparison at selected times
        n_times = len(results['grid_t'])
        time_indices = [0, n_times//4, n_times//2, 3*n_times//4, n_times-1]
        
        for idx in time_indices:
            t = results['grid_t'][idx]
            figures.append(self.plot_class_comparison(
                results, idx, 
                title=f"Vehicle Class Comparison at t = {t:.2f}h",
                show=show, save=save
            ))
        
        # Plot flow-density relationships
        figures.append(self.plot_flow_density_relationship(
            results, show=show, save=save
        ))
        
        return figures
    
    def plot_class_comparison(self, results, time_idx, title=None, show=False, save=True):
        """
        Compare densities of different vehicle classes at a specific time.
        
        Args:
            results: Dictionary containing simulation results
            time_idx: Index of the time to plot
            title: Plot title
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure
        """
        class_densities = results['class_densities']
        n_classes = results['n_classes']
        grid_x = results['grid_x']
        grid_t = results['grid_t']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i in range(n_classes):
            class_name = self.class_names[i] if i < len(self.class_names) else f'Class {i}'
            color = self.class_colors[i % len(self.class_colors)]
            ax.plot(grid_x, class_densities[i, time_idx], label=class_name, color=color, linewidth=2)
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Densité (véh/km)')
        
        if title:
            ax.set_title(title)
        else:
            t = grid_t[time_idx]
            ax.set_title(f"Vehicle Class Comparison at t = {t:.2f}h")
        
        ax.grid(True)
        ax.legend()
        
        if save:
            filename = f"class_comparison_t{time_idx:03d}"
            if title:
                filename = title.replace(" ", "_").lower()
            plt.savefig(f'{self.output_dir}/{filename}.png', bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_flow_density_relationship(self, results, show=False, save=True):
        """
        Plot flow vs density for different vehicle classes.
        
        Args:
            results: Dictionary containing simulation results
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure
        """
        class_densities = results['class_densities']
        class_flows = results['class_flows']
        n_classes = results['n_classes']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for i in range(n_classes):
            class_name = self.class_names[i] if i < len(self.class_names) else f'Class {i}'
            color = self.class_colors[i % len(self.class_colors)]
            
            # Flatten arrays for scatter plot
            densities_flat = class_densities[i].flatten()
            flows_flat = class_flows[i].flatten()
            
            # Plot points with slight transparency
            ax.scatter(densities_flat, flows_flat, label=class_name, color=color, 
                       alpha=0.3, s=5)
        
        # Also plot total flow vs density
        ax.scatter(results['density'].flatten(), results['flow'].flatten(), 
                  label='Total', color='black', alpha=0.3, s=5)
        
        ax.set_xlabel('Densité (véh/km)')
        ax.set_ylabel('Flux (véh/h)')
        ax.set_title('Relation Flux-Densité par Classe de Véhicule')
        ax.grid(True)
        ax.legend()
        
        if save:
            plt.savefig(f'{self.output_dir}/flow_density_relationship.png', 
                       bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def create_multiclass_animation(self, results):
        """
        Create an animated visualization of multiclass results.
        
        Args:
            results: Dictionary containing simulation results
            
        Returns:
            Matplotlib figure and animation
        """
        from matplotlib.animation import FuncAnimation
        
        class_densities = results['class_densities']
        n_classes = results['n_classes']
        grid_x = results['grid_x']
        grid_t = results['grid_t']
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        lines = []
        for i in range(n_classes):
            class_name = self.class_names[i] if i < len(self.class_names) else f'Class {i}'
            color = self.class_colors[i % len(self.class_colors)]
            line, = ax.plot([], [], label=class_name, color=color, linewidth=2)
            lines.append(line)
        
        # Also add total density line
        total_line, = ax.plot([], [], label='Total', color='black', linewidth=2, linestyle='--')
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Densité (véh/km)')
        ax.set_title('Vehicle Class Densities')
        ax.set_xlim(grid_x[0], grid_x[-1])
        ax.set_ylim(0, 1.1 * np.max(results['density']))
        ax.grid(True)
        ax.legend()
        
        # Time annotation
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
        
        def init():
            for line in lines:
                line.set_data([], [])
            total_line.set_data([], [])
            time_text.set_text('')
            return lines + [total_line, time_text]
        
        def update(frame):
            for i, line in enumerate(lines):
                line.set_data(grid_x, class_densities[i, frame])
            total_line.set_data(grid_x, results['density'][frame])
            time_text.set_text(f't = {grid_t[frame]:.2f}h')
            return lines + [total_line, time_text]
        
        ani = FuncAnimation(
            fig, update, frames=len(grid_t), 
            init_func=init, blit=True, interval=100
        )
        
        plt.tight_layout()
        return fig, ani
    
    def plot_spacetime_class_comparison(self, densities, x_grid, t_grid, time_indices=None, title=None, show=True, save=True):
        """
        Creates a visualization comparing the proportion of different vehicle classes across space and time.
        
        Parameters:
        -----------
        densities : dict
            Dictionary with class names as keys and 2D density arrays as values
        x_grid : numpy.ndarray
            1D array of spatial grid points [km]
        t_grid : numpy.ndarray
            1D array of time grid points [h]
        time_indices : list or numpy.ndarray, optional
            Indices of time steps to plot. If None, equally spaced times will be chosen
        title : str, optional
            Title for the plot
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
        if not isinstance(densities, dict):
            raise TypeError("Densities must be provided as a dictionary")
        
        # Choose time indices if not provided
        if time_indices is None:
            num_times = 5  # Default number of time snapshots
            time_indices = np.linspace(0, len(t_grid) - 1, num_times, dtype=int)
        
        # Create a figure
        fig, axs = plt.subplots(len(time_indices), 1, figsize=(10, 3*len(time_indices)))
        
        # Handle case with only one time index
        if len(time_indices) == 1:
            axs = [axs]
        
        # For each time index, calculate class proportions and plot
        for i, t_idx in enumerate(time_indices):
            # Calculate total density at each point in space
            total_density = np.zeros_like(x_grid)
            for class_name, density_array in densities.items():
                if t_idx < density_array.shape[0]:
                    total_density += density_array[t_idx]
                else:
                    raise IndexError(f"Time index {t_idx} out of bounds for class {class_name}")
            
            # Calculate proportions for each class
            class_proportions = {}
            for class_name, density_array in densities.items():
                class_proportions[class_name] = np.divide(
                    density_array[t_idx], 
                    total_density, 
                    out=np.zeros_like(density_array[t_idx]), 
                    where=(total_density > 0)
                )
            
            # Create stacked area plot
            bottom = np.zeros_like(x_grid)
            for class_name, proportion in class_proportions.items():
                axs[i].fill_between(
                    x_grid, 
                    bottom, 
                    bottom + proportion, 
                    label=class_name if i == 0 else None,  # Only add label in first subplot
                    color=self.class_colors.get(class_name, 'gray')
                )
                bottom += proportion
            
            axs[i].set_ylabel('Proportion')
            axs[i].set_title(f'Time = {t_grid[t_idx]:.2f} h')
            axs[i].set_ylim(0, 1)
        
        # Set x-label only for the last subplot
        axs[-1].set_xlabel('Position (km)')
        
        # Add legend to the figure
        fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05), ncol=len(densities))
        
        # Set the main title if provided
        if title:
            fig.suptitle(title, fontsize=16)
        else:
            fig.suptitle(f'{self.model_name}: Spatial Class Proportion Comparison', fontsize=16)
        
        plt.tight_layout()
        
        # Save figure if requested
        if save:
            save_title = title if title else f'{self.model_name}_spacetime_class_comparison'
            filename = f"{self.output_dir}/{save_title.replace(' ', '_').lower()}.png"
            try:
                plt.savefig(filename)
                print(f"Figure saved as {filename}")
            except Exception as e:
                print(f"Error saving figure: {e}")
        
        # Show figure if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig

    def create_dashboard(self, results, x_grid, t_grid, title=None, show=True, save=True):
        """
        Creates a comprehensive dashboard combining multiple visualizations for multiclass traffic analysis.
        
        Parameters:
        -----------
        results : dict
            Dictionary containing simulation results with keys:
            - 'densities': Dict of class densities
            - 'velocities': Dict of class velocities
            - 'flows': Dict of class flows
            - 'total_density', 'mean_velocity', 'total_flow': Total/mean traffic variables
        x_grid : numpy.ndarray
            1D array of spatial grid points [km]
        t_grid : numpy.ndarray
            1D array of time grid points [h]
        title : str, optional
            Title for the dashboard
        show : bool, optional
            If True, the dashboard will be displayed
        save : bool, optional
            If True, the dashboard will be saved to a file
        
        Returns:
        --------
        fig : matplotlib.figure.Figure
            The generated figure
        """
        # Input validation
        required_keys = ['densities', 'velocities', 'flows', 'total_density', 'mean_velocity', 'total_flow']
        if not all(key in results for key in required_keys):
            missing = [key for key in required_keys if key not in results]
            raise KeyError(f"Missing required keys in results: {missing}")
        
        # Create a large figure with a grid layout
        fig = plt.figure(figsize=(20, 16))
        gs = gridspec.GridSpec(3, 3, figure=fig)
        
        # 1. Total traffic variables evolution (top row)
        # Total density evolution
        ax1 = fig.add_subplot(gs[0, 0])
        X, T = np.meshgrid(x_grid, t_grid)
        im1 = ax1.pcolormesh(X, T, results['total_density'], cmap='viridis', shading='auto')
        ax1.set_title('Total Density Evolution')
        ax1.set_ylabel('Time (h)')
        fig.colorbar(im1, ax=ax1, label='Density (veh/km)')
        
        # Mean velocity evolution
        ax2 = fig.add_subplot(gs[0, 1])
        im2 = ax2.pcolormesh(X, T, results['mean_velocity'], cmap='coolwarm', shading='auto')
        ax2.set_title('Mean Velocity Evolution')
        ax2.set_ylabel('Time (h)')
        fig.colorbar(im2, ax=ax2, label='Velocity (km/h)')
        
        # Total flow evolution
        ax3 = fig.add_subplot(gs[0, 2])
        im3 = ax3.pcolormesh(X, T, results['total_flow'], cmap='plasma', shading='auto')
        ax3.set_title('Total Flow Evolution')
        ax3.set_ylabel('Time (h)')
        fig.colorbar(im3, ax=ax3, label='Flow (veh/h)')
        
        # 2. Class comparison at specific times (middle row)
        # Select 3 representative time indices (start, middle, end)
        time_indices = [0, len(t_grid) // 2, -1]
        
        # Class density comparison
        ax4 = fig.add_subplot(gs[1, :])
        # Calculate class proportions at each position and time
        times = [t_grid[idx] for idx in time_indices]
        time_labels = [f"t={t:.2f}h" for t in times]
        
        bottom = np.zeros_like(x_grid)
        class_names = list(results['densities'].keys())
        for class_name in class_names:
            for i, t_idx in enumerate(time_indices):
                if i == 0:  # Only for the first time, to avoid duplicate labels
                    ax4.plot([], [], color=self.class_colors.get(class_name, 'gray'), 
                             label=class_name, linewidth=3)
        
        for i, t_idx in enumerate(time_indices):
            # Get total density at this time
            total_density = results['total_density'][t_idx]
            
            # Reset bottom for each time
            bottom = np.zeros_like(x_grid)
            
            # Offset for each time point
            offset = i * np.max(x_grid) * 1.1
            
            # Plot each class's contribution
            for class_name in class_names:
                density = results['densities'][class_name][t_idx]
                # Skip if all zero
                if np.all(density == 0):
                    continue
                    
                ax4.fill_between(
                    x_grid + offset,
                    bottom,
                    bottom + density,
                    color=self.class_colors.get(class_name, 'gray'),
                    alpha=0.7
                )
                bottom += density
            
            # Add time label
            ax4.text(offset + np.max(x_grid)/2, np.max(total_density)*1.1, 
                    time_labels[i], ha='center', fontsize=12)
                
        ax4.set_title('Class Composition at Different Times')
        ax4.set_xlabel('Position (km)')
        ax4.set_ylabel('Density (veh/km)')
        ax4.legend(loc='upper right')
        ax4.set_xticks([])
        
        # 3. Fundamental diagrams and gap-filling visualization (bottom row)
        # Flow-density relationship
        ax5 = fig.add_subplot(gs[2, 0])
        for class_name, density in results['densities'].items():
            # Flatten arrays for scatter plot
            flat_density = density.flatten()
            flat_flow = results['flows'][class_name].flatten()
            
            # Filter out zero density points for clarity
            mask = flat_density > 0
            ax5.scatter(flat_density[mask], flat_flow[mask], 
                       label=class_name, 
                       color=self.class_colors.get(class_name, 'gray'),
                       alpha=0.5, s=20)
        
        # Add total flow vs total density
        flat_total_density = results['total_density'].flatten()
        flat_total_flow = results['total_flow'].flatten()
        mask = flat_total_density > 0
        ax5.scatter(flat_total_density[mask], flat_total_flow[mask],
                   label='Total', color='black', alpha=0.7, s=25)
        
        ax5.set_title('Flow-Density Relationship')
        ax5.set_xlabel('Density (veh/km)')
        ax5.set_ylabel('Flow (veh/h)')
        ax5.legend()
        
        # Gap-filling effect visualization for motorcycles
        ax6 = fig.add_subplot(gs[2, 1:])
        
        # Attempt to extract motorcycle density and velocity
        moto_class = None
        for class_name in results['densities'].keys():
            if 'moto' in class_name.lower() or 'motorcycle' in class_name.lower():
                moto_class = class_name
                break
        
        if moto_class and 'cars' in results['densities']:
            # Calculate motorcycle proportion
            total_density_for_ratio = np.zeros_like(results['total_density'])
            for class_name, density in results['densities'].items():
                total_density_for_ratio += density
            
            moto_proportion = np.divide(
                results['densities'][moto_class],
                total_density_for_ratio,
                out=np.zeros_like(results['densities'][moto_class]),
                where=(total_density_for_ratio > 0)
            )
            
            # Create meshgrid for contour plot
            X, T = np.meshgrid(x_grid, t_grid)
            
            # Create contour plot of motorcycle proportion
            contour = ax6.contourf(X, T, moto_proportion, cmap='YlOrRd', levels=10)
            ax6.set_title('Motorcycle Proportion (Gap-Filling Effect)')
            ax6.set_xlabel('Position (km)')
            ax6.set_ylabel('Time (h)')
            fig.colorbar(contour, ax=ax6, label='Motorcycle Proportion')
            
            # Overlay velocity as contour lines
            CS = ax6.contour(X, T, results['mean_velocity'], colors='black', levels=5)
            ax6.clabel(CS, inline=True, fontsize=10, fmt='%.1f')
        else:
            ax6.text(0.5, 0.5, 'Motorcycle class data not available', 
                    ha='center', va='center', transform=ax6.transAxes)
            ax6.set_title('Gap-Filling Effect (Not Available)')
        
        # Add main title to the dashboard
        if title:
            fig.suptitle(title, fontsize=20)
        else:
            fig.suptitle(f'{self.model_name}: Traffic Analysis Dashboard', fontsize=20)
        
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        
        # Save figure if requested
        if save:
            save_title = title if title else f'{self.model_name}_traffic_dashboard'
            filename = f"{self.output_dir}/{save_title.replace(' ', '_').lower()}.png"
            try:
                plt.savefig(filename, dpi=150)
                print(f"Dashboard saved as {filename}")
            except Exception as e:
                print(f"Error saving dashboard: {e}")
        
        # Show figure if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
