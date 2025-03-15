# Traffic Simulation Model

This project implements a traffic simulation model using the Lighthill-Whitham-Richards (LWR) framework. It includes various scenarios to demonstrate different traffic conditions and behaviors, along with visualization tools to analyze the results.

## Project Structure

```
traffic-simulation
├── src
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── lwr_model.py
│   │   └── fundamental_diagram.py
│   ├── visualization
│   │   ├── __init__.py
│   │   ├── animator.py
│   │   ├── plotter.py
│   │   ├── simulation_plotter.py
│   │   ├── multiclass_plotter.py
│   │   └── motorcycle_impact_visualizer.py
│   └── utils
│       ├── __init__.py
│       └── numerical_methods.py
├── scenarios
│   ├── __init__.py
│   ├── red_light.py
│   ├── shock_wave.py
│   ├── rarefaction_wave.py
│   └── traffic_jam.py
├── tests
│   ├── __init__.py
│   ├── test_lwr_model.py
│   └── test_visualization.py
├── notebooks
│   └── examples.ipynb
├── main.py
├── requirements.txt
└── README.md
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd traffic-simulation
pip install -r requirements.txt
```

## Usage

To run the traffic simulation, execute the `main.py` file. This file orchestrates the model and scenarios.

```bash
python main.py
```

## Scenarios

The project includes several scenarios to demonstrate different traffic conditions:

- **Red Light Scenario**: Simulates traffic stopping and starting at a traffic light.
- **Shock Wave Scenario**: Models the propagation of a shock wave in traffic.
- **Rarefaction Wave Scenario**: Simulates the transition from high to low density traffic.
- **Traffic Jam Scenario**: Demonstrates congestion and its effects on traffic flow.

## Visualization

The project provides a comprehensive set of visualization tools to analyze traffic simulations:

### Basic Traffic Visualization

The `SimulationPlotter` class provides:
- Density, velocity, and flow evolution over time and space
- Combined visualizations showing all three parameters in one figure
- Space profiles at selected time points
- Interactive animations of traffic evolution

### Multiclass Traffic Visualization

The `MulticlassPlotter` extends the basic visualizations to handle multiple vehicle classes:
- Class comparisons showing density, velocity, and flow for each vehicle type
- Flow-density relationships for each class
- Class proportion analysis across space and time
- Comprehensive traffic analysis dashboards

### Specialized Motorcycle Impact Visualizations

The `MotorcycleImpactVisualizer` provides specialized tools for analyzing motorcycle-specific phenomena:
- Gap-filling effect visualization showing how motorcycles utilize spaces between cars
- Road surface impact analysis showing how different vehicle classes respond to road quality variations
- Interweaving effect visualization demonstrating how motorcycles affect other vehicle classes

Example usage:

```python
from src.visualization import SimulationPlotter, MulticlassPlotter, MotorcycleImpactVisualizer

# Basic visualization
plotter = SimulationPlotter(model_name="LWR", output_dir="outputs/basic")
plotter.plot_combined_evolution(density, velocity, flow, x_grid, t_grid)

# Multiclass visualization
mc_plotter = MulticlassPlotter(model_name="Multiclass LWR", output_dir="outputs/multiclass")
mc_plotter.create_dashboard(results, x_grid, t_grid)

# Motorcycle-specific visualization
moto_viz = MotorcycleImpactVisualizer(output_dir="outputs/motorcycle_analysis")
moto_viz.visualize_gap_filling_effect(densities, velocities, x_grid, t_grid, gamma_values=[0.2, 0.4, 0.6])
moto_viz.visualize_road_surface_impact(densities, velocities, lambda_values, x_grid, t_grid)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.