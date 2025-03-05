"""
Traffic Simulation Main Entry Point

This script serves as the main entry point for running traffic simulations.
It allows selecting different models (LWR, MulticlassLWR) and scenarios through
command-line arguments.
"""

import os
import argparse
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add the project root to the Python path
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

# Import models
from src.models.lwr_model import LWRModel
# Import multiclass models
from src.models.multiclass_lwr_model import MulticlassLWRModel

# Import scenarios
from scenarios.base_scenario import BaseScenario
from scenarios.rarefaction_wave import RarefactionWaveScenario
from scenarios.shock_wave import ShockWaveScenario
from scenarios.red_light import RedLightScenario  # Add import for RedLightScenario
from scenarios.traffic_jam import TrafficJamScenario  # Add import for TrafficJamScenario
from scenarios.multiclass_scenarios import (
   MulticlassRedLightScenario,
   DegradedRoadScenario, 
   GapFillingScenario
)

# Import visualization utilities
from src.visualization.fundamental_plotter import FundamentalDiagramPlotter
from src.visualization.simulation_plotter import SimulationPlotter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Traffic Simulation Framework")
    
    # Model selection
    parser.add_argument(
        "--model", 
        type=str, 
        choices=["lwr", "multiclass"],
        default="lwr",
        help="Traffic model to use"
    )
    
    # Scenario selection
    parser.add_argument(
        "--scenario", 
        type=str,
        choices=["rarefaction", "shock", "redlight", "degraded", "gapfilling", "trafficjam"],  # Add "trafficjam" option
        default="rarefaction",
        help="Traffic scenario to simulate"
    )
    
    # Simulation parameters
    parser.add_argument("--domain", type=float, default=20.0, help="Domain length (km)")
    parser.add_argument("--time", type=float, default=1.0, help="Simulation time (h)")
    parser.add_argument("--dx", type=float, default=0.1, help="Spatial step (km)")
    parser.add_argument("--dt", type=float, default=None, help="Time step (h), None for auto")
    parser.add_argument("--cfl", type=float, default=0.9, help="CFL safety factor")
    
    # Model parameters
    parser.add_argument("--vmax", type=float, default=100.0, help="Maximum velocity (km/h)")
    parser.add_argument("--rhomax", type=float, default=180.0, help="Maximum density (veh/km)")
    parser.add_argument("--classes", type=int, default=2, help="Number of vehicle classes")
    parser.add_argument("--eta", type=float, default=0.3, help="Gap-filling parameter")
    
    # Scenario-specific parameters
    parser.add_argument("--test_segment_length", type=float, default=5.0, help="Length of test segment (km)")
    
    # Traffic Jam specific parameters
    parser.add_argument("--left-density", type=float, default=0.7, help="Density ratio on the left side (Traffic Jam)")
    parser.add_argument("--right-density", type=float, default=0.1, help="Density ratio on the right side (Traffic Jam)")
    parser.add_argument("--transition-width", type=float, default=1.0, help="Width of transition zone (km)")
    parser.add_argument("--smooth", action="store_true", help="Use smooth transition in traffic jam scenario")
    
    # Visualization options
    parser.add_argument(
        "--plot", 
        type=str, 
        choices=["none", "basic", "all", "interactive"],
        default="basic",
        help="Plotting level"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        default="simulations",
        help="Output directory for results"
    )
    
    return parser.parse_args()


def create_model(args):
    """Create and return the appropriate traffic model based on arguments."""
    if args.model == "lwr":
        return LWRModel(v_max=args.vmax, rho_max=args.rhomax)
    
    elif args.model == "multiclass":
        # For multiclass, create vehicle classes with parameters
        # First class is motorcycles (default)
        vehicle_classes = []
        
        # Motorcycles
        motorcycle_params = {
            "name": "moto",
            "v_max": args.vmax * 0.9,  # Motorcycles slightly slower than max
            "rho_max": args.rhomax * 1.2,  # But can pack more densely
            "eta": args.eta,  # Gap-filling parameter
            "lambda_min": 0.8  # Less affected by road quality
        }
        
        # Cars
        car_params = {
            "name": "car",
            "v_max": args.vmax,  # Standard max velocity
            "rho_max": args.rhomax,  # Standard max density
            "beta": 0.3,  # Sensitivity to motorcycle interweaving
            "lambda_min": 0.6  # More affected by road quality
        }
        
        # Add more classes if specified
        if args.classes > 2:
            # Trucks/buses
            truck_params = {
                "name": "truck",
                "v_max": args.vmax * 0.7,  # Trucks slower
                "rho_max": args.rhomax * 0.7,  # Take more space
                "beta": 0.6,  # Very sensitive to motorcycle interweaving
                "lambda_min": 0.5  # Significantly affected by road quality
            }
            vehicle_classes.append(truck_params)
        
        return MulticlassLWRModel(
            vehicle_classes=[motorcycle_params, car_params] + vehicle_classes,
            n_classes=args.classes
        )
    
    else:
        raise ValueError(f"Unknown model type: {args.model}")


