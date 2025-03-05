"""
Utility script to combine density, velocity, and flow figures into a single image
"""

import os
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.image as mpimg
from pathlib import Path

def combine_simulation_figures(model, scenario, output_dir=None):
    """
    Combine density, velocity, and flow evolution figures into one composite image
    
    Args:
        model: Model name (LWR, MULTICLASS)
        scenario: Scenario name (rarefaction, shock, redlight, etc.)
        output_dir: Output directory (default is the same as input)
    """
    # Base directory for simulations
    base_dir = Path("simulations") / model / scenario
    
    # Output directory
    if output_dir is None:
        output_dir = base_dir
    else:
        output_dir = Path(output_dir)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Find the scenario name from file naming pattern
    file_pattern = None
    for file in os.listdir(base_dir):
        if "_Density_Evolution.png" in file:
            file_pattern = file.replace("_Density_Evolution.png", "")
            break
    
    if file_pattern is None:
        print(f"No matching files found in {base_dir}")
        return False
    
    # Load the three images
    try:
        density_img = mpimg.imread(base_dir / f"{file_pattern}_Density_Evolution.png")
        velocity_img = mpimg.imread(base_dir / f"{file_pattern}_Velocity_Evolution.png")
        flow_img = mpimg.imread(base_dir / f"{file_pattern}_Flow_Evolution.png")
    except FileNotFoundError as e:
        print(f"Error loading images: {e}")
        return False
    
    # Create a combined figure
    fig = plt.figure(figsize=(12, 15))
    gs = GridSpec(3, 1, height_ratios=[1, 1, 1], hspace=0.3)
    
    # Add the three images
    ax1 = fig.add_subplot(gs[0])
    ax1.imshow(density_img)
    ax1.set_title("(a) Density Evolution", fontsize=14)
    ax1.axis('off')
    
    ax2 = fig.add_subplot(gs[1])
    ax2.imshow(velocity_img)
    ax2.set_title("(b) Velocity Evolution", fontsize=14)
    ax2.axis('off')
    
    ax3 = fig.add_subplot(gs[2])
    ax3.imshow(flow_img)
    ax3.set_title("(c) Flow Evolution", fontsize=14)
    ax3.axis('off')
    
    # Save combined figure
    output_file = output_dir / f"{file_pattern}_combined.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Combined figure saved to {output_file}")
    return True

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python combine_figures.py MODEL SCENARIO [OUTPUT_DIR]")
        return
    
    model = sys.argv[1]
    scenario = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = combine_simulation_figures(model, scenario, output_dir)
    if success:
        print("Successfully combined figures")
    else:
        print("Failed to combine figures")

if __name__ == "__main__":
    main()
