"""
Multiclass Comparison Example

This script demonstrates how to use the traffic simulation framework to compare 
different vehicle class distributions, with a focus on the impact of motorcycles.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import models and visualization tools
from src.models.multiclass_lwr_model import MulticlassLWRModel
from src.visualization.fundamental_plotter import FundamentalDiagramPlotter
from src.visualization.multiclass_plotter import MulticlassPlotter
from src.analysis.flow_capacity_analyzer import FlowCapacityAnalyzer
from scenarios.rarefaction_wave import RarefactionWaveScenario
from scenarios.multiclass_scenarios import DegradedRoadScenario


def setup_models():
    """
    Setup models with different vehicle class configurations.
    
    Returns:
        dict: Dictionary of model configurations
    """
    # Base model parameters
    v_max_car = 100.0   # km/h
    rho_max_car = 180.0  # veh/km
    
    # Configuration 1: Cars only
    car_only_model = MulticlassLWRModel(
        vehicle_classes=[
            {
                "name": "car",
                "v_max": v_max_car,
                "rho_max": rho_max_car,
                "beta": 0.0,
                "lambda_min": 0.6
            }
        ],
        n_classes=1
    )
    
    # Configuration 2: Standard mix (25% motorcycles, 75% cars)
    standard_mix_model = MulticlassLWRModel(
        vehicle_classes=[
            {
                "name": "moto",
                "v_max": 90.0,
                "rho_max": 200.0,
                "eta": 0.3,
                "lambda_min": 0.8
            },
            {
                "name": "car",
                "v_max": v_max_car,
                "rho_max": rho_max_car,
                "beta": 0.3,
                "lambda_min": 0.6
            }
        ],
        n_classes=2
    )
    
    # Configuration 3: Benin mix (75% motorcycles, 25% cars)
    benin_mix_model = MulticlassLWRModel(
        vehicle_classes=[
            {
                "name": "moto",
                "v_max": 90.0,
                "rho_max": 200.0,
                "eta": 0.3,
                "lambda_min": 0.8
            },
            {
                "name": "car",
                "v_max": v_max_car,
                "rho_max": rho_max_car,
                "beta": 0.3,
                "lambda_min": 0.6
            }
        ],
        n_classes=2
    )
    
    return {
        "Cars Only": car_only_model,
        "Standard Mix (25% motorcycles)": standard_mix_model,
        "Benin Mix (75% motorcycles)": benin_mix_model
    }


def compare_fundamental_diagrams(models):
    """
    Compare fundamental diagrams for different model configurations.
    
    Args:
        models: Dictionary of models to compare
    """
    output_dir = "results/comparison/fundamental_diagrams"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create fundamental diagram plotter
    fd_plotter = FundamentalDiagramPlotter("Comparison", output_dir)
    
    # Compare fundamental diagrams
    fig = fd_plotter.compare_fundamental_diagrams(
        models, 
        density_range=(0, 200),
        n_points=100,
        show=False,
        save=True,
        filename="model_comparison"
    )
    
    print(f"Fundamental diagram comparison saved to {output_dir}/model_comparison.png")
    
    # For the multiclass models, plot with different motorcycle proportions
    for name, model in models.items():
        if hasattr(model, 'n_classes') and model.n_classes > 1:
            fd_plotter.plot_multiclass_fundamental_diagrams(
                model,
                moto_proportions=[0.0, 0.25, 0.50, 0.75, 0.90],
                density_range=(0, 200),
                n_points=100,
                show=False,
                save=True
            )
            print(f"Multiclass fundamental diagrams for {name} saved to {output_dir}")


def run_rarefaction_scenario(models):
    """
    Run rarefaction wave scenario for different model configurations.
    
    Args:
        models: Dictionary of models to compare
        
    Returns:
        dict: Dictionary of simulation results
    """
    results = {}
    output_dir = "results/comparison/rarefaction"
    os.makedirs(output_dir, exist_ok=True)
    
    # Parameters for the scenario
    params = {
        'domain_length': 20.0,
        'simulation_time': 0.5,
        'dx': 0.1,
        'upstream_density': 0.7,
        'downstream_density': 0.1,
        'transition_point': 0.5,
        'output_dir': output_dir
    }
    
    # Run simulation for each model
    for name, model in models.items():
        print(f"\nRunning rarefaction wave scenario with {name}...")
        
        # Create and run scenario
        scenario = RarefactionWaveScenario(model, f"Rarefaction - {name}")
        result = scenario.run(params)
        results[name] = result
        
        # Save results
        scenario.save_results()
        
        # Create a multiclass plotter for visualization
        plotter = MulticlassPlotter(name, os.path.join(output_dir, name.replace(" ", "_")))
        
        # If multiclass, create a dashboard
        if hasattr(model, 'n_classes') and model.n_classes > 1:
            plotter.create_dashboard(result, show=False, save=True)
    
    return results


def run_degraded_road_scenario(models):
    """
    Run degraded road scenario for different model configurations.
    
    Args:
        models: Dictionary of models to compare
        
    Returns:
        dict: Dictionary of simulation results
    """
    # Only use multiclass models for this scenario
    multiclass_models = {name: model for name, model in models.items() 
                         if hasattr(model, 'n_classes') and model.n_classes > 1}
    
    if not multiclass_models:
        print("No multiclass models available for degraded road scenario")
        return {}
    
    results = {}
    output_dir = "results/comparison/degraded_road"
    os.makedirs(output_dir, exist_ok=True)
    
    # Parameters for the scenario
    params = {
        'domain_length': 10.0,
        'simulation_time': 0.2,
        'dx': 0.05,
        'density': 0.3,
        'degraded_start': 3.0,
        'degraded_end': 7.0,
        'quality_good': 1.0,
        'quality_bad': 0.6,
        'output_dir': output_dir
    }
    
    # Run simulation for each multiclass model
    for name, model in multiclass_models.items():
        print(f"\nRunning degraded road scenario with {name}...")
        
        # Create and run scenario
        scenario = DegradedRoadScenario(model, f"DegradedRoad - {name}")
        result = scenario.run(params)
        results[name] = result
        
        # Save results
        scenario.save_results()
        
        # Create a multiclass plotter for visualization
        plotter = MulticlassPlotter(name, os.path.join(output_dir, name.replace(" ", "_")))
        plotter.create_dashboard(result, show=False, save=True)
    
    return results


def analyze_flow_capacity(models):
    """
    Analyze flow capacity for different motorcycle proportions.
    
    Args:
        models: Dictionary of models to compare
    """
    # Only use multiclass models for this analysis
    multiclass_models = {name: model for name, model in models.items() 
                         if hasattr(model, 'n_classes') and model.n_classes > 1}
    
    if not multiclass_models:
        print("No multiclass models available for flow capacity analysis")
        return
    
    output_dir = "results/comparison/flow_capacity"
    os.makedirs(output_dir, exist_ok=True)
    
    for name, model in multiclass_models.items():
        print(f"\nAnalyzing flow capacity with {name}...")
        
        # Create flow capacity analyzer
        analyzer = FlowCapacityAnalyzer(model)
        
        # Analyze impact of motorcycle proportion
        proportions = np.linspace(0, 0.9, 10)
        save_path = os.path.join(output_dir, f"{name.replace(' ', '_')}_moto_impact.png")
        analyzer.analyze_moto_proportion_impact(proportions, save_path)
        
        # Create fundamental diagrams for different proportions
        save_path = os.path.join(output_dir, f"{name.replace(' ', '_')}_fund_diagrams.png")
        analyzer.create_fundamental_diagrams(
            moto_proportions=[0.0, 0.25, 0.5, 0.75, 0.9],
            save_path=save_path
        )


def compare_results(results_dict, scenario_name):
    """
    Compare and visualize results from different model configurations.
    
    Args:
        results_dict: Dictionary of simulation results
        scenario_name: Name of the scenario
    """
    output_dir = f"results/comparison/{scenario_name.lower()}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert results dict to list for the plotter
    results_list = list(results_dict.values())
    labels = list(results_dict.keys())
    
    # Create density profile plotter
    plotter = DensityProfilePlotter(output_dir)
    
    # Compare density profiles at middle time
    time_indices = [len(r['grid_t'])//2 for r in results_list]
    plotter.plot_spatial_profile(
        results_list, 
        time_indices=time_indices, 
        labels=labels,
        title=f"{scenario_name} - Density Profiles Comparison",
        show=False,
        save=True
    )
    
    # Compare density evolution at a specific location
    positions = [r['domain_length']/2 for r in results_list]
    plotter.plot_temporal_profile(
        results_list,
        positions=positions,
        labels=labels,
        title=f"{scenario_name} - Density Evolution Comparison",
        show=False,
        save=True
    )


def main():
    """Main function to run all comparisons."""
    print("Setting up models for comparison...")
    models = setup_models()
    
    print("\nComparing fundamental diagrams...")
    compare_fundamental_diagrams(models)
    
    print("\nRunning rarefaction wave scenario...")
    rarefaction_results = run_rarefaction_scenario(models)
    
    print("\nRunning degraded road scenario...")
    degraded_results = run_degraded_road_scenario(models)
    
    print("\nAnalyzing flow capacity...")
    analyze_flow_capacity(models)
    
    print("\nComparing simulation results...")
    if rarefaction_results:
        compare_results(rarefaction_results, "RarefactionWave")
    
    if degraded_results:
        compare_results(degraded_results, "DegradedRoad")
    
    print("\nAll comparisons completed. Results saved in the 'results/comparison' directory.")


if __name__ == "__main__":
    main()
