import numpy as np

from bokeh.layouts import gridplot
from bokeh.io import show
from bokeh.plotting import figure

HI_POLE_COUNTS = 41
LO_POLE_COUNTS = 33
POLE_PAIR_PRECISION = 4096

def get_counts_per_rad(pole_counts):
    return (pole_counts * POLE_PAIR_PRECISION) / (2*np.pi)

def rads_to_counts(rad, counts_per_rad):
    return (rad * counts_per_rad) % POLE_PAIR_PRECISION


x = np.linspace(0, 2*np.pi, endpoint=True, num=HI_POLE_COUNTS * POLE_PAIR_PRECISION)

# For Hi ring
counts_per_rad = get_counts_per_rad(HI_POLE_COUNTS)
y0 = [rads_to_counts(j, counts_per_rad) for j in x]

# For lo ring
counts_per_rad = get_counts_per_rad(LO_POLE_COUNTS)
y1 = [rads_to_counts(j, counts_per_rad) for j in x]

plot_options = dict(width=250, plot_height=250, tools='pan, wheel_zoom')

s1 = figure(**plot_options)
s1.line(x, y0, line_width=2)

s2 = figure(x_range=s1.x_range, y_range=s1.y_range, **plot_options)
s2.line(x, y0, line_width=2)

p = gridplot([[s1, s2]])

show(p)
