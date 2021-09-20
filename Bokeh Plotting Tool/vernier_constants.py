import numpy as np


POLE_PAIR_PRECISION = 4096

NUM_STEPS = 2500

CIRCLE_SIZES = [8]

TAU = 2 * np.pi

POSITIONS = list(np.linspace(0, 2*np.pi, endpoint=True, num=NUM_STEPS))

VERTICAL_LINE_Y_COORDS = [0, POLE_PAIR_PRECISION]