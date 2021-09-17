import numpy as np

from bokeh.io import show
from bokeh.plotting import figure

p = figure(plot_width=1600, plot_height=1600)

HI_POLE_COUNTS = 2
POLE_PAIR_PRECISION = 4096

counts_per_rad = (HI_POLE_COUNTS * POLE_PAIR_PRECISION) / (2*np.pi)

def rads_to_counts(rad):
    return (rad * counts_per_rad) % POLE_PAIR_PRECISION

x = np.linspace(0, 2*np.pi, endpoint=True, num=HI_POLE_COUNTS * POLE_PAIR_PRECISION)
y = [rads_to_counts(j) for j in x]

p.line(x, y, line_width=2)

show(p)
