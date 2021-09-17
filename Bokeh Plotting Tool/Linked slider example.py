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
        xs=[x, x],
        ys=[y0, y1],
    )
)

mypalette=Spectral11[0:2]

plot = figure(plot_width=800, plot_height=800)

plot.multi_line(
    "xs",
    "ys",
    line_color=mypalette,
    line_width=2,
    source=source
)

lo_slider = Slider(start=1, end=41, value=2, step=1, title="lo pole pairs")
hi_slider = Slider(start=1, end=41, value=3, step=1, title="hi pole pairs")

update_lo_counts = CustomJS(args=dict(source=source, slider=lo_slider), code="""
    var precision = 4096;
    var data = source.data;
    var f = slider.value;
    var x = data['xs'][0];
    var y = data['ys'][0];
    var counts_per_rads = (f * precision) / (2 * Math.PI);
    // for (var i = 0; i < x.length; i++) {
    //     y[i] = (x[i] * counts_per_rad) % precision
    // }

    for (var i = 0; i < x.length; i++) {
        y[i] = counts_per_rads * x[i] % precision
    }

    // necessary becasue we mutated source.data in-place
    source.change.emit();
""")

update_hi_counts = CustomJS(args=dict(source=source, slider=hi_slider), code="""
    var precision = 4096;
    var data = source.data;
    var f = slider.value;
    var x = data['xs'][1];
    var y = data['ys'][1];
    var counts_per_rads = (f * precision) / (2 * Math.PI);
    // for (var i = 0; i < x.length; i++) {
    //     y[i] = (x[i] * counts_per_rad) % precision
    // }

    for (var i = 0; i < x.length; i++) {
        y[i] = counts_per_rads * x[i] % precision
    }

    // necessary becasue we mutated source.data in-place
    source.change.emit();
""")

lo_slider.js_on_change('value', update_lo_counts)
hi_slider.js_on_change('value', update_hi_counts)


layout = row(
    plot,
    column(lo_slider, hi_slider)
)

show(layout)
