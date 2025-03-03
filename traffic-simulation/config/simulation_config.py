"""
Simulation Configuration

This module provides configuration settings and defaults for the traffic simulation.
It includes parameters for different vehicle classes, road types, and simulation scenarios.
"""

# Standard vehicle class parameters
VEHICLE_CLASSES = {
    "motorcycle": {
        "name": "moto",
        "v_max": 90.0,         # km/h
        "rho_max": 200.0,      # veh/km (motorcycles can pack more densely)
        "eta": 0.3,            # Gap-filling parameter
        "lambda_min": 0.8      # Minimum road quality effect (motorcycles less affected)
    },
    "car": {
        "name": "car",
        "v_max": 100.0,        # km/h
        "rho_max": 180.0,      # veh/km
        "beta": 0.3,           # Sensitivity to motorcycle interweaving
        "lambda_min": 0.6      # Road quality effect
    },
    "taxi": {
        "name": "taxi",
        "v_max": 95.0,         # km/h
        "rho_max": 180.0,      # veh/km
        "beta": 0.4,           # Higher sensitivity (more cautious)
        "lambda_min": 0.65     # Road quality effect
    },
    "bus": {
        "name": "bus",
        "v_max": 85.0,         # km/h
        "rho_max": 140.0,      # veh/km (larger vehicles)
        "beta": 0.5,           # High sensitivity to motorcycles
        "lambda_min": 0.55     # Strongly affected by road quality
    },
    "truck": {
        "name": "truck",
        "v_max": 80.0,         # km/h
        "rho_max": 120.0,      # veh/km (largest vehicles)
        "beta": 0.6,           # Very sensitive to motorcycles
        "lambda_min": 0.5      # Most affected by road quality
    }
}

# Road type parameters
ROAD_TYPES = {
    "bitumen_good": {
        "base_quality": 1.0,
        "description": "Good quality asphalt"
    },
    "bitumen_poor": {
        "base_quality": 0.8,
        "description": "Deteriorated asphalt with potholes"
    },
    "paved": {
        "base_quality": 0.9,
        "description": "Paved road (cobblestone or concrete blocks)"
    },
    "gravel": {
        "base_quality": 0.7,
        "description": "Gravel or crushed stone surface"
    },
    "dirt": {
        "base_quality": 0.5,
        "description": "Dirt or earth road"
    },
    "damaged": {
        "base_quality": 0.4,
        "description": "Severely damaged road with major potholes"
    }
}

# Default simulation parameters
DEFAULT_SIMULATION_PARAMS = {
    # Spatial and temporal discretization
    "domain_length": 20.0,     # km
    "simulation_time": 1.0,    # hours
    "dx": 0.1,                 # km
    "cfl_factor": 0.9,         # CFL safety factor
    
    # Scenario parameters
    "default_scenarios": {
        "rarefaction": {
            "upstream_density": 0.7,    # Ratio of maximum density
            "downstream_density": 0.1,  # Ratio of maximum density
            "transition_point": 0.5     # Position as ratio of domain length
        },
        "red_light": {
            "light_position": 3.0,      # km
            "background_density": 0.2,  # Ratio
            "jam_density": 0.9,         # Ratio
            "jam_length": 0.5,          # km
            "green_time": 0.05          # hours
        },
        "degraded_road": {
            "density": 0.3,             # Ratio
            "degraded_start": 3.0,      # km
            "degraded_end": 7.0,        # km
            "quality_good": 1.0,        # Quality coefficient for good sections
            "quality_bad": 0.6          # Quality coefficient for bad sections
        }
    },
    
    # Output settings
    "output_dir": "simulations",
    "save_interval": 0.05,     # hours
    
    # Feature flags for specialized behaviors
    "enable_gap_filling": True,
    "enable_road_quality_effects": True
}

