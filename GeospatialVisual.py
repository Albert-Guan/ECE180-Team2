from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from math import sqrt
import seaborn as sns
from bokeh.io import export_png
blues = sns.color_palette("Blues")

map_options = GMapOptions(lat=32.880, lng=-117.24, map_type="roadmap", zoom=15)

plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options)
plot.title.text = "UCSD Campus"

plot.api_key = "AIzaSyA0u5heBnNk8IayxQmCus7S6SmLNeAjmhU"

filename = "./geospatialData/FA16-geospatial.csv";

li = [];
with open(filename, "r") as f:
	f.readline();
	li = [line.split(',') for line in f];

lat_list = [float(ele[1]) for ele in li]
lon_list = [float(ele[2]) for ele in li]
size_list = [int(ele[-1]) for ele in li]

for i in range(1, len(size_list)):
	print i;
	source = ColumnDataSource(
	    data=dict(
	        lat=[lat_list[i]],
	        lon=[lon_list[i]],
	    )
	)
	# print size_list[i];
	circle = Circle(x="lon", y="lat", size=sqrt(size_list[i])/1.3, fill_color=blues.as_hex()[4], fill_alpha=0.8, line_color=None)
	plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
export_png(plot, filename = "plot.png")
show(plot)
