"""
Multiclass Visualization for Traffic Models

This module provides specialized visualization tools for multiclass traffic models,
showing the relationships between different vehicle classes.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
    
    def plot_spacetime_class_comparison(self, results, show=False, save=True):
        """
        Create a space-time diagram showing class proportions.
        
        Args:
            results: Dictionary containing simulation results
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure
        """
        class_densities = results['class_densities']
        n_classes = results['n_classes']
        grid_x = results['grid_x']
        grid_t = results['grid_t']
        
        # Convert to class proportions
        class_proportions = np.zeros_like(class_densities)
        total_density = np.sum(class_densities, axis=0)
        
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            for i in range(n_classes):
                class_proportions[i] = class_densities[i] / np.maximum(total_density, 1e-10)
                class_proportions[i] = np.nan_to_num(class_proportions[i])
        
        # Create space-time RGB image based on class proportions
        nt, nx = total_density.shape
        rgb_image = np.zeros((nt, nx, 3))
        
        # Map each class to a color (using first 3 classes if more than 3)
        color_maps = [
            [1, 0, 0],  # Red for motorcycles
            [0, 1, 0],  # Green for cars
            [0, 0, 1],  # Blue for trucks/buses
        ]
        
        # Fill in RGB image based on class proportions
        for i in range(min(n_classes, 3)):
            for c in range(3):
                rgb_image[:, :, c] += class_proportions[i] * color_maps[i][c]
        
        # Normalize and clip RGB values
        rgb_image = np.clip(rgb_image, 0, 1)
        
        # Create figure and plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot RGB image as pcolormesh
        X, T = np.meshgrid(grid_x, grid_t)
        ax.pcolormesh(X, T, total_density, cmap='gray', alpha=0.3)
        ax.imshow(rgb_image, extent=[grid_x[0], grid_x[-1], grid_t[-1], grid_t[0]], 
                  aspect='auto', alpha=0.7)
        
        # Create custom legend
        legend_elements = []
        for i in range(min(n_classes, 3)):
            class_name = self.class_names[i] if i < len(self.class_names) else f'Class {i}'
            color = color_maps[i]
            legend_elements.append(plt.Line2D([0], [0], marker='s', color='w', 
                                             markerfacecolor=color, markersize=15, 
                                             label=class_name))
        
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Temps (h)')
        ax.set_title('Space-Time Class Distribution')
        ax.legend(handles=legend_elements, loc='upper right')
        
        if save:
            plt.savefig(f'{self.output_dir}/spacetime_class_comparison.png', 
                       bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_class_proportions_evolution(self, results, x_position=None, show=False, save=True):
        """
        Plot evolution of class proportions at a specific location.
        
        Args:
            results: Dictionary containing simulation results
            x_position: Position to plot proportions (if None, domain midpoint is used)
            show: Whether to display the plot
            save: Whether to save the plot to file
            
        Returns:
            Matplotlib figure
        """
        class_densities = results['class_densities']
        n_classes = results['n_classes']
        grid_x = results['grid_x']
        grid_t = results['grid_t']
        
        # If no position specified, use midpoint of domain
        if x_position is None:
            midpoint_idx = len(grid_x) // 2
            x_position = grid_x[midpoint_idx]
        else:
            # Find closest grid point to requested position
            midpoint_idx = np.argmin(np.abs(grid_x - x_position))
            x_position = grid_x[midpoint_idx]
        
        # Extract densities at selected position
        densities_at_position = class_densities[:, :, midpoint_idx]
        
        # Calculate proportions
        total_density = np.sum(densities_at_position, axis=0)
        proportions = np.zeros_like(densities_at_position)
        
        with np.errstate(divide='ignore', invalid='ignore'):
            for i in range(n_classes):
                proportions[i] = densities_at_position[i] / np.maximum(total_density, 1e-10)
                proportions[i] = np.nan_to_num(proportions[i])
        
        # Create stacked area plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.stackplot(grid_t, *[proportions[i] for i in range(n_classes)],
                     labels=[self.class_names[i] if i < len(self.class_names) else f'Class {i}'
                            for i in range(n_classes)],
                     colors=[self.class_colors[i % len(self.class_colors)] for i in range(n_classes)])
        
        ax.set_xlabel('Temps (h)')
        ax.set_ylabel('Proportion')
        ax.set_title(f'Class Proportions Evolution at x = {x_position:.2f} km')
        ax.set_xlim(grid_t[0], grid_t[-1])
        ax.set_ylim(0, 1)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Add total density as a line on twin axis
        ax2 = ax.twinx()
        ax2.plot(grid_t, total_density, 'k--', alpha=0.7, label='Total Density')
        ax2.set_ylabel('Densité totale (véh/km)')
        ax2.set_ylim(0, np.max(total_density) * 1.2)
        
        if save:
            plt.savefig(f'{self.output_dir}/class_proportions_x{x_position:.1f}.png', 
                       bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def create_dashboard(self, results, time_idx=None, show=False, save=True):
        """
        Create a comprehensive dashboard visualization of multiclass simulation results.
        
        Args:
            results: Dictionary containing simulation results
            time_idx: Time index to use for spatial profiles (if None, uses middle of simulation)
            show: Whether to display the dashboard
            save: Whether to save the dashboard to file
            
        Returns:
            Matplotlib figure
        """
        if time_idx is None:
            time_idx = len(results['grid_t']) // 2
            
        # Create large figure for dashboard
        fig = plt.figure(figsize=(20, 16))
        grid = plt.GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Density evolution (time-space diagram)
        ax1 = fig.add_subplot(grid[0, 0])
        X, T = np.meshgrid(results['grid_x'], results['grid_t'])
        im1 = ax1.pcolormesh(X, T, results['density'], cmap='viridis', shading='auto')
        ax1.set_title('Total Density Evolution')
        ax1.set_xlabel('Position (km)')
        ax1.set_ylabel('Temps (h)')
        plt.colorbar(im1, ax=ax1, label='Densité (véh/km)')
        
        # 2. Class density profiles at selected time
        ax2 = fig.add_subplot(grid[0, 1])
        for i in range(results['n_classes']):
            class_name = self.class_names[i] if i < len(self.class_names) else f'Class {i}'
            color = self.class_colors[i % len(self.class_colors)]
            ax2.plot(results['grid_x'], results['class_densities'][i, time_idx], 
                     label=class_name, color=color)
        ax2.set_title(f'Class Density Profiles at t = {results["grid_t"][time_idx]:.2f}h')
        ax2.set_xlabel('Position (km)')
        ax2.set_ylabel('Densité (véh/km)')
        ax2.grid(True)
        ax2.legend()
        
        # 3. Flow-density relationships
        ax3 = fig.add_subplot(grid[1, 0])
        for i in range(results['n_classes']):
            class_name = self.class_names[i] if i < len(self.class_names) else f'Class {i}'
            color = self.class_colors[i % len(self.class_colors)]
            densities_flat = results['class_densities'][i].flatten()
            flows_flat = results['class_flows'][i].flatten()
            ax3.scatter(densities_flat, flows_flat, s=2, color=color, alpha=0.3, label=class_name)
        ax3.set_title('Flow-Density Relationships by Class')
        ax3.set_xlabel('Densité (véh/km)')
        ax3.set_ylabel('Flux (véh/h)')
        ax3.grid(True)
        ax3.legend()
        
        # 4. Class proportions evolution at middle point
        midpoint_idx = len(results['grid_x']) // 2
        densities_at_position = [results['class_densities'][i, :, midpoint_idx] 
                                for i in range(results['n_classes'])]
        total_density = np.sum(results['class_densities'][:, :, midpoint_idx], axis=0)
        proportions = [np.divide(densities_at_position[i], np.maximum(total_density, 1e-10)) 
                      for i in range(results['n_classes'])]
        
        ax4 = fig.add_subplot(grid[1, 1])
        ax4.stackplot(results['grid_t'], *proportions,
                     labels=[self.class_names[i] if i < len(self.class_names) else f'Class {i}'
                            for i in range(results['n_classes'])],
                     colors=[self.class_colors[i % len(self.class_colors)] 
                            for i in range(results['n_classes'])])
        ax4.set_title(f'Class Proportions at x = {results["grid_x"][midpoint_idx]:.2f}km')
        ax4.set_xlabel('Temps (h)')
        ax4.set_ylabel('Proportion')
        ax4.grid(True)
        ax4.legend()
        
        # 5. Space-time class distribution
        ax5 = fig.add_subplot(grid[2, :])
        
        # Calculate class proportions
        class_proportions = np.zeros_like(results['class_densities'])
        total_density = np.sum(results['class_densities'], axis=0)
        with np.errstate(divide='ignore', invalid='ignore'):
            for i in range(results['n_classes']):
                class_proportions[i] = results['class_densities'][i] / np.maximum(total_density, 1e-10)
                class_proportions[i] = np.nan_to_num(class_proportions[i])
        
        # Create RGB image (first 3 classes only)
        nt, nx = total_density.shape
        rgb_image = np.zeros((nt, nx, 3))
        color_maps = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # Red, Green, Blue
        
        for i in range(min(results['n_classes'], 3)):
            for c in range(3):
                rgb_image[:, :, c] += class_proportions[i] * color_maps[i][c]
        
        # Normalize and clip RGB values
        rgb_image = np.clip(rgb_image, 0, 1)
        
        ax5.imshow(rgb_image, extent=[results['grid_x'][0], results['grid_x'][-1],
                                    results['grid_t'][-1], results['grid_t'][0]], 
                  aspect='auto')
        
        # Create custom legend for the RGB plot
        legend_elements = []
        for i in range(min(results['n_classes'], 3)):
            class_name = self.class_names[i] if i < len(self.class_names) else f'Class {i}'
            color = color_maps[i]
            legend_elements.append(plt.Line2D([0], [0], marker='s', color='w', 
                                             markerfacecolor=color, markersize=15, 
                                             label=class_name))
        
        ax5.set_title('Space-Time Class Distribution')
        ax5.set_xlabel('Position (km)')
        ax5.set_ylabel('Temps (h)')
        ax5.legend(handles=legend_elements)
        
        plt.suptitle(f"Multiclass Traffic Simulation: {results['name']}", fontsize=16)
        
        if save:
            plt.savefig(f'{self.output_dir}/multiclass_dashboard.png', 
                       bbox_inches='tight', dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
