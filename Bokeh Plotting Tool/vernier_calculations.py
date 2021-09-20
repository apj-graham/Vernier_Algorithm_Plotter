import numpy as np
from vernier_constants import POLE_PAIR_PRECISION, TAU, NUM_STEPS, POSITIONS

def get_position_index(current_position):
    delta = TAU / (NUM_STEPS * 2)
    for idx, val in enumerate(POSITIONS):
        if abs(val - current_position) < delta:
            return idx
    raise ValueError(f"{current_position} not in plotted angles")

def get_counts_per_rad(pole_counts):
    return (pole_counts * POLE_PAIR_PRECISION) / (2*np.pi)

def rads_to_counts(rad, counts_per_rad):
    return (rad * counts_per_rad) % POLE_PAIR_PRECISION

def calculate_ring_counts(pole_pairs):
    counts_per_rad = get_counts_per_rad(pole_pairs)
    return [rads_to_counts(j, counts_per_rad) for j in POSITIONS]

def calculate_vernier_helper(hi_pole_pairs, lo_pole_pairs, hi_reading, lo_reading):
    return (lo_pole_pairs * hi_reading) - (hi_pole_pairs * lo_reading)