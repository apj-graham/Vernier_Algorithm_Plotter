from typing import ValuesView
from bokeh.io.doc import curdoc
from bokeh.models.glyphs import Circle, Scatter
import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Line
from bokeh.plotting import figure
from bokeh.io import curdoc


POLE_PAIR_PRECISION = 4096
NUM_STEPS = 1000
angles = list(np.linspace(0, 2*np.pi, endpoint=True, num=NUM_STEPS))
y = list(np.linspace(0, 2*np.pi, endpoint=True, num=NUM_STEPS))

HI_POLE_COUNTS = 3
LO_POLE_COUNTS = 2

def get_position_index(position):
    delta = (2 * np.pi)/(1000.0 * 2)
    for idx, val in enumerate(angles):
        if abs(val - position) < delta:
            return idx
    raise ValueError(f"{position} not in plotted angles")

def get_counts_per_rad(pole_counts):
    return (pole_counts * POLE_PAIR_PRECISION) / (2*np.pi)

def rads_to_counts(rad, counts_per_rad):
    return (rad * counts_per_rad) % POLE_PAIR_PRECISION

def calculate_ring_counts(pole_pairs):
    counts_per_rad = get_counts_per_rad(pole_pairs)
    return [rads_to_counts(j, counts_per_rad) for j in angles]

ring_counts_source = ColumnDataSource(
    dict(
        x=angles,
        y0=y,
        y1=y
    )
)

position_source = ColumnDataSource(
    dict(
        x=[0, 0],
        y=[0, 4096]
    )
)

diff_source = ColumnDataSource(
    dict(
        x = [0],
        y = [0],
        sizes = [8]
    )
)


lo_counts_glyph = Line(x="x", y="y0", line_color="red", line_width=2)
hi_counts_glyph = Line(x="x", y="y1", line_color="blue", line_width=2)
angle_glyph = Line(x="x", y="y", line_color="black", line_width=2)

counts_vs_rads_plot = figure(plot_width=800, plot_height=800)
counts_vs_rads_plot.add_glyph(ring_counts_source, lo_counts_glyph)
counts_vs_rads_plot.add_glyph(ring_counts_source, hi_counts_glyph)
counts_vs_rads_plot.add_glyph(position_source, angle_glyph)

circle_glyph = Circle(x='x', y='y', size='sizes', fill_color='red')
scatter_glyph = Scatter(x='y0', y='y1')

m_vs_n_plot = figure(plot_width=800, plot_height=800)
m_vs_n_plot.add_glyph(ring_counts_source, scatter_glyph)
m_vs_n_plot.add_glyph(diff_source ,circle_glyph)

lo_slider = Slider(start=1, end=41, value=2, step=1, title="lo pole pairs")
hi_slider = Slider(start=1, end=41, value=3, step=1, title="hi pole pairs")
angle_slider = Slider(start=0, end=2*np.pi, value=0, step=2*np.pi/1000.0, title="Position (rad)")


def update_position(attrname, old, new):
    pos = angle_slider.value
    x = [pos, pos]
    y = [0, POLE_PAIR_PRECISION]
    position_source.data = dict(x=x, y=y)

    idx = get_position_index(pos)
    m = ring_counts_source.data['y0'][idx]
    n = ring_counts_source.data['y1'][idx]
    diff_source.data = dict(x=[m], y=[n], sizes=[8])

def update_counts(attrname, old, new):
    y0 = calculate_ring_counts(lo_slider.value)
    y1 = calculate_ring_counts(hi_slider.value)

    ring_counts_source.data = dict(x=angles, y0=y0, y1=y1)


lo_slider.on_change('value', update_counts)
hi_slider.on_change('value', update_counts)
angle_slider.on_change('value', update_position)


layout = column(
    lo_slider,
    hi_slider,
    angle_slider,
    row(counts_vs_rads_plot,
        m_vs_n_plot
    )
)

curdoc().add_root(layout)