def create_scenario(args, model):
    """Create and return the appropriate scenario based on arguments."""
    # Define base simulation parameters common to all scenarios
    simulation_params = {
        'domain_length': args.domain,
        'simulation_time': args.time,
        'dx': args.dx,
        'dt': args.dt,
        'cfl_factor': args.cfl,
        'test_segment_length': args.test_segment_length,
        # Common scenario parameters
        'buffer_length': 2.0,  
        'transition_point': 0.5,  
        'upstream_density': 0.4,  
        'downstream_density': 0.3,
        'car_factor': 0.7,        
        'moto_factor': 1.2,
        # Red light scenario parameters
        'light_position': 3.0,
        'background_density': 0.2,
        'jam_density': 0.9,
        'jam_length': 0.5,
        'green_time': 0.05,
        # Degraded road parameters
        'degraded_start': 3.0,
        'degraded_end': 7.0,
        'quality_good': 1.0,
        'quality_bad': 0.6,
        'density': 0.3,
        # Add Traffic Jam specific parameters
        'left_density': args.left_density,
        'right_density': args.right_density,
        'transition_width': args.transition_width,
        'smooth_transition': args.smooth,
    }
    
    if args.scenario == "rarefaction":
        return RarefactionWaveScenario(model)
    
    elif args.scenario == "shock":  # Add shock wave case
        return ShockWaveScenario(model)
    
    elif args.scenario == "redlight":
        if args.model == "multiclass":
            return MulticlassRedLightScenario(model)
        else:
            # Use the proper RedLightScenario for LWR model
            return RedLightScenario(model)
    
    elif args.scenario == "degraded":
        if args.model == "multiclass":
            return DegradedRoadScenario(model)
        else:
            print("Warning: Degraded road scenario requires multiclass model.")
            return RarefactionWaveScenario(model)
    
    elif args.scenario == "gapfilling":
        if args.model == "multiclass":
            return GapFillingScenario(model)
        else:
            print("Warning: Gap filling scenario requires multiclass model.")
            return RarefactionWaveScenario(model)
    
    elif args.scenario == "trafficjam":  # Add traffic jam case
        return TrafficJamScenario(model)
    
    else:
        raise ValueError(f"Unknown scenario: {args.scenario}")


def visualize_results(results, args):
    """Generate visualizations based on simulation results."""
    # Create output directory
    model_name = args.model.upper()
    scenario_name = args.scenario
    output_dir = os.path.join(args.output, model_name, scenario_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create simulation plotter
    plotter = SimulationPlotter(model_name, output_dir)
    
    # Basic plots - always generate
    if args.plot != "none":
        # Plot time evolution of density
        plotter.plot_density_evolution(
            results['density'], 
            results['grid_x'], 
            results['grid_t'],
            title=f"{results['name']} - Density Evolution"
        )
        
        # Plot time evolution of velocity
        plotter.plot_velocity_evolution(
            results['velocity'], 
            results['grid_x'], 
            results['grid_t'],
            title=f"{results['name']} - Velocity Evolution"
        )
        
        # Plot time evolution of flow
        plotter.plot_flow_evolution(
            results['flow'], 
            results['grid_x'], 
            results['grid_t'],
            title=f"{results['name']} - Flow Evolution"
        )
        
        # Create a combined evolution plot
        plotter.plot_combined_evolution(
            results['density'],
            results['velocity'],
            results['flow'],
            results['grid_x'],
            results['grid_t'],
            title=f"{results['name']}"
        )
    
    # For multiclass model, generate class-specific plots
    if args.model == "multiclass" and args.plot in ["all", "interactive"]:
        # Plot individual class densities
        for i in range(results['n_classes']):
            class_name = f"Class {i}" if i < len(["Motorcycles", "Cars", "Trucks"]) else ["Motorcycles", "Cars", "Trucks"][i]
            plotter.plot_density_evolution(
                results['class_densities'][i], 
                results['grid_x'], 
                results['grid_t'],
                title=f"{results['name']} - {class_name} Density"
            )
    
    # Interactive visualization
    if args.plot == "interactive":
        plt.ion()
        plotter.create_interactive_visualization(results)
        plt.show()
        input("Press Enter to continue...")


def main():
    """Main entry point for the simulation."""
    args = parse_arguments()
    
    print(f"Running {args.model} model with {args.scenario} scenario.")
    
    # Create model
    model = create_model(args)
    
    # Create scenario
    scenario = create_scenario(args, model)
    
    # Prepare parameters
    # Calculate dt if not provided, using CFL condition
    if args.dt is None:
        dt = args.cfl * args.dx / args.vmax  # Ensure CFL condition
    else:
        dt = float(args.dt)  # Convert to scalar

    # CRITICAL FIX: Ensure all required parameters are included for all scenarios
    params = {
        'domain_length': float(args.domain),
        'simulation_time': float(args.time),
        'dx': float(args.dx),
        'dt': dt,
        'cfl_factor': float(args.cfl),
        'test_segment_length': float(args.test_segment_length),
        'transition_point': 0.5,  # Default transition point for all scenarios
        'upstream_density': 0.4,  # Default upstream density
        'downstream_density': 0.3,  # Default downstream density
        'buffer_length': 2.0      # Default buffer length
    }
    
    # Run simulation
    start_time = time.time()
    results = scenario.run(params)
    end_time = time.time()
    
    print(f"Simulation completed in {end_time - start_time:.2f} seconds.")
    
    # Generate fundamental diagram if requested
    if args.plot in ["all", "interactive"]:
        fd_plotter = FundamentalDiagramPlotter(args.model, args.output)
        fd_plotter.plot_fundamental_diagrams(model, show=(args.plot == "interactive"))
    
    # Visualize results
    visualize_results(results, args)
    
    print(f"Results saved to {os.path.abspath(args.output)}")


if __name__ == "__main__":
    main()
