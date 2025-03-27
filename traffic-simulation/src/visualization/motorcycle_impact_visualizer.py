import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
import os
from .multiclass_plotter import MulticlassPlotter
import matplotlib.colors as mcolors

class MotorcycleImpactVisualizer(MulticlassPlotter):
    """
    Specialized visualization class for analyzing and visualizing the specific impacts
    of motorcycles in multiclass traffic simulations, particularly focusing on
    gap-filling behavior and road surface effects.
    """
    
    def __init__(self, model_name="Motorcycle Impact Analysis", output_dir="outputs/motorcycle_analysis"):
        """
        Initialize the motorcycle impact visualizer.
        
        Parameters:
        -----------
        model_name : str
            Name of the model being visualized
        output_dir : str
            Directory where output figures will be saved
        """
        super().__init__(model_name, output_dir)
        
        # Add specialized colors for motorcycle analysis
        self.effect_colors = {
            'gap_filling': 'green',
            'interweaving': 'red',
            'road_impact': 'purple',
            'baseline': 'gray'
        }
        
        # Set motorcycle-specific class colors
        self.class_colors = {
            'motorcycles': '#ff7f0e',
            'cars': '#1f77b4',
            'trucks': '#2ca02c',
            'buses': '#d62728',
            'other': '#9467bd'
        }

    def _get_surface_type(self, lambda_value):
        """Helper method to convert lambda value to road surface type label."""
        if lambda_value >= 0.9:
            return "Good Asphalt"
        elif lambda_value >= 0.7:
            return "Worn Asphalt"
        elif lambda_value >= 0.5:
            return "Paved Road"
        elif lambda_value >= 0.3:
            return "Compacted Earth"
        else:
            return "Poor Road"

    def visualize_gap_filling_effect(self, densities, velocities, x_grid, t_grid, 
                                     gamma_values=None, title=None, show=True, save=True):
        """
        Creates a specialized visualization to demonstrate the gap-filling effect of motorcycles.
        
        Parameters:
        -----------
        densities : dict
            Dictionary with class densities for different gamma values
        velocities : dict
            Dictionary with class velocities for different gamma values
        x_grid : numpy.ndarray
            1D array of spatial grid points [km]
        t_grid : numpy.ndarray
            1D array of time grid points [h]
        gamma_values : list, optional
            List of gamma values used in simulations, if applicable
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
        if not isinstance(densities, dict) or not isinstance(velocities, dict):
            raise TypeError("Densities and velocities must be provided as dictionaries")
            
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # Plot 1: Motorcycle density vs. velocity for different gamma values
        if gamma_values:
            for gamma, density_dict in densities.items():
                if 'motorcycles' in density_dict:
                    moto_density = density_dict['motorcycles'].flatten()
                    moto_velocity = velocities[gamma]['motorcycles'].flatten()
                    
                    # Filter out zeros and NaNs
                    mask = (moto_density > 0) & ~np.isnan(moto_velocity)
                    
                    ax1.scatter(moto_density[mask], moto_velocity[mask], 
                               label=f'γ = {gamma}', alpha=0.7, s=20)
        else:
            # Assuming single simulation with motorcycle class
            for class_name, density in densities.items():
                if 'moto' in class_name.lower():
                    flat_density = density.flatten()
                    flat_velocity = velocities[class_name].flatten()
                    
                    # Filter out zeros and NaNs
                    mask = (flat_density > 0) & ~np.isnan(flat_velocity)
                    
                    ax1.scatter(flat_density[mask], flat_velocity[mask], 
                               label=class_name, color='blue', alpha=0.7, s=20)
        
        ax1.set_title('Motorcycle Density vs. Velocity')
        ax1.set_xlabel('Density (veh/km)')
        ax1.set_ylabel('Velocity (km/h)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Theoretical gap-filling effect visualization
        # Generate sample data to visualize the concept
        rho = np.linspace(0, 100, 1000)
        
        # Base velocity function (without gap-filling)
        v_base = 60 * (1 - rho/100)
        ax2.plot(rho, v_base, label='No Gap-filling (γ=0)', color='black', linestyle='--')
        
        # Velocity functions with different gamma values
        gamma_samples = [0.2, 0.4, 0.6, 0.8] if not gamma_values else gamma_values
        for gamma in gamma_samples:
            # Gap-filling velocity formula from the model extension
            v_gap = v_base * (1 + gamma * (rho/100))
            ax2.plot(rho, v_gap, label=f'γ = {gamma}')
            
        ax2.set_title('Theoretical Gap-Filling Effect')
        ax2.set_xlabel('Motorcycle Density (% of max)')
        ax2.set_ylabel('Relative Velocity')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Set main title
        if title:
            fig.suptitle(title, fontsize=16)
        else:
            fig.suptitle(f'{self.model_name}: Motorcycle Gap-Filling Analysis', fontsize=16)
            
        plt.tight_layout()
        
        # Save figure if requested
        if save:
            save_title = title if title else f'{self.model_name}_gap_filling_effect'
            filename = f"{self.output_dir}/{save_title.replace(' ', '_').lower()}.png"
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                plt.savefig(filename)
                print(f"Figure saved as {os.path.abspath(filename)}")
            except Exception as e:
                print(f"Error saving figure: {e}")
        
        # Show figure if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
    
    def visualize_road_surface_impact(self, densities, velocities, lambda_values, 
                                     x_grid, t_grid, positions=None, title=None, show=True, save=True):
        """
        Visualizes the impact of road surface quality on different vehicle classes.
        
        Parameters:
        -----------
        densities : dict
            Dictionary with class densities for different positions
        velocities : dict
            Dictionary with class velocities for different positions
        lambda_values : dict
            Dictionary mapping position ranges to lambda values (road quality)
        x_grid : numpy.ndarray
            1D array of spatial grid points [km]
        t_grid : numpy.ndarray
            1D array of time grid points
        positions : list, optional
            Specific positions to analyze in detail
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
        # Create a figure with multiple subplots
        fig = plt.figure(figsize=(15, 12))
        gs = gridspec.GridSpec(3, 1, height_ratios=[1, 2, 2])
        
        # Plot 1: Road surface quality
        ax1 = fig.add_subplot(gs[0])
        
        # Plot lambda values to visualize road quality
        road_quality = np.ones_like(x_grid)
        for pos_range, lambda_val in lambda_values.items():
            # Assuming pos_range is a tuple (start, end)
            if isinstance(pos_range, tuple) and len(pos_range) == 2:
                start, end = pos_range
                mask = (x_grid >= start) & (x_grid <= end)
                road_quality[mask] = lambda_val
        
        ax1.plot(x_grid, road_quality, 'k-', linewidth=2)
        ax1.set_ylabel('Road Quality (λ)')
        ax1.set_title('Road Surface Quality Along Route')
        ax1.set_ylim(0, 1.1)
        ax1.grid(True, alpha=0.3)
        
        # Mark different road surface types
        for pos_range, lambda_val in lambda_values.items():
            if isinstance(pos_range, tuple) and len(pos_range) == 2:
                start, end = pos_range
                mid = (start + end) / 2
                surface_type = self._get_surface_type(lambda_val)
                ax1.text(mid, lambda_val + 0.05, surface_type, 
                        ha='center', va='bottom', fontsize=9,
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        
        # Plot 2: Velocity profiles at different positions for different vehicle classes
        ax2 = fig.add_subplot(gs[1])
        
        # If specific positions not provided, choose some representative points
        if positions is None:
            # Choose positions at different road qualities
            positions = []
            for pos_range in lambda_values.keys():
                if isinstance(pos_range, tuple) and len(pos_range) == 2:
                    positions.append((pos_range[0] + pos_range[1]) / 2)
        
        # For time evolution analysis, use the middle time point
        mid_time_idx = len(t_grid) // 2
        
        # Plot velocity for each vehicle class at specified positions
        class_names = list(densities.keys())
        positions = np.array(positions)
        position_indices = [np.abs(x_grid - pos).argmin() for pos in positions]
        
        for class_name in class_names:
            for i, pos_idx in enumerate(position_indices):
                vel = velocities[class_name][mid_time_idx, pos_idx]
                den = densities[class_name][mid_time_idx, pos_idx]
                
                # Skip if density is too low
                if den < 1e-3:
                    continue
                
                # Get the lambda value for this position
                pos = x_grid[pos_idx]
                lambda_val = None
                for pos_range, lam in lambda_values.items():
                    if isinstance(pos_range, tuple) and len(pos_range) == 2:
                        start, end = pos_range
                        if start <= pos <= end:
                            lambda_val = lam
                            break
                
                # Plot point with color based on vehicle class
                color = self.class_colors.get(class_name.lower(), 'gray')
                ax2.scatter(lambda_val, vel, color=color, s=100, alpha=0.7,
                          label=f"{class_name}" if i == 0 else "")
                
                # Add a text label
                ax2.text(lambda_val + 0.02, vel, f"{class_name} @ x={pos:.1f}", 
                        fontsize=8, va='center')
        
        # Customize the plot
        ax2.set_xlabel('Road Quality (λ)')
        ax2.set_ylabel('Velocity (km/h)')
        ax2.set_title('Velocity by Vehicle Class at Different Road Qualities')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 1.1)
        ax2.legend()
        
        # Plot 3: Density-velocity relationship colored by road quality
        ax3 = fig.add_subplot(gs[2])
        
        # Create normalized colormap for road quality
        norm = mcolors.Normalize(vmin=0, vmax=1)
        
        # Combine data from all positions for analysis
        for class_name in class_names:
            # Skip non-motorcycle classes
            if 'moto' not in class_name.lower() and 'motorcycle' not in class_name.lower():
                continue
                
            for t_idx in range(0, len(t_grid), max(1, len(t_grid) // 10)):  # Sample time points
                for pos_idx in range(len(x_grid)):
                    pos = x_grid[pos_idx]
                    
                    # Get lambda value for this position
                    lambda_val = None
                    for pos_range, lam in lambda_values.items():
                        if isinstance(pos_range, tuple) and len(pos_range) == 2:
                            start, end = pos_range
                            if start <= pos <= end:
                                lambda_val = lam
                                break
                    
                    if lambda_val is None:
                        continue
                        
                    den = densities[class_name][t_idx, pos_idx]
                    vel = velocities[class_name][t_idx, pos_idx]
                    
                    # Skip if values are too small
                    if den < 1e-3:
                        continue
                        
                    # Plot with color based on lambda value
                    ax3.scatter(den, vel, c=[lambda_val], cmap='viridis', 
                               norm=norm, s=20, alpha=0.5)
        
        # Add colorbar
        cbar = plt.colorbar(cm.ScalarMappable(norm=norm, cmap='viridis'), ax=ax3)
        cbar.set_label('Road Quality (λ)')
        
        ax3.set_xlabel('Density (veh/km)')
        ax3.set_ylabel('Velocity (km/h)')
        ax3.set_title('Motorcycle Density-Velocity Relationship by Road Quality')
        ax3.grid(True, alpha=0.3)
        
        # Set main title
        if title:
            fig.suptitle(title, fontsize=16)
        else:
            fig.suptitle(f'{self.model_name}: Road Surface Impact Analysis', fontsize=16)
        
        plt.tight_layout()
        
        # Save figure if requested
        if save:
            save_title = title if title else f'{self.model_name}_road_surface_impact'
            filename = f"{self.output_dir}/{save_title.replace(' ', '_').lower()}.png"
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                plt.savefig(filename)
                print(f"Figure saved as {os.path.abspath(filename)}")
            except Exception as e:
                print(f"Error saving figure: {e}")
        
        # Show figure if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
        
    def visualize_interweaving_effect(self, densities, velocities, x_grid, t_grid, beta_values=None, 
                                     title=None, show=True, save=True):
        """
        Visualizes the interweaving effect of motorcycles on other vehicle classes.
        
        Parameters:
        -----------
        densities : dict
            Dictionary with class densities for different beta values or scenarios
        velocities : dict
            Dictionary with class velocities for different beta values or scenarios
        x_grid : numpy.ndarray
            1D array of spatial grid points [km]
        t_grid : numpy.ndarray
            1D array of time grid points [h]
        beta_values : dict, optional
            Dictionary mapping class names to their beta (interweaving sensitivity) values
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
        # Create figure with 2x2 subplots
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))
        
        # Define analysis time points (start, 1/3, 2/3, end)
        time_points = [0, len(t_grid)//3, 2*len(t_grid)//3, len(t_grid)-1]
        time_labels = [f"t = {t_grid[idx]:.2f}h" for idx in time_points]
        
        # Plot 1: Motorcycle density vs. other vehicle velocities
        ax = axs[0, 0]
        
        # Extract motorcycle class
        moto_class = None
        for class_name in densities.keys():
            if 'moto' in class_name.lower() or 'motorcycle' in class_name.lower():
                moto_class = class_name
                break
                
        if moto_class:
            for class_name in densities.keys():
                if class_name == moto_class:
                    continue
                    
                # Collect motorcycle densities and corresponding velocities
                moto_densities = []
                class_velocities = []
                
                for t_idx in range(0, len(t_grid), max(1, len(t_grid)//50)):
                    for x_idx in range(len(x_grid)):
                        moto_den = densities[moto_class][t_idx, x_idx]
                        vel = velocities[class_name][t_idx, x_idx]
                        
                        # Only include points with significant density
                        if moto_den > 1e-3:
                            moto_densities.append(moto_den)
                            class_velocities.append(vel)
                
                if moto_densities:
                    ax.scatter(moto_densities, class_velocities, 
                              label=class_name, alpha=0.5, s=15)
            
            # Add best fit line to show trend
            if 'cars' in densities:
                # Collect data for cars specifically
                car_moto_densities = []
                car_velocities = []
                
                for t_idx in range(0, len(t_grid), max(1, len(t_grid)//50)):
                    for x_idx in range(len(x_grid)):
                        moto_den = densities[moto_class][t_idx, x_idx]
                        car_vel = velocities['cars'][t_idx, x_idx]
                        
                        if moto_den > 1e-3:
                            car_moto_densities.append(moto_den)
                            car_velocities.append(car_vel)
                
                if car_moto_densities:
                    # Simple linear regression for trend line
                    x = np.array(car_moto_densities)
                    y = np.array(car_velocities)
                    
                    # Try to fit a line using polynomial regression
                    try:
                        z = np.polyfit(x, y, 1)
                        p = np.poly1d(z)
                        
                        # Plot trend line
                        x_range = np.linspace(min(x), max(x), 100)
                        ax.plot(x_range, p(x_range), 'r--', 
                               label=f'Car velocity trend: y = {z[0]:.4f}x + {z[1]:.2f}')
                    except:
                        # If fitting fails, skip trend line
                        pass
            
        ax.set_xlabel('Motorcycle Density (veh/km)')
        ax.set_ylabel('Velocity of Other Classes (km/h)')
        ax.setTitle('Interweaving Effect: Motorcycle Density vs. Other Vehicle Velocities')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 2: Velocity profiles at selected times
        ax = axs[0, 1]
        
        # Plot velocity profiles for each class at selected times
        for t_idx in [time_points[1]]:  # Use second time point (1/3 through simulation)
            for class_name in densities.keys():
                ax.plot(x_grid, velocities[class_name][t_idx], 
                       label=f"{class_name}", linewidth=2)
                       
            # Add motorcycle density on secondary axis for reference
            if moto_class:
                ax2 = ax.twinx()
                ax2.plot(x_grid, densities[moto_class][t_idx], 'k--', 
                        label=f"{moto_class} density", alpha=0.5)
                ax2.set_ylabel(f'{moto_class} Density (veh/km)', color='k')
                
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Velocity (km/h)')
        ax.set_title(f'Velocity Profiles at {time_labels[1]}')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left')
        
        # Plot 3: Beta effect visualization (theoretical)
        ax = axs[1, 0]
        
        # Generate theoretical data
        rho_m = np.linspace(0, 50, 100)  # Motorcycle density
        rho_max_m = 50  # Maximum motorcycle density
        
        # Generate interweaving functions for different beta values
        beta_samples = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        for beta in beta_samples:
            # Interweaving function: f_i(ρ_M) = 1 - β_i * (ρ_M / ρ_{M,max})
            f_i = 1 - beta * (rho_m / rho_max_m)
            ax.plot(rho_m, f_i, label=f'β = {beta}')
            
        # If beta values provided, add points for actual values
        if beta_values:
            for class_name, beta in beta_values.items():
                if class_name != moto_class:
                    ax.plot(rho_max_m/2, 1 - beta * 0.5, 'o', markersize=10,
                           label=f'{class_name} (β={beta:.2f})')
                
        ax.set_xlabel('Motorcycle Density (veh/km)')
        ax.set_ylabel('Interweaving Function f_i(ρ_M)')
        ax.set_title('Theoretical Interweaving Effect for Different β Values')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Plot 4: Speed reduction at high motorcycle density regions
        ax = axs[1, 1]
        
        if moto_class:
            # Define motorcycle density threshold for analysis
            moto_density_threshold = 10  # veh/km
            
            # Collect data
            high_density_points = []
            low_density_points = []
            
            for class_name in densities.keys():
                if class_name == moto_class:
                    continue
                
                high_vel_values = []
                low_vel_values = []
                
                for t_idx in range(0, len(t_grid), max(1, len(t_grid)//10)):
                    for x_idx in range(len(x_grid)):
                        moto_den = densities[moto_class][t_idx, x_idx]
                        class_vel = velocities[class_name][t_idx, x_idx]
                        
                        if densities[class_name][t_idx, x_idx] < 1e-3:
                            continue
                            
                        if moto_den >= moto_density_threshold:
                            high_vel_values.append(class_vel)
                        else:
                            low_vel_values.append(class_vel)
                
                if high_vel_values and low_vel_values:
                    high_density_points.append((class_name, 
                                              np.mean(high_vel_values),
                                              np.std(high_vel_values)))
                    low_density_points.append((class_name,
                                             np.mean(low_vel_values),
                                             np.std(low_vel_values)))
            
            # Create grouped bar chart
            if high_density_points and low_density_points:
                class_names = [p[0] for p in high_density_points]
                high_means = [p[1] for p in high_density_points]
                high_stds = [p[2] for p in high_density_points]
                low_means = [p[1] for p in low_density_points]
                low_stds = [p[2] for p in low_density_points]
                
                bar_width = 0.35
                indices = np.arange(len(class_names))
                
                ax.bar(indices - bar_width/2, low_means, bar_width, 
                      label=f'Low Motorcycle Density (<{moto_density_threshold} veh/km)',
                      yerr=low_stds, capsize=5, color='lightblue')
                ax.bar(indices + bar_width/2, high_means, bar_width,
                      label=f'High Motorcycle Density (≥{moto_density_threshold} veh/km)',
                      yerr=high_stds, capsize=5, color='salmon')
                
                ax.set_xlabel('Vehicle Class')
                ax.set_ylabel('Mean Velocity (km/h)')
                ax.set_title('Effect of High Motorcycle Density on Other Vehicle Classes')
                ax.set_xticks(indices)
                ax.set_xticklabels(class_names)
                ax.grid(True, alpha=0.3, axis='y')
                ax.legend()
        else:
            ax.text(0.5, 0.5, 'Motorcycle class data not available', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Speed Reduction Analysis (Not Available)')
        
        # Set main title
        if title:
            fig.suptitle(title, fontsize=16)
        else:
            fig.suptitle(f'{self.model_name}: Motorcycle Interweaving Effect Analysis', fontsize=16)
        
        plt.tight_layout()
        
        # Save figure if requested
        if save:
            save_title = title if title else f'{self.model_name}_interweaving_effect'
            filename = f"{self.output_dir}/{save_title.replace(' ', '_').lower()}.png"
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                plt.savefig(filename)
                print(f"Figure saved as {os.path.abspath(filename)}")
            except Exception as e:
                print(f"Error saving figure: {e}")
        
        # Show figure if requested
        if show:
            plt.show()
        else:
            plt.close()
            
        return fig