# Basic benin locations with their characteristics
BENIN_LOCATIONS = {
    "cotonou_center": {
        "description": "Downtown Cotonou with heavy mixed traffic",
        "moto_proportion": 0.75,
        "road_type": "bitumen_good",
        "typical_density": 0.6  # Ratio of max density
    },
    "calavi_godomey": {
        "description": "Suburban area with mixed road quality",
        "moto_proportion": 0.7,
        "road_type": "bitumen_poor",
        "typical_density": 0.5
    },
    "cotonou_port": {
        "description": "Port area with high truck percentage",
        "moto_proportion": 0.5,
        "road_type": "bitumen_good",
        "typical_density": 0.7,
        "truck_proportion": 0.3
    },
    "rural_road": {
        "description": "Rural road between towns",
        "moto_proportion": 0.55,
        "road_type": "dirt",
        "typical_density": 0.3
    },
    "ouidah_road": {
        "description": "Intercity road with varying quality",
        "moto_proportion": 0.6,
        "road_type": "bitumen_poor",
        "typical_density": 0.4,
        "sections": [
            {"position": 0, "length": 5, "road_type": "bitumen_good"},
            {"position": 5, "length": 10, "road_type": "bitumen_poor"},
            {"position": 15, "length": 5, "road_type": "gravel"}
        ]
    }
}

# Traffic signal parameters
TRAFFIC_SIGNALS = {
    "standard": {
        "cycle_time": 120,     # seconds
        "green_time": 60,      # seconds
        "yellow_time": 5,      # seconds
        "moto_anticipation": 2.5,  # seconds (motorcycles tend to start earlier)
        "clearing_time": 3.0   # seconds (time to clear intersection after red)
    },
    "peak_hour": {
        "cycle_time": 180,
        "green_time": 90,
        "yellow_time": 5,
        "moto_anticipation": 3.0,
        "clearing_time": 3.5
    },
    "off_peak": {
        "cycle_time": 90,
        "green_time": 45,
        "yellow_time": 5,
        "moto_anticipation": 2.0,
        "clearing_time": 2.5
    }
}

# Visualization settings
VISUALIZATION_SETTINGS = {
    "default_colormap": "viridis",
    "class_colors": {
        "moto": "#ff7f0e",     # orange
        "car": "#1f77b4",      # blue
        "taxi": "#2ca02c",     # green
        "bus": "#d62728",      # red
        "truck": "#9467bd"     # purple
    },
    "road_type_styles": {
        "bitumen_good": {"color": "black", "linestyle": "-", "linewidth": 2.0},
        "bitumen_poor": {"color": "dimgray", "linestyle": "-", "linewidth": 1.5},
        "paved": {"color": "darkgray", "linestyle": "-.", "linewidth": 1.5},
        "gravel": {"color": "brown", "linestyle": "--", "linewidth": 1.5},
        "dirt": {"color": "sandybrown", "linestyle": ":", "linewidth": 1.0},
        "damaged": {"color": "red", "linestyle": "-", "linewidth": 1.0}
    },
    "figure_size": (12, 8),
    "dpi": 300,
    "animation_fps": 10
}

# Calibration targets for Benin traffic
CALIBRATION_TARGETS = {
    "gap_filling_parameter": {
        "min": 0.2,
        "max": 0.5,
        "default": 0.3,
        "description": "Gap-filling capability of motorcycles"
    },
    "interweaving_sensitivity": {
        "min": 0.1,
        "max": 0.6,
        "default": {
            "car": 0.3,
            "taxi": 0.4,
            "bus": 0.5,
            "truck": 0.6
        },
        "description": "Sensitivity of vehicles to motorcycle interweaving"
    },
    "road_quality_sensitivity": {
        "min": 0.4,
        "max": 0.9,
        "default": {
            "moto": 0.8,
            "car": 0.6,
            "taxi": 0.65,
            "bus": 0.55,
            "truck": 0.5
        },
        "description": "How much road quality affects different vehicle classes"
    },
    "maximum_flow_ranges": {
        "bitumen_good": {
            "moto": [600, 800],  # vehicles/hour
            "car": [1800, 2200],
            "mixed": [2400, 2800]
        },
        "bitumen_poor": {
            "moto": [500, 700],
            "car": [1400, 1800],
            "mixed": [2000, 2400]
        }
    },
    "moto_proportion_effect": {
        "0.00": 1.00,  # Baseline (no motorcycles)
        "0.25": 1.08,  # 8% capacity increase
        "0.50": 1.18,  # 18% capacity increase
        "0.75": 1.25,  # 25% capacity increase
        "0.90": 1.30   # 30% capacity increase
    }
}