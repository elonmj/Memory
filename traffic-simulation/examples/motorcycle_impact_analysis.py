"""
Motorcycle Impact Analysis

This script analyzes the impact of motorcycles on traffic flow,
particularly focusing on the gap-filling behavior and its effect on capacity.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import required modules
from src.models.multiclass_lwr_model import MulticlassLWRModel
from src.analysis.flow_capacity_analyzer import FlowCapacityAnalyzer
from src.visualization.fundamental_plotter import FundamentalDiagramPlotter
from scenarios.rarefaction_wave import RarefactionWaveScenario
from scenarios.multiclass_scenarios import GapFillingScenario
from config.simulation_config import VEHICLE_CLASSES, BENIN_LOCATIONS


def create_base_model():
    """
    Create a base multiclass model for comparison.
    
    Returns:
        MulticlassLWRModel: Base model with standard parameters
    """
    # Extract default parameters from config
    moto_params = VEHICLE_CLASSES["motorcycle"].copy()
    car_params = VEHICLE_CLASSES["car"].copy()
    
    # Create multiclass model
    model = MulticlassLWRModel(
        vehicle_classes=[moto_params, car_params],
        n_classes=2
    )
    
    return model


def analyze_gap_filling_effect():
    """
    Analyze how the gap-filling parameter affects traffic flow.
    """
    output_dir = "results/motorcycle_impact/gap_filling"
    os.makedirs(output_dir, exist_ok=True)
    
    # Range of gap-filling parameters to test
    eta_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    
    # Motorcycle proportions to test
    moto_proportions = [0.25, 0.5, 0.75]
    
    # Create models with different gap-filling parameters
    models = {}
    for eta in eta_values:
        # Create model with specific gap-filling parameter
        moto_params = VEHICLE_CLASSES["motorcycle"].copy()
        moto_params["eta"] = eta
        car_params = VEHICLE_CLASSES["car"].copy()
        
        model = MulticlassLWRModel(
            vehicle_classes=[moto_params, car_params],
            n_classes=2
        )
        
        models[f"eta={eta}"] = model
    
    # Plot fundamental diagrams for different eta values
    plotter = FundamentalDiagramPlotter("GapFilling", output_dir)
    plotter.compare_fundamental_diagrams(
        models,
        density_range=(0, 200),
        n_points=100,
        show=False,
        save=True,
        filename="gap_filling_comparison"
    )
    
    # Analyze capacity for different combinations of eta and moto proportion
    results = {}
    for eta in eta_values:
        model = models[f"eta={eta}"]
        analyzer = FlowCapacityAnalyzer(model)
        
        # Calculate flow capacity for different moto proportions
        capacities = []
        for prop in moto_proportions:
            max_flow, critical_density, _, _ = analyzer.calculate_maximum_flow(prop)
            capacities.append(max_flow)
        
        results[eta] = capacities
    
    # Create bar chart comparing capacities
    plt.figure(figsize=(12, 8))
    bar_width = 0.15
    index = np.arange(len(moto_proportions))
    
    for i, eta in enumerate(eta_values):
        plt.bar(
            index + i*bar_width, 
            results[eta], 
            bar_width,
            label=f'η = {eta}',
            alpha=0.7
        )
    
    plt.xlabel('Motorcycle Proportion')
    plt.ylabel('Maximum Flow (veh/h)')
    plt.title('Impact of Gap-Filling Parameter (η) on Traffic Capacity')
    plt.xticks(index + bar_width * (len(eta_values) - 1) / 2, [f'{p*100}%' for p in moto_proportions])
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'gap_filling_capacity_impact.png'), dpi=300)
    
    # Create scenario to demonstrate gap-filling
    demo_model = models["eta=0.3"]  # Use model with middle eta value
    run_gap_filling_scenario(demo_model, output_dir)
    
    print(f"Gap-filling analysis completed. Results saved to {output_dir}")


def analyze_interweaving_effect():
    """
    Analyze how the interweaving sensitivity affects traffic flow.
    """
    output_dir = "results/motorcycle_impact/interweaving"
    os.makedirs(output_dir, exist_ok=True)
    
    # Range of interweaving sensitivity parameters to test
    beta_values = [0.0, 0.2, 0.3, 0.4, 0.6]
    
    # Motorcycle proportions to test
    moto_proportions = [0.25, 0.5, 0.75]
    
    # Create models with different interweaving parameters
    models = {}
    for beta in beta_values:
        # Create model with specific interweaving parameter
        moto_params = VEHICLE_CLASSES["motorcycle"].copy()
        car_params = VEHICLE_CLASSES["car"].copy()
        car_params["beta"] = beta
        
        model = MulticlassLWRModel(
            vehicle_classes=[moto_params, car_params],
            n_classes=2
        )
        
        models[f"beta={beta}"] = model
    
    # Plot fundamental diagrams for different beta values
    plotter = FundamentalDiagramPlotter("Interweaving", output_dir)
    plotter.compare_fundamental_diagrams(
        models,
        density_range=(0, 200),
        n_points=100,
        show=False,
        save=True,
        filename="interweaving_comparison"
    )
    
    # Analyze capacity for different combinations of beta and moto proportion
    results = {}
    for beta in beta_values:
        model = models[f"beta={beta}"]
        analyzer = FlowCapacityAnalyzer(model)
        
        # Calculate flow capacity for different moto proportions
        capacities = []
        for prop in moto_proportions:
            max_flow, critical_density, _, _ = analyzer.calculate_maximum_flow(prop)
            capacities.append(max_flow)
        
        results[beta] = capacities
    
    # Create bar chart comparing capacities
    plt.figure(figsize=(12, 8))
    bar_width = 0.15
    index = np.arange(len(moto_proportions))
    
    for i, beta in enumerate(beta_values):
        plt.bar(
            index + i*bar_width, 
            results[beta], 
            bar_width,
            label=f'β = {beta}',
            alpha=0.7
        )
    
    plt.xlabel('Motorcycle Proportion')
    plt.ylabel('Maximum Flow (veh/h)')
    plt.title('Impact of Interweaving Sensitivity (β) on Traffic Capacity')
    plt.xticks(index + bar_width * (len(beta_values) - 1) / 2, [f'{p*100}%' for p in moto_proportions])
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'interweaving_capacity_impact.png'), dpi=300)
    
    print(f"Interweaving analysis completed. Results saved to {output_dir}")


def run_gap_filling_scenario(model, output_dir):
    """
    Run a scenario demonstrating the gap-filling effect.
    
    Args:
        model: MulticlassLWRModel instance with appropriate parameters
        output_dir: Directory to save results
    """
    # Parameters for gap filling scenario
    params = {
        'domain_length': 5.0,
        'simulation_time': 0.25,
        'dx': 0.02,
        'car_density_ratio': 0.4,
        'moto_density_ratios': [0.0, 0.2, 0.4, 0.6],
        'output_dir': output_dir
    }
    
    # Run scenario
    scenario = GapFillingScenario(model, "GapFillingDemo")
    results = scenario.run(params)
    scenario.save_results()
    
    # Create visualizations
    from src.visualization.multiclass_plotter import MulticlassPlotter
    plotter = MulticlassPlotter("GapFillingDemo", output_dir)
    plotter.plot_all(results, show=False, save=True)
    
    # Create a special dashboard highlighting the gap-filling effect
    plotter.create_dashboard(results, show=False, save=True)
    
    print(f"Gap-filling scenario completed. Results saved to {output_dir}")


def simulate_benin_locations():
    """
    Simulate traffic conditions at different Benin locations.
    """
    output_dir = "results/motorcycle_impact/benin_locations"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create base model
    base_model = create_base_model()
    
    # For each location in the config
    location_results = {}
    for loc_name, loc_data in BENIN_LOCATIONS.items():
        print(f"Simulating traffic at {loc_name}...")
        
        # Extract location parameters
        moto_proportion = loc_data.get('moto_proportion', 0.5)
        road_type = loc_data.get('road_type', 'bitumen_good')
        typical_density_ratio = loc_data.get('typical_density', 0.3)
        
        # Create a scenario based on the location data
        scenario_params = {
            'domain_length': 10.0,
            'simulation_time': 0.2,
            'dx': 0.05,
            'upstream_density': typical_density_ratio,
            'downstream_density': typical_density_ratio * 0.5,  # Lower density downstream
            'transition_point': 0.7,  # Transition near the end
            'output_dir': os.path.join(output_dir, loc_name)
        }
        
        # Define a road quality function based on the location
        if 'sections' in loc_data:
            # Location has variable road quality sections
            sections = loc_data['sections']
            
            def road_quality_func(x):
                for section in sections:
                    start = section['position']
                    end = start + section['length']
                    if start <= x < end:
                        from src.models.vc_modulations import road_quality_coefficient
                        return road_quality_coefficient(section['road_type'], 0)  # Get for motorcycle class
                return road_quality_coefficient(road_type, 0)
                
        else:
            # Uniform road quality
            from src.models.vc_modulations import road_quality_coefficient
            road_quality_func = lambda x: road_quality_coefficient(road_type, 0)
        
        # Create and run scenario
        scenario = RarefactionWaveScenario(base_model, f"Benin-{loc_name}")
        
        # Define initial density function with appropriate motorcycle proportion
        def initial_density_func(x):
            # Get base density from scenario
            base_density = scenario.get_initial_density(x)
            
            # If it's already an array (multiclass), adjust the proportions
            if isinstance(base_density, list):
                total_density = sum(base_density)
                return [total_density * moto_proportion, total_density * (1 - moto_proportion)]
            else:
                # Single class, convert to multiclass with proper proportions
                return [base_density * moto_proportion, base_density * (1 - moto_proportion)]
        
        # Run simulation with location-specific parameters and custom initial density
        params = scenario_params.copy()
        params['road_quality_func'] = road_quality_func
        
        # Run simulation
        results = base_model.simulate(
            initial_density=initial_density_func,
            domain_length=params['domain_length'],
            simulation_time=params['simulation_time'],
            dx=params['dx'],
            road_quality_func=road_quality_func
        )
        
        # Add metadata
        results['name'] = f"Benin-{loc_name}"
        results['location'] = loc_data
        
        # Store results
        location_results[loc_name] = results
        
        # Create visualizations
        loc_output_dir = os.path.join(output_dir, loc_name)
        os.makedirs(loc_output_dir, exist_ok=True)
        
        from src.visualization.multiclass_plotter import MulticlassPlotter
        plotter = MulticlassPlotter(f"Benin-{loc_name}", loc_output_dir)
        plotter.plot_all(results, show=False, save=True)
        
        # Create a specialized dashboard
        plotter.create_dashboard(results, show=False, save=True)
    
    # Compare results across different locations
    if len(location_results) > 1:
        compare_locations(location_results, output_dir)
        
    print(f"Benin location simulations completed. Results saved to {output_dir}")
    
    return location_results


def compare_locations(location_results, output_dir):
    """
    Compare traffic patterns across different Benin locations.
    
    Args:
        location_results: Dictionary of simulation results by location
        output_dir: Directory to save comparison results
    """
    from src.visualization.density_profile_plotter import DensityProfilePlotter
    
    # Create a plotter for comparisons
    plotter = DensityProfilePlotter(os.path.join(output_dir, "comparisons"))
    
    # Compare density profiles
    results_list = list(location_results.values())
    labels = list(location_results.keys())
    
    # Get middle time point for each simulation
    time_indices = [len(r['grid_t'])//2 for r in results_list]
    
    # Compare overall density
    plotter.plot_spatial_profile(
        results_list, 
        time_indices=time_indices, 
        labels=labels,
        title="Density Comparison Across Benin Locations",
        show=False,
        save=True
    )
    
    # Compare motorcycle density specifically
    if all('class_densities' in r for r in results_list):
        # Extract motorcycle densities (class 0)
        moto_results = []
        for result in results_list:
            moto_result = result.copy()
            moto_result['density'] = result['class_densities'][0]
            moto_results.append(moto_result)
            
        plotter.plot_spatial_profile(
            moto_results, 
            time_indices=time_indices, 
            labels=labels,
            title="Motorcycle Density Comparison Across Benin Locations",
            show=False,
            save=True
        )
    
    # Create summary of capacity statistics
    create_location_capacity_summary(location_results, os.path.join(output_dir, "capacity_summary.png"))


def create_location_capacity_summary(location_results, output_path):
    """
    Create a summary visualization of capacity statistics across locations.
    
    Args:
        location_results: Dictionary of simulation results by location
        output_path: Path to save the output image
    """
    locations = list(location_results.keys())
    max_flows = []
    moto_proportions = []
    
    # Extract maximum flow and motorcycle proportion for each location
    for loc, result in location_results.items():
        max_flows.append(np.max(result['flow']))
        
        # Get motorcycle proportion
        if 'location' in result:
            moto_proportions.append(result['location'].get('moto_proportion', 0.5))
        else:
            # Estimate from class densities if available
            if 'class_densities' in result:
                total_density = np.sum(result['density'])
                moto_density = np.sum(result['class_densities'][0])
                if total_density > 0:
                    moto_proportions.append(moto_density / total_density)
                else:
                    moto_proportions.append(0.5)
            else:
                moto_proportions.append(0.5)
    
    # Create a bar chart of maximum flows
    plt.figure(figsize=(12, 7))
    
    # Create colormap based on motorcycle proportion
    colors = plt.cm.plasma(np.array(moto_proportions))
    
    # Create bars
    bar_positions = np.arange(len(locations))
    bars = plt.bar(bar_positions, max_flows, color=colors)
    
    # Add annotations
    for i, (bar, prop) in enumerate(zip(bars, moto_proportions)):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 100,
                f'{prop*100:.0f}% motos', 
                ha='center', va='bottom', rotation=0, color='black')
    
    # Set labels and title
    plt.xlabel('Location')
    plt.ylabel('Maximum Flow (veh/h)')
    plt.title('Traffic Capacity Comparison Across Benin Locations')
    plt.xticks(bar_positions, locations, rotation=45, ha='right')
    plt.tight_layout()
    