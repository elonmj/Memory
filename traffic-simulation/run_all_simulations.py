"""
Run All Simulations Script

This script runs all combinations of models and scenarios, handling errors gracefully
and ensuring all possible visualizations are generated and saved.
"""

import os
import sys
import time
import datetime
import subprocess
import argparse
import logging
from itertools import product
from pathlib import Path

# Set up paths
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
main_script = current_dir / "main.py"

# Configure logging
# Configure logging with project root-based path
log_file_path = os.path.join(str(project_root), 'simulation_run.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file_path)
    ]
)
logger = logging.getLogger(__name__)

# Available models and scenarios from main.py
MODELS = ["lwr", "multiclass"]
SCENARIOS = ["rarefaction", "shock", "redlight", "degraded", "gapfilling", "trafficjam"]

# Default parameter values that can be overridden
DEFAULT_PARAMS = {
    "domain": 20.0,
    "time": 1.0,
    "dx": 0.1,
    "cfl": 0.9,
    "vmax": 100.0,
    "rhomax": 180.0,
    "classes": 2,
    "eta": 0.3,
    "output": "simulations"
}


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run all traffic simulation combinations")
    
    parser.add_argument("--models", type=str, nargs="+", choices=MODELS, default=MODELS,
                        help="Models to run (default: all)")
    parser.add_argument("--scenarios", type=str, nargs="+", choices=SCENARIOS, default=SCENARIOS,
                        help="Scenarios to run (default: all)")
    
    # Add all parameters from main.py that can be overridden
    for param, default in DEFAULT_PARAMS.items():
        parser.add_argument(f"--{param}", type=type(default), default=default,
                            help=f"Override default value for {param} (default: {default})")
    
    parser.add_argument("--plot", type=str, choices=["none", "basic", "all"], default="all",
                        help="Plotting level (default: all)")
    parser.add_argument("--log-file", type=str, default="simulation_run.log",
                        help="Log file path")
    parser.add_argument("--sequential", action="store_true", 
                        help="Run simulations sequentially instead of by model group")
    
    return parser.parse_args()


def run_simulation(model, scenario, params):
    """
    Run a single simulation with given model and scenario.
    
    Args:
        model: Model type (e.g., "lwr")
        scenario: Scenario type (e.g., "rarefaction")
        params: Dictionary of parameters
        
    Returns:
        bool: True if simulation succeeded, False otherwise
    """
    cmd = [sys.executable, str(main_script), "--model", model, "--scenario", scenario]
    
    # Add all parameters
    for param, value in params.items():
        if param not in ["models", "scenarios", "log_file", "sequential"]:
            cmd.extend([f"--{param}", str(value)])
    
    # Create output directory using project root
    output_dir = os.path.join(str(project_root), params["output"], model.upper(), scenario)
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Running: {' '.join(cmd)} in {current_dir}")
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=current_dir)
        end_time = time.time()
        
        # Log output
        if result.stdout:
            for line in result.stdout.splitlines():
                logger.info(f"[{model}/{scenario}] {line}")
        
        logger.info(f"✓ {model}/{scenario} completed successfully in {end_time - start_time:.2f} seconds")
        return True
    
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        logger.error(f"✗ {model}/{scenario} failed in {end_time - start_time:.2f} seconds")
        
        # Log error output
        if e.stdout:
            for line in e.stdout.splitlines():
                logger.info(f"[{model}/{scenario}] {line}")
        
        if e.stderr:
            for line in e.stderr.splitlines():
                logger.error(f"[{model}/{scenario}] {line}")
        
        return False
    
    except Exception as e:
        end_time = time.time()
        logger.error(f"✗ {model}/{scenario} failed with unexpected error: {str(e)}")
        return False


def run_all_simulations(args):
    """
    Run all specified combinations of models and scenarios.
    
    Args:
        args: Command line arguments
        
    Returns:
        tuple: (total_count, success_count, failed_simulations)
    """
    # Convert args to dictionary of parameters
    params = vars(args)
    
    # Get list of models and scenarios to run
    models = args.models
    scenarios = args.scenarios
    
    # Count successful and failed runs
    total_count = len(models) * len(scenarios)
    success_count = 0
    failed_simulations = []
    
    # Start time for the entire batch
    batch_start_time = time.time()
    
    logger.info(f"Starting batch run of {total_count} simulations")
    logger.info(f"Models: {', '.join(models)}")
    logger.info(f"Scenarios: {', '.join(scenarios)}")
    
    if args.sequential:
        # Run all combinations sequentially
        for model, scenario in product(models, scenarios):
            if run_simulation(model, scenario, params):
                success_count += 1
            else:
                failed_simulations.append(f"{model}/{scenario}")
    else:
        # Run by model group (complete all scenarios for one model before moving to next)
        for model in models:
            logger.info(f"Running all scenarios for model: {model}")
            for scenario in scenarios:
                if run_simulation(model, scenario, params):
                    success_count += 1
                else:
                    failed_simulations.append(f"{model}/{scenario}")
    
    # Calculate total time
    total_time = time.time() - batch_start_time
    
    # Log summary
    logger.info("=" * 50)
    logger.info(f"Simulation Batch Completed")
    logger.info(f"Total runtime: {datetime.timedelta(seconds=int(total_time))}")
    logger.info(f"Success: {success_count}/{total_count} simulations")
    
    if failed_simulations:
        logger.warning(f"Failed simulations: {', '.join(failed_simulations)}")
    else:
        logger.info("All simulations completed successfully")
    
    return total_count, success_count, failed_simulations


def main():
    """Main entry point for the script."""
    args = parse_arguments()
    
    # Configure logging to file
    if args.log_file:
        log_file_path = os.path.join(str(project_root), args.log_file)
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                logger.removeHandler(handler)
        
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
    
    # Print header
    logger.info("=" * 50)
    logger.info("TRAFFIC SIMULATION BATCH RUN")
    logger.info("=" * 50)
    
    try:
        total_count, success_count, failed_simulations = run_all_simulations(args)
        
        # Print overall status at the end
        if success_count == total_count:
            logger.info("ALL SIMULATIONS COMPLETED SUCCESSFULLY")
            return 0
        else:
            logger.warning(f"{total_count - success_count} SIMULATIONS FAILED")
            return 1
    
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        return 130
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
