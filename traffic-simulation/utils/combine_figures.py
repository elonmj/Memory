"""
Combine Figures Utility

This module provides functions to combine multiple figures from different simulations
into comparison panels or summary dashboards.
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from PIL import Image


def find_similar_figures(base_dir, pattern, models=None, scenarios=None):
    """
    Find similar figures across different model and scenario directories.
    
    Args:
        base_dir: Base directory to search
        pattern: Figure filename pattern to search for (e.g., "*_density.png")
        models: List of models to include (if None, include all)
        scenarios: List of scenarios to include (if None, include all)
        
    Returns:
        dict: Dictionary mapping {model: {scenario: filepath}}
    """
    result = {}
    
    # If models/scenarios not specified, detect them from directory structure
    if models is None:
        models = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for model in models:
        model_dir = os.path.join(base_dir, model)
        if not os.path.isdir(model_dir):
            continue
            
        result[model] = {}
        
        if scenarios is None:
            model_scenarios = [d for d in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, d))]
        else:
            model_scenarios = scenarios
        
        for scenario in model_scenarios:
            scenario_dir = os.path.join(model_dir, scenario)
            if not os.path.isdir(scenario_dir):
                continue
                
            # Find matching files
            matches = glob.glob(os.path.join(scenario_dir, pattern))
            if matches:
                result[model][scenario] = matches[0]  # Take the first match
    
    return result


def combine_figures(file_dict, output_path=None, title=None, figsize=(15, 10)):
    """
    Combine figures from different models and scenarios into a grid layout.
    
    Args:
        file_dict: Dictionary mapping {model: {scenario: filepath}}
        output_path: Path to save the combined figure (if None, display only)
        title: Main title for the combined figure
        figsize: Size of the output figure
        
    Returns:
        matplotlib.figure.Figure: The combined figure
    """
    # Count models and scenarios
    models = list(file_dict.keys())
    all_scenarios = set()
    for model_scenarios in file_dict.values():
        all_scenarios.update(model_scenarios.keys())
    scenarios = sorted(all_scenarios)
    
    n_models = len(models)
    n_scenarios = len(scenarios)
    
    if n_models == 0 or n_scenarios == 0:
        raise ValueError("No figures found to combine")
    
    # Create figure with grid
    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(n_models, n_scenarios)
    
    # Add title if provided
    if title:
        fig.suptitle(title, fontsize=16)
    
    # Plot each figure in the grid
    for i, model in enumerate(models):
        for j, scenario in enumerate(scenarios):
            if scenario in file_dict[model]:
                # Create subplot
                ax = fig.add_subplot(gs[i, j])
                
                # Load and display image
                img_path = file_dict[model][scenario]
                img = plt.imread(img_path)
                ax.imshow(img)
                
                # Set labels
                if i == 0:
                    ax.set_title(scenario.capitalize())
                if j == 0:
                    ax.set_ylabel(model)
                
                # Remove ticks
                ax.set_xticks([])
                ax.set_yticks([])
    
    plt.tight_layout()
    
    # Save if output path provided
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"Combined figure saved to: {output_path}")
    
    return fig


def create_comparative_dashboard(simulation_dir, output_dir=None, models=None, scenarios=None):
    """
    Create comparative dashboards across models and scenarios.
    
    Args:
        simulation_dir: Base directory containing simulation results
        output_dir: Directory to save comparison figures (default: simulation_dir/comparisons)
        models: List of models to include (if None, include all)
        scenarios: List of scenarios to include (if None, include all)
        
    Returns:
        list: Paths to created dashboard images
    """
    if output_dir is None:
        output_dir = os.path.join(simulation_dir, "comparisons")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Find and combine density evolution figures
    density_figures = find_similar_figures(
        simulation_dir, "*_density_evolution.png", models, scenarios)
    
    density_comparison = combine_figures(
        density_figures, 
        os.path.join(output_dir, "density_comparison.png"),
        "Density Evolution Comparison"
    )
    
    # Find and combine velocity evolution figures
    velocity_figures = find_similar_figures(
        simulation_dir, "*_velocity_evolution.png", models, scenarios)
    
    velocity_comparison = combine_figures(
        velocity_figures, 
        os.path.join(output_dir, "velocity_comparison.png"),
        "Velocity Evolution Comparison"
    )
    
    # Find and combine flow evolution figures
    flow_figures = find_similar_figures(
        simulation_dir, "*_flow_evolution.png", models, scenarios)
    
    flow_comparison = combine_figures(
        flow_figures, 
        os.path.join(output_dir, "flow_comparison.png"),
        "Flow Evolution Comparison"
    )
    
    # Create combined dashboard if requested
    combined_dashboard_path = os.path.join(output_dir, "combined_dashboard.png")
    
    fig = plt.figure(figsize=(18, 15))
    gs = gridspec.GridSpec(3, 1)
    
    # Add the three comparison images to the dashboard
    for i, (title, path) in enumerate([
        ("Density Comparison", os.path.join(output_dir, "density_comparison.png")),
        ("Velocity Comparison", os.path.join(output_dir, "velocity_comparison.png")),
        ("Flow Comparison", os.path.join(output_dir, "flow_comparison.png"))
    ]):
        ax = fig.add_subplot(gs[i, 0])
        if os.path.exists(path):
            img = plt.imread(path)
            ax.imshow(img)
        else:
            ax.text(0.5, 0.5, f"{title} not available", ha="center", va="center")
        
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    
    plt.tight_layout()
    plt.savefig(combined_dashboard_path, dpi=300, bbox_inches="tight")
    
    return [
        os.path.join(output_dir, "density_comparison.png"),
        os.path.join(output_dir, "velocity_comparison.png"),
        os.path.join(output_dir, "flow_comparison.png"),
        combined_dashboard_path
    ]


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Combine simulation figures into comparison dashboards")
    parser.add_argument("--input-dir", type=str, default="simulations", 
                        help="Base directory containing simulation results")
    parser.add_argument("--output-dir", type=str, default=None, 
                        help="Directory to save comparison figures")
    parser.add_argument("--models", type=str, nargs="+", default=None, 
                        help="Models to include")
    parser.add_argument("--scenarios", type=str, nargs="+", default=None, 
                        help="Scenarios to include")
    
    args = parser.parse_args()
    
    print("Creating comparative dashboards...")
    result_paths = create_comparative_dashboard(
        args.input_dir, args.output_dir, args.models, args.scenarios)
    
    print("Generated comparative dashboards:")
    for path in result_paths:
        print(f"- {path}")
