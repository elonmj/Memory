"""
Flow Capacity Analysis Tool

This module provides tools for analyzing how traffic flow capacity 
changes with different vehicle class distributions, particularly 
focusing on the impact of motorcycles.
"""

import numpy as np
import matplotlib.pyplot as plt


class FlowCapacityAnalyzer:
    """Analyzer for studying flow capacity variations in multiclass traffic."""
    
    def __init__(self, model):
        """
        Initialize the analyzer with a traffic model.
        
        Args:
            model: Traffic model instance (should be multiclass)
        """
        self.model = model
        if not hasattr(model, 'n_classes') or model.n_classes < 2:
            raise ValueError("FlowCapacityAnalyzer requires a multiclass model with at least 2 classes")
    
    def calculate_maximum_flow(self, moto_proportion, total_density=None):
        """
        Calculate maximum flow achievable with a given motorcycle proportion.
        
        Args:
            moto_proportion: Proportion of motorcycles in the traffic (0-1)
            total_density: If provided, uses this density instead of finding critical
                          density for maximum flow
            
        Returns:
            tuple: (maximum flow, critical density, motorcycle density, other densities)
        """
        # Check if proportion is valid
        if not 0 <= moto_proportion <= 1:
            raise ValueError("Motorcycle proportion must be between 0 and 1")
        
        if total_density is None:
            # We need to find the critical density that maximizes flow
            # Use a simple grid search approach
            max_density = max(vc.rho_max for vc in self.model.vehicle_classes)
            test_densities = np.linspace(0, max_density, 100)
            max_flow = 0
            critical_density = 0
            
            for rho in test_densities:
                # Calculate class densities based on proportion
                rho_moto = rho * moto_proportion
                rho_others = [(rho * (1 - moto_proportion)) / (self.model.n_classes - 1)] * (self.model.n_classes - 1)
                class_densities = [rho_moto] + rho_others
                
                # Calculate total flow
                flow = sum(class_densities[i] * self.model.get_velocity(
                    rho, i, rho_moto if i > 0 else None) 
                    for i in range(self.model.n_classes))
                
                if flow > max_flow:
                    max_flow = flow
                    critical_density = rho
            
            # Calculate class densities at critical density
            rho_moto = critical_density * moto_proportion
            rho_others = [(critical_density * (1 - moto_proportion)) / (self.model.n_classes - 1)] * (self.model.n_classes - 1)
            
            return max_flow, critical_density, rho_moto, rho_others
        else:
            # Use provided total density
            rho_moto = total_density * moto_proportion
            rho_others = [(total_density * (1 - moto_proportion)) / (self.model.n_classes - 1)] * (self.model.n_classes - 1)
            class_densities = [rho_moto] + rho_others
            
            # Calculate flow at provided density
            flow = sum(class_densities[i] * self.model.get_velocity(
                total_density, i, rho_moto if i > 0 else None) 
                for i in range(self.model.n_classes))
            
            return flow, total_density, rho_moto, rho_others
    
    def analyze_moto_proportion_impact(self, proportions=None, save_path=None):
        """
        Analyze how different motorcycle proportions impact the flow capacity.
        
        Args:
            proportions: List of motorcycle proportions to analyze (0-1)
            save_path: Path to save the plot (if None, plot is displayed)
            
        Returns:
            tuple: (proportions, max_flows, critical_densities)
        """
        if proportions is None:
            proportions = np.linspace(0, 0.9, 10)  # 0% to 90% motorcycles
        
        max_flows = []
        critical_densities = []
        
        for prop in proportions:
            max_flow, critical_density, _, _ = self.calculate_maximum_flow(prop)
            max_flows.append(max_flow)
            critical_densities.append(critical_density)
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot flow capacity vs moto proportion
        ax1.plot(proportions, max_flows, 'b-o', linewidth=2)
        ax1.set_xlabel('Proportion de motocycles')
        ax1.set_ylabel('Capacité maximum (véh/h)')
        ax1.set_title('Impact de la proportion de motocycles sur la capacité')
        ax1.grid(True)
        
        # Normalize to baseline (0% motorcycles)
        baseline_flow = max_flows[0]
        normalized_flows = [flow / baseline_flow for flow in max_flows]
        
        # Add text annotations for percentage increase
        for i, (prop, norm_flow) in enumerate(zip(proportions, normalized_flows)):
            if i > 0:  # Skip baseline
                percent_increase = (norm_flow - 1) * 100
                ax1.annotate(f"+{percent_increase:.1f}%", 
                             xy=(prop, max_flows[i]),
                             xytext=(0, 10),
                             textcoords='offset points',
                             ha='center',
                             fontsize=8)
        
        # Plot critical density vs moto proportion
        ax2.plot(proportions, critical_densities, 'r-o', linewidth=2)
        ax2.set_xlabel('Proportion de motocycles')
        ax2.set_ylabel('Densité critique (véh/km)')
        ax2.set_title('Impact de la proportion de motocycles sur la densité critique')
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
            
        return proportions, max_flows, critical_densities
    
    def create_fundamental_diagrams(self, moto_proportions=None, density_range=None, save_path=None):
        """
        Create fundamental diagrams for different motorcycle proportions.
        
        Args:
            moto_proportions: List of motorcycle proportions to analyze (0-1)
            density_range: Range of densities to consider (min, max)
            save_path: Path to save the plot (if None, plot is displayed)
            
        Returns:
            Figure object
        """
        if moto_proportions is None:
            moto_proportions = [0.0, 0.25, 0.5, 0.75]
        
        if density_range is None:
            max_density = max(vc.rho_max for vc in self.model.vehicle_classes)
            density_range = (0, max_density)
        
        densities = np.linspace(density_range[0], density_range[1], 100)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Different colors for different proportions
        colors = plt.cm.viridis(np.linspace(0, 1, len(moto_proportions)))
        
        for i, prop in enumerate(moto_proportions):
            flows = []
            velocities = []
            
            for rho in densities:
                flow, _, _, _ = self.calculate_maximum_flow(prop, rho)
                flows.append(flow)
                if rho > 0:
                    velocities.append(flow / rho)
                else:
                    velocities.append(0)
            
            # Plot density-flow relationship
            ax1.plot(densities, flows, label=f'{prop*100:.0f}% motos', 
                     color=colors[i], linewidth=2)
            
            # Plot density-velocity relationship
            ax2.plot(densities, velocities, label=f'{prop*100:.0f}% motos', 
                     color=colors[i], linewidth=2)
            
            # Find and mark the max flow point
            max_flow_idx = np.argmax(flows)
            max_flow = flows[max_flow_idx]
            critical_density = densities[max_flow_idx]
            
            ax1.plot(critical_density, max_flow, 'o', color=colors[i])
            ax1.annotate(f'$q_{{max}}$={max_flow:.0f}', 
                         xy=(critical_density, max_flow),
                         xytext=(10, 0),
                         textcoords='offset points',
                         fontsize=8)
        
        ax1.set_xlabel('Densité totale (véh/km)')
        ax1.set_ylabel('Flux total (véh/h)')
        ax1.set_title('Diagramme fondamental flux-densité')
        ax1.grid(True)
        ax1.legend()
        
        ax2.set_xlabel('Densité totale (véh/km)')
        ax2.set_ylabel('Vitesse moyenne (km/h)')
        ax2.set_title('Relation vitesse-densité')
        ax2.grid(True)
        ax2.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
            
        return fig