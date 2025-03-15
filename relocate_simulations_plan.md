# Plan to Relocate Simulation Outputs

This document outlines the plan to move the simulation output directory and update file paths.

## Problem

The simulation outputs are currently being saved in `traffic-simulation/simulations` instead of the project root (`d:/Projets/Alibi/Projet_tutore`). This needs to be corrected so that the LaTeX document (`memoire.tex`) can correctly reference the simulation results.

## Plan

1.  **Move the `simulations` directory:** Move `traffic-simulation/simulations` to the project root (`d:/Projets/Alibi/Projet_tutore`).
2.  **Update file paths in `main.py`:** Search for `"simulations"` in `traffic-simulation/main.py` and remove `traffic-simulation/` from any paths.
3.  **Update file paths in `run_all_simulations.py`:** Search for `"simulations"` in `traffic-simulation/run_all_simulations.py` and remove `traffic-simulation/` from any paths.
4.  **Update `memoire.tex`:** Check `memoire.tex` and update the `\graphicspath` if necessary.
5.  **Check other files (optional):** Search for `traffic-simulation/simulations` in the project and correct any other files if needed.
6. **Confirm and Switch Mode:** After completing these steps, confirm with the user and request to switch to code mode.

## Mermaid Diagram

```mermaid
graph LR
    A[User Request: Move simulation outputs] --> B(Read main.py);
    B --> C(Read run_all_simulations.py);
    C --> D(Read simulation_run.log);
    D --> E{Confirm output path};
    E -- Yes --> F[Move simulations directory];
    E -- No --> F;
    F --> G[Update paths in main.py];
    G --> H[Update paths in run_all_simulations.py];
    H --> I[Check/Update paths in memoire.tex];
    I --> J[Check other files (optional)];
    J --> K[Confirm with user];
    K --> L[Switch to Code Mode];