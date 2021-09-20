from typing import ValuesView
from bokeh.io.doc import curdoc
from bokeh.models.glyphs import Circle, MultiLine, Scatter
import numpy as np

from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Line
from bokeh.plotting import figure
from bokeh.io import curdoc

from vernier_constants import POLE_PAIR_PRECISION, TAU, NUM_STEPS, POSITIONS, VERTICAL_LINE_Y_COORDS
from vernier_calculations import get_position_index, calculate_vernier_helper, calculate_ring_counts

##############################################################################
#Starting values
##############################################################################
HI_POLE_COUNTS = 3
LO_POLE_COUNTS = 2

y0 = calculate_ring_counts(HI_POLE_COUNTS)
y1 = calculate_ring_counts(LO_POLE_COUNTS)

deltas = [calculate_vernier_helper(HI_POLE_COUNTS, LO_POLE_COUNTS, m, n)
    for m, n in zip(y0, y1)]

##############################################################################
#Data Sources
##############################################################################
ring_counts_source = ColumnDataSource(
    dict(
        x=POSITIONS,
        y0=y0,
        y1=y1,
        deltas=deltas
    )
)

position_source = ColumnDataSource(
    dict(
        x=[0, 0],
        y=VERTICAL_LINE_Y_COORDS
    )
)

circle_positions_source = ColumnDataSource(
    dict(
        m = [0],
        n = [0],
        delta = [0],
        sizes = [8]
    )
)

##############################################################################
#Plots
##############################################################################
lo_counts_glyph = Line(x="x", y="y0", line_color="red", line_width=2)
hi_counts_glyph = Line(x="x", y="y1", line_color="blue", line_width=2)
line_glyph = Line(x="x", y="y", line_color="black", line_width=2)
counts_vs_rads_plot = figure(plot_width=800, plot_height=800)
counts_vs_rads_plot.add_glyph(ring_counts_source, lo_counts_glyph)
counts_vs_rads_plot.add_glyph(ring_counts_source, hi_counts_glyph)
counts_vs_rads_plot.add_glyph(position_source, line_glyph)

circle_glyph = Circle(x='m', y='n', size='sizes', fill_color='red')
scatter_glyph = Scatter(x='y0', y='y1', marker='dash')
m_vs_n_plot = figure(plot_width=800, plot_height=800)
m_vs_n_plot.add_glyph(ring_counts_source, scatter_glyph)
m_vs_n_plot.add_glyph(circle_positions_source ,circle_glyph)

circle_glyph = Circle(x='m', y='delta', size='sizes', fill_color='red')
scatter_glyph = Scatter(x='y0', y='deltas',marker='dash')
vernier_helper_plot = figure(plot_width=800, plot_height=800)
vernier_helper_plot.add_glyph(ring_counts_source, scatter_glyph)
vernier_helper_plot.add_glyph(circle_positions_source ,circle_glyph)

##############################################################################
#Sliders and Callbacks
##############################################################################
def update_position(attrname, old, new):
    pos = angle_slider.value
    x = [pos, pos]
    y = VERTICAL_LINE_Y_COORDS
    position_source.data = dict(x=x, y=y)

    idx = get_position_index(pos)
    m = ring_counts_source.data['y0'][idx]
    n = ring_counts_source.data['y1'][idx]
    delta = calculate_vernier_helper(
        hi_slider.value,
        lo_slider.value,
        m,
        n
    )
    circle_positions_source.data = dict(m=[m], n=[n], delta=[delta], sizes=[8])

def update_counts(attrname, old, new):
    y0 = calculate_ring_counts(hi_slider.value)
    y1 = calculate_ring_counts(lo_slider.value)
    deltas = [calculate_vernier_helper(hi_slider.value, lo_slider.value, m, n)
              for m, n in zip(y0, y1)]
    ring_counts_source.data = dict(x=POSITIONS, y0=y0, y1=y1, deltas=deltas)


lo_slider = Slider(start=1, end=41, value=2, step=1, title="lo pole pairs")
hi_slider = Slider(start=1, end=41, value=3, step=1, title="hi pole pairs")
angle_slider = Slider(start=0, end=2*np.pi, value=0, step=2*np.pi/1000.0, title="Position (rad)")

lo_slider.on_change('value', update_counts)
hi_slider.on_change('value', update_counts)
angle_slider.on_change('value', update_position)

##############################################################################
#Layout
##############################################################################
layout = column(
    column(lo_slider, hi_slider, angle_slider),
    row(counts_vs_rads_plot, m_vs_n_plot,vernier_helper_plot)
)

curdoc().add_root(layout)
