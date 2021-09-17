import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, ColumnDataSource, Slider, Line
from bokeh.plotting import figure
from bokeh.io import show


HI_POLE_COUNTS = 3
LO_POLE_COUNTS = 2
POLE_PAIR_PRECISION = 4096

NUM_STEPS = 1000

def get_counts_per_rad(pole_counts):
    return (pole_counts * POLE_PAIR_PRECISION) / (2*np.pi)

def rads_to_counts(rad, counts_per_rad):
    return (rad * counts_per_rad) % POLE_PAIR_PRECISION


x = np.linspace(0, 2*np.pi, endpoint=True, num=NUM_STEPS)
print(2*np.pi/1000)
print(x)


# For Hi ring
counts_per_rad_hi = get_counts_per_rad(HI_POLE_COUNTS)
y0 = [rads_to_counts(j, counts_per_rad_hi) for j in x]

# For lo ring
counts_per_rad_lo = get_counts_per_rad(LO_POLE_COUNTS)
y1 = [rads_to_counts(j, counts_per_rad_lo) for j in x]

source = ColumnDataSource(
    dict(
        x=x,
        y0=y0,
        y1=y1
    )
)

source2 = ColumnDataSource(
    dict(
        x=[0, 0],
        y=[0, 4096]
    )
)


lo_counts_glyph = Line(x="x", y="y0", line_color="red", line_width=2)
hi_counts_glyph = Line(x="x", y="y1", line_color="blue", line_width=2)
angle_glyph = Line(x="x", y="y", line_color="black", line_width=2)

counts_vs_rads_plot = figure(plot_width=800, plot_height=800)
counts_vs_rads_plot.add_glyph(source, lo_counts_glyph)
counts_vs_rads_plot.add_glyph(source, hi_counts_glyph)
counts_vs_rads_plot.add_glyph(source2, angle_glyph)

m_vs_n_plot = figure(plot_width=800, plot_height=800)
m_vs_n_plot.scatter('y0', 'y1', source=source)
m_vs_n_plot.circle([0], [0], size=8, color='red')


lo_slider = Slider(start=1, end=41, value=2, step=1, title="lo pole pairs")
hi_slider = Slider(start=1, end=41, value=3, step=1, title="hi pole pairs")
angle_slider = Slider(start=0, end=2*np.pi, value=0, step=2*np.pi/1000, title="Position (rad)")

update_angle = CustomJS(args=dict(source=source2, slider=angle_slider), code="""
    var data = source.data;
    var f = slider.value;
    var x = data['x'];

    for (var i = 0; i < x.length; i++) {
        x[i] = f
    }

    // necessary becasue we mutated source.data in-place
    source.change.emit();
""")

update_lo_counts = CustomJS(args=dict(source=source, slider=lo_slider), code="""
    var precision = 4096;
    var data = source.data;
    var f = slider.value;
    var x = data['x'];
    var y = data['y0'];
    var counts_per_rads = (f * precision) / (2 * Math.PI);

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
    var x = data['x'];
    var y = data['y1'];
    var counts_per_rads = (f * precision) / (2 * Math.PI);

    for (var i = 0; i < x.length; i++) {
        y[i] = counts_per_rads * x[i] % precision
    }

    // necessary becasue we mutated source.data in-place
    source.change.emit();
""")

lo_slider.js_on_change('value', update_lo_counts)
hi_slider.js_on_change('value', update_hi_counts)
angle_slider.js_on_change('value', update_angle)


layout = column(
    lo_slider,
    hi_slider,
    angle_slider,
    row(counts_vs_rads_plot,
        m_vs_n_plot
    )
)

show(layout)
