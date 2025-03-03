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
│   │   └── plotter.py
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

The project provides visualization tools to plot and animate the results of the traffic simulations. You can visualize density, speed, and flow over time using the provided plotting and animation functionalities.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.