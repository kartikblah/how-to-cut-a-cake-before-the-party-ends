# generate_valuations.py
import numpy as np
from valuations import PiecewiseLinearValuation

def generate_random_valuations(n_agents, k_pieces):
    """
    Generate `n_agents` piecewise linear valuations, each with `k_pieces` segments.
    Total area under each agent’s value density is normalized to 1.
    """
    agents = []
    for _ in range(n_agents):
        # Randomly split [0,1] into `k_pieces` intervals
        internal_points = np.random.uniform(0, 1, k_pieces - 1)
        breakpoints = np.sort(np.concatenate([[0], internal_points, [1]]))
        
        # Generate random value densities at breakpoints
        y_values = np.random.uniform(0, 2, size=k_pieces + 1)
        
        # Compute total area under the curve
        total_area = 0.0
        for i in range(len(breakpoints) - 1):
            x0 = breakpoints[i]
            x1 = breakpoints[i + 1]
            y0 = y_values[i]
            y1 = y_values[i + 1]
            segment_area = 0.5 * (y0 + y1) * (x1 - x0)
            total_area += segment_area
        
        # Normalize y_values to ensure total area = 1
        if total_area < 1e-9:  # Avoid division by zero
            normalized_y = np.ones_like(y_values)  # Fallback to uniform density
        else:
            normalized_y = y_values / total_area
        
        # Build segments with normalized values
        segments = []
        for i in range(len(breakpoints) - 1):
            x0 = breakpoints[i]
            x1 = breakpoints[i + 1]
            if x0 == x1:
                continue  # Skip zero-length intervals
            
            y0 = normalized_y[i]
            y1 = normalized_y[i + 1]
            slope = (y1 - y0) / (x1 - x0) if (x1 - x0) != 0 else 0
            intercept = y0 - slope * x0
            segments.append((x0, x1, slope, intercept))
        
        total_area = 0.0
        # print(len(segments))
        # for i in range(len(segments)): 
        #     x0 = segments[i][0]
        #     # print(i)
        #     x1 = segments[i][1]
        #     slope = segments[i][2]
        #     intercept = segments[i][3]
        #     segment_area = 0.5 * (slope * x0 + intercept + slope * x1 + intercept) * (x1 - x0)
        #     total_area += segment_area
        # print(f"Total area for agent {_ + 1}: {total_area}")

        agents.append(PiecewiseLinearValuation(segments))
    return agents