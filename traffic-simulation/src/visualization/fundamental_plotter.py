"""
Fundamental Diagram Plotter

This module provides tools for plotting and analyzing fundamental diagrams of traffic flow,
showing relationships between density, flow, and velocity for different traffic models.
"""

import numpy as np
import matplotlib.pyplot as plt
import os


class FundamentalDiagramPlotter:
    """Class for creating and visualizing fundamental traffic diagrams."""
    
    def __init__(self, model_name="LWR", output_dir="fundamental_diagrams"):
        """
        Initialize the plotter.
        
        Args:
            model_name: Name of the traffic model
            output_dir: Directory for saving diagrams
        """
        self.model_name = model_name
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Color schemes
        self.color = 'tab:blue'
        self.critical_color = 'red'
        self.grid_alpha = 0.3
    
    def plot_fundamental_diagrams(self, model, density_range=None, n_points=100, 
                                 show=True, save=True, filename=None):
        """
        Plot the three fundamental diagrams (density-flow, density-velocity, flow-velocity).
        
        Args:
            model: Traffic model instance
            density_range: Range of densities to plot (min, max)
            n_points: Number of points to use for plotting
            show: Whether to display the plots
            save: Whether to save the plots to file
            filename: Filename for saved plot (without extension)
            
        Returns:
            Matplotlib figure
        """
        # Set density range
        if density_range is None:
            if hasattr(model, 'rho_max'):
                rho_max = model.rho_max
            elif hasattr(model, 'vehicle_classes'):
                # For multiclass model, use max density of any class
                rho_max = max(vc.rho_max for vc in model.vehicle_classes)
            else:
                rho_max = 180  # Default max density
            
            density_range = (0, rho_max)
        
        # Create density points
        densities = np.linspace(density_range[0], density_range[1], n_points)
        
        # Calculate flows and velocities
        # Adjust calculation based on model type
        if hasattr(model, 'get_velocity') and hasattr(model, 'get_flow'):
            # Standard LWR model
            velocities = np.array([model.get_velocity(rho) for rho in densities])
            flows = np.array([model.get_flow(rho) for rho in densities])
            
            # Calculate critical density
            try:
                critical_density = model.critical_density()
            except (AttributeError, TypeError):
                # If no method available, estimate critical density
                critical_idx = np.argmax(flows)
                critical_density = densities[critical_idx]
        else:
            # For other models, use a generic approach
            velocities = np.zeros_like(densities)
            flows = np.zeros_like(densities)
            
            for i, rho in enumerate(densities):
                # For multiclass, we'll just use a simple assumed distribution
                if hasattr(model, 'n_classes'):
                    # Assume 50% motorcycles and distribute rest evenly
                    rho_moto = rho * 0.5
                    rho_others = [(rho * 0.5) / (model.n_classes - 1)] * (model.n_classes - 1)
                    class_densities = [rho_moto] + rho_others
                    
                    total_flow = 0
                    for j in range(model.n_classes):
                        v_j = model.get_velocity(rho, j, rho_moto if j > 0 else None)
                        total_flow += class_densities[j] * v_j
                        
                    flows[i] = total_flow
                    if rho > 0:
                        velocities[i] = total_flow / rho
                    else:
                        velocities[i] = model.vehicle_classes[0].v_max
                else:
                    # Generic method using simulation with uniform density
                    result = model.simulate(
                        initial_density=rho, 
                        domain_length=1.0,
                        simulation_time=0.01,
                        dx=0.1,
                        cfl_factor=0.5
                    )
                    flows[i] = np.mean(result['flow'][0])
                    velocities[i] = np.mean(result['velocity'][0])
            
            # Estimate critical density
            critical_idx = np.argmax(flows)
            critical_density = densities[critical_idx]
        
        critical_velocity = model.get_velocity(critical_density) if hasattr(model, 'get_velocity') else flows[critical_idx] / critical_density
        critical_flow = model.get_flow(critical_density) if hasattr(model, 'get_flow') else flows[critical_idx]
        
        # Create figure with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # 1. Density-Flow diagram
        ax1.plot(densities, flows, '-', linewidth=2, color=self.color)
        ax1.plot(critical_density, critical_flow, 'o', markersize=8, color=self.critical_color)
        ax1.annotate(f'max={critical_flow:.0f}', 
                    xy=(critical_density, critical_flow),
                    xytext=(10, 10),
                    textcoords='offset points',
                    color=self.critical_color)
        
        ax1.set_xlabel('Densité (véh/km)')
        ax1.set_ylabel('Flux (véh/h)')
        ax1.set_title('Diagramme Flux-Densité')
        ax1.grid(alpha=self.grid_alpha)
        
        # 2. Density-Velocity diagram
        ax2.plot(densities, velocities, '-', linewidth=2, color=self.color)
        ax2.plot(critical_density, critical_velocity, 'o', markersize=8, color=self.critical_color)
        
        ax2.set_xlabel('Densité (véh/km)')
        ax2.set_ylabel('Vitesse (km/h)')
        ax2.set_title('Diagramme Vitesse-Densité')
        ax2.grid(alpha=self.grid_alpha)
        
        # 3. Velocity-Flow diagram (using parametric plot)
        ax3.plot(velocities, flows, '-', linewidth=2, color=self.color)
        ax3.plot(critical_velocity, critical_flow, 'o', markersize=8, color=self.critical_color)
        
        ax3.set_xlabel('Vitesse (km/h)')
        ax3.set_ylabel('Flux (véh/h)')
        ax3.set_title('Diagramme Flux-Vitesse')
        ax3.grid(alpha=self.grid_alpha)
        
        # Add overall title
        plt.suptitle(f'Diagrammes Fondamentaux - Modèle {self.model_name}', fontsize=16)
        
        plt.tight_layout()
        
        # Save if requested
        if save:
            if filename is None:
                filename = f"{self.model_name.lower()}_fundamental_diagrams"
            save_path = os.path.join(self.output_dir, f"{filename}.png")
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        # Show if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def compare_fundamental_diagrams(self, models_dict, density_range=None, n_points=100,
                                   show=True, save=True, filename=None):
        """
        Compare fundamental diagrams for multiple models.
        
        Args:
            models_dict: Dictionary of {name: model} to compare
            density_range: Range of densities to plot (min, max)
            n_points: Number of points to use for plotting
            show: Whether to display the plots
            save: Whether to save the plots to file
            filename: Filename for saved plot (without extension)
            
        Returns:
            Matplotlib figure
        """
        # Set density range
        if density_range is None:
            rho_maxes = []
            for model in models_dict.values():
                if hasattr(model, 'rho_max'):
                    rho_maxes.append(model.rho_max)
                elif hasattr(model, 'vehicle_classes'):
                    rho_maxes.append(max(vc.rho_max for vc in model.vehicle_classes))
                else:
                    rho_maxes.append(180)  # Default
            
            density_range = (0, max(rho_maxes))
        
        # Create density points
        densities = np.linspace(density_range[0], density_range[1], n_points)
        
        # Create figure with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        # Colors for different models
        colors = plt.cm.tab10(np.linspace(0, 1, len(models_dict)))
        
        # Plot for each model
        for i, (name, model) in enumerate(models_dict.items()):
            color = colors[i]
            
            # Calculate flows and velocities (similar to plot_fundamental_diagrams)
            if hasattr(model, 'get_velocity') and hasattr(model, 'get_flow'):
                velocities = np.array([model.get_velocity(rho) for rho in densities])
                flows = np.array([model.get_flow(rho) for rho in densities])
            else:
                # For complex models, use a simplified approach
                velocities = np.zeros_like(densities)
                flows = np.zeros_like(densities)
                
                for j, rho in enumerate(densities):
                    if hasattr(model, 'n_classes'):
                        rho_moto = rho * 0.5
                        rho_others = [(rho * 0.5) / (model.n_classes - 1)] * (model.n_classes - 1)
                        class_densities = [rho_moto] + rho_others
                        
                        total_flow = 0
                        for k in range(model.n_classes):
                            v_k = model.get_velocity(rho, k, rho_moto if k > 0 else None)
                            total_flow += class_densities[k] * v_k
                            
                        flows[j] = total_flow
                        if rho > 0:
                            velocities[j] = total_flow / rho
                        else:
                            velocities[j] = model.vehicle_classes[0].v_max
                    else:
                        # Generic approach
                        result = model.simulate(
                            initial_density=rho, 
                            domain_length=1.0,
                            simulation_time=0.01,
                            dx=0.1,
                            cfl_factor=0.5
                        )
                        flows[j] = np.mean(result['flow'][0])
                        velocities[j] = np.mean(result['velocity'][0])
            
            # Find critical point
            critical_idx = np.argmax(flows)
            critical_density = densities[critical_idx]
            critical_flow = flows[critical_idx]
            critical_velocity = velocities[critical_idx]
            
            # Plot on each subplot
            ax1.plot(densities, flows, '-', linewidth=2, color=color, label=name)
            ax1.plot(critical_density, critical_flow, 'o', color=color)
            
            ax2.plot(densities, velocities, '-', linewidth=2, color=color, label=name)
            ax2.plot(critical_density, critical_velocity, 'o', color=color)
            
            ax3.plot(velocities, flows, '-', linewidth=2, color=color, label=name)
            ax3.plot(critical_velocity, critical_flow, 'o', color=color)
        
        # Set labels and titles
        ax1.set_xlabel('Densité (véh/km)')
        ax1.set_ylabel('Flux (véh/h)')
        ax1.set_title('Diagramme Flux-Densité')
        ax1.grid(alpha=self.grid_alpha)
        ax1.legend()
        
        ax2.set_xlabel('Densité (véh/km)')
        ax2.set_ylabel('Vitesse (km/h)')
        ax2.set_title('Diagramme Vitesse-Densité')
        ax2.grid(alpha=self.grid_alpha)
        ax2.legend()
        
        ax3.set_xlabel('Vitesse (km/h)')
        ax3.set_ylabel('Flux (véh/h)')
        ax3.set_title('Diagramme Flux-Vitesse')
        ax3.grid(alpha=self.grid_alpha)
        ax3.legend()
        
        # Add overall title
        plt.suptitle('Comparaison des Diagrammes Fondamentaux', fontsize=16)
        
        plt.tight_layout()
        
        # Save if requested
        if save:
            if filename is None:
                filename = "comparison_fundamental_diagrams"
            save_path = os.path.join(self.output_dir, f"{filename}.png")
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        # Show if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def plot_multiclass_fundamental_diagrams(self, multiclass_model, moto_proportions=None, 
                                            density_range=None, n_points=100,
                                            show=True, save=True):
        """
        Plot fundamental diagrams for a multiclass model with different motorcycle proportions.
        
        Args:
            multiclass_model: MulticlassLWRModel instance
            moto_proportions: List of motorcycle proportions to plot
            density_range: Range of densities to plot (min, max)
            n_points: Number of points to use for plotting
            show: Whether to display the plots
            save: Whether to save the plots to file
            
        Returns:
            Matplotlib figure
        """
        # Default motorcycle proportions if not provided
        if moto_proportions is None:
            moto_proportions = [0.0, 0.25, 0.5, 0.75]
        
        # Set density range
        if density_range is None:
            max_density = max(vc.rho_max for vc in multiclass_model.vehicle_classes)
            density_range = (0, max_density)
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Colors for different proportions
        colors = plt.cm.viridis(np.linspace(0, 1, len(moto_proportions)))
        
        # Create density points
        densities = np.linspace(density_range[0], density_range[1], n_points)
        
        # For each proportion of motorcycles
        for i, prop in enumerate(moto_proportions):
            flows = []
            velocities = []
            
            # Calculate flow and velocity for each density
            for rho in densities:
                # Distribute total density according to proportion
                rho_moto = rho * prop
                rho_others = [(rho * (1 - prop)) / (multiclass_model.n_classes - 1)] * (multiclass_model.n_classes - 1)
                class_densities = [rho_moto] + rho_others
                
                # Calculate total flow
                total_flow = 0
                for j in range(multiclass_model.n_classes):
                    v_j = multiclass_model.get_velocity(rho, j, rho_moto if j > 0 else None)
                    total_flow += class_densities[j] * v_j
                
                flows.append(total_flow)
                
                # Calculate average velocity
                if rho > 0:
                    velocities.append(total_flow / rho)
                else:
                    velocities.append(multiclass_model.vehicle_classes[0].v_max)
            
            # Plot density-flow relationship
            ax1.plot(densities, flows, '-', linewidth=2, color=colors[i], 
                    label=f'{prop*100:.0f}% motorcycles')
            
            # Plot density-velocity relationship
            ax2.plot(densities, velocities, '-', linewidth=2, color=colors[i],
                    label=f'{prop*100:.0f}% motorcycles')
            
            # Find critical density (maximum flow)
            critical_idx = np.argmax(flows)
            critical_density = densities[critical_idx]
            critical_flow = flows[critical_idx]
            
            # Mark critical points
            ax1.plot(critical_density, critical_flow, 'o', markersize=6, color=colors[i])
            ax1.annotate(f'{critical_flow:.0f} veh/h', 
                        xy=(critical_density, critical_flow),
                        xytext=(5, 5),
                        textcoords='offset points',
                        fontsize=8)
        
        # Set labels and titles
        ax1.set_xlabel('Density (veh/km)')
        ax1.set_ylabel('Flow (veh/h)')
        ax1.set_title('Flow-Density Diagram with Varying Motorcycle Proportions')
        ax1.grid(alpha=0.3)
        ax1.legend()
        
        ax2.set_xlabel('Density (veh/km)')
        ax2.set_ylabel('Average velocity (km/h)')
        ax2.set_title('Velocity-Density Diagram with Varying Motorcycle Proportions')
        ax2.grid(alpha=0.3)
        ax2.legend()
        
        plt.suptitle('Impact of Motorcycle Proportion on Traffic Flow', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust for suptitle
        
        if save:
            filename = f"{self.model_name.lower()}_multiclass_fundamental_diagrams.png"
            save_path = os.path.join(self.output_dir, filename)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
