# Traffic Simulation - Log Figure Path

## Changes Required

### 1. traffic-simulation/src/visualization/simulation_plotter.py

*   **Action:** Add `filepath = f'{self.output_dir}/{filename}.png'` and `print(f"Figure saved as {os.path.abspath(filepath)}")` after the `plt.savefig()` call in the following functions:
    *   `plot_density_evolution`
    *   `plot_velocity_evolution`
    *   `plot_flow_evolution`
    *   `plot_combined_evolution`
    *   `plot_multiclass_comparison`
    *   `plot_flow_density_relationship`
    *   `create_multiclass_animation`
    *   `plot_spacetime_class_comparison`
    *   `create_dashboard`
    *   `visualize_gap_filling_effect`
    *   `visualize_road_surface_impact`
    *   `visualize_interweaving_effect`

### 2. traffic-simulation/run_all_simulations.py

*   **Action:** Modify the loop that processes `result.stdout` in the `run_simulation` function to check if a line starts with "Figure saved as". If it does, log the entire line.