"""
Examples demonstrating how to use the visualization components of the traffic simulation package
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from src.visualization import SimulationPlotter, MulticlassPlotter, MotorcycleImpactVisualizer

def create_synthetic_data():
    """Create synthetic data for visualization examples."""
    # Grid setup
    x_grid = np.linspace(0, 10, 100)  # 10 km road
    t_grid = np.linspace(0, 1, 100)   # 1 hour simulation
    
    # Create meshgrid for generating 2D data
    X, T = np.meshgrid(x_grid, t_grid)
    
    # Single class data
    density = 20 * np.exp(-0.5 * ((X - 5 - 3*T) / 1.5) ** 2)  # Moving Gaussian
    velocity = 60 * (1 - density / 120)  # Greenshields model
    velocity = np.maximum(velocity, 5)  # Minimum speed
    flow = density * velocity
    
    # Multiclass data - 3 classes
    class_names = ['Motorcycles', 'Cars', 'Trucks']
    class_props = [0.6, 0.3, 0.1]  # Proportions
    class_max_speeds = [80, 60, 40]  # km/h
    
    densities = {}
    velocities = {}
    flows = {}
    
    for i, name in enumerate(class_names):
        # Each class has different spatial distributions
        if name == 'Motorcycles':
            # Motorcycles concentrate more at the beginning
            class_density = density * class_props[i] * (1.2 - 0.04 * X)
        elif name == 'Cars':
            # Cars uniformly distributed
            class_density = density * class_props[i] * np.ones_like(X)
        else:
            # Trucks concentrate more at the end
            class_density = density * class_props[i] * (0.8 + 0.04 * X)
            
        # Velocities for each class
        class_velocity = class_max_speeds[i] * (1 - density / 120)
        class_velocity = np.maximum(class_velocity, class_max_speeds[i] / 10)
        
        # Flows for each class
        class_flow = class_density * class_velocity
        
        densities[name] = class_density
        velocities[name] = class_velocity
        flows[name] = class_flow
    
    # Total values
    total_density = sum(densities.values())
    mean_velocity = sum(flows.values()) / total_density
    mean_velocity = np.nan_to_num(mean_velocity, nan=0.0)  # Replace NaN with 0
    total_flow = sum(flows.values())
    
    return {
        'x_grid': x_grid,
        't_grid': t_grid,
        'density': density,
        'velocity': velocity,
        'flow': flow,
        'densities': densities,
        'velocities': velocities,
        'flows': flows,
        'total_density': total_density,
        'mean_velocity': mean_velocity,
        'total_flow': total_flow
    }

def example_basic_visualization():
    """Demonstrate basic visualization capabilities."""
    print("Generating basic visualization examples...")
    data = create_synthetic_data()
    
    # Create output directory
    output_dir = 'outputs/visualization_examples/basic'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create plotter
    plotter = SimulationPlotter(model_name="LWR Example", output_dir=output_dir)
    
    # Generate individual plots
    plotter.plot_density_evolution(data['density'], data['x_grid'], data['t_grid'], 
                                 title="LWR Density Evolution", show=False, save=True)
    
    plotter.plot_velocity_evolution(data['velocity'], data['x_grid'], data['t_grid'],
                                  title="LWR Velocity Evolution", show=False, save=True)
    
    plotter.plot_flow_evolution(data['flow'], data['x_grid'], data['t_grid'],
                              title="LWR Flow Evolution", show=False, save=True)
    
    # Generate space profiles
    plotter.plot_space_profiles(data['density'], data['velocity'], data['flow'],
                              data['x_grid'], data['t_grid'], show=False, save=True)
    
    # Generate combined evolution plot
    plotter.plot_combined_evolution(data['density'], data['velocity'], data['flow'],
                                  data['x_grid'], data['t_grid'], 
                                  title="Combined Traffic Evolution", show=False, save=True)
    
    print(f"Basic visualization examples saved to {output_dir}")

def example_multiclass_visualization():
    """Demonstrate multiclass visualization capabilities."""
    print("Generating multiclass visualization examples...")
    data = create_synthetic_data()
    
    # Create output directory
    output_dir = 'outputs/visualization_examples/multiclass'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create plotter
    plotter = MulticlassPlotter(model_name="Multiclass LWR Example", output_dir=output_dir)
    
    # Create dashboard
    results = {
        'densities': data['densities'],
        'velocities': data['velocities'],
        'flows': data['flows'],
        'total_density': data['total_density'],
        'mean_velocity': data['mean_velocity'],
        'total_flow': data['total_flow']
    }
    
    plotter.create_dashboard(results, data['x_grid'], data['t_grid'], show=False, save=True)
    
    # Class comparison at specific time
    time_idx = len(data['t_grid']) // 2  # Middle time point
    class_densities = [data['densities'][name][time_idx] for name in ['Motorcycles', 'Cars', 'Trucks']]
    plotter.plot_multiclass_comparison(class_densities, ['Motorcycles', 'Cars', 'Trucks'], 
                                     data['x_grid'], 0, title="Vehicle Class Comparison", show=False, save=True)
    
    # Space-time class comparison
    plotter.plot_spacetime_class_comparison(data['densities'], data['x_grid'], data['t_grid'], show=False, save=True)
    
    print(f"Multiclass visualization examples saved to {output_dir}")

def example_motorcycle_visualization():
    """Demonstrate motorcycle-specific visualization capabilities."""
    print("Generating motorcycle-specific visualization examples...")
    data = create_synthetic_data()
    
    # Create output directory
    output_dir = 'outputs/visualization_examples/motorcycle'
    os.makedirs(output_dir, exist_ok=True)
    
    # Create motorcycle visualizer
    moto_viz = MotorcycleImpactVisualizer(model_name="Motorcycle Analysis", output_dir=output_dir)
    
    # Create data with different gamma values (gap-filling parameter)
    gamma_densities = {}
    gamma_velocities = {}
    
    for gamma in [0.0, 0.2, 0.4, 0.6]:
        gamma_densities[gamma] = {name: array.copy() for name, array in data['densities'].items()}
        gamma_velocities[gamma] = {name: array.copy() for name, array in data['velocities'].items()}
        
        # Apply gap-filling effect to motorcycles
        if gamma > 0:
            rho_m = gamma_densities[gamma]['Motorcycles']
            rho_max_m = 120
            gamma_velocities[gamma]['Motorcycles'] *= (1 + gamma * (rho_m / rho_max_m))
    
    # Visualize gap-filling effect
    moto_viz.visualize_gap_filling_effect(gamma_densities, gamma_velocities, 
                                        data['x_grid'], data['t_grid'], 
                                        gamma_values=[0.0, 0.2, 0.4, 0.6],
                                        show=False, save=True)
    
    # Create data with different lambda values (road quality parameter)
    lambda_values = {
        (0, 2): 0.95,    # Good asphalt (0-2 km)
        (2, 4): 0.75,    # Worn asphalt (2-4 km)
        (4, 6): 0.60,    # Paved road (4-6 km)
        (6, 8): 0.40,    # Compacted earth (6-8 km)
        (8, 10): 0.90    # Good asphalt again (8-10 km)
    }
    
    # Visualize road surface impact
    moto_viz.visualize_road_surface_impact(data['densities'], data['velocities'], 
                                         lambda_values, data['x_grid'], data['t_grid'],
                                         show=False, save=True)
    
    # Create beta values (interweaving sensitivity)
    beta_values = {
        'Cars': 0.3,
        'Trucks': 0.6
    }
    
    # Visualize interweaving effect
    moto_viz.visualize_interweaving_effect(data['densities'], data['velocities'], 
                                         data['x_grid'], data['t_grid'], beta_values,
                                         show=False, save=True)
    
    print(f"Motorcycle-specific visualization examples saved to {output_dir}")

if __name__ == "__main__":
    print("Running visualization examples...")
    example_basic_visualization()
    example_multiclass_visualization()
    example_motorcycle_visualization()
    print("All visualization examples completed.")
