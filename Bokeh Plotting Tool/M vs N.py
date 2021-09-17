import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, ColumnDataSource, Slider, MultiLine
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.palettes import Spectral11


HI_POLE_COUNTS = 3
LO_POLE_COUNTS = 2
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


source = ColumnDataSource(
    dict(
        x=x,
        y0=y0,
        y1=y1
    )
)


plot = figure(plot_width=800, plot_height=800)
plot.scatter('y0', 'y1', source=source)
plot.circle([0], [0], size=8, color='red')
show(plot)