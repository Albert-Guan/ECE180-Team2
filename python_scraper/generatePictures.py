from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool, WheelZoomTool, BoxSelectTool
)
from math import sqrt
from collections import defaultdict
from bokeh.io import export_png

terms = ["FA16","WI17","SP17","S117","S217","S317","SU17","SA17","FA17"]
map_options = GMapOptions(lat=32.880, lng=-117.24, map_type="roadmap", zoom=15)

# For GMaps to function, Google requires you obtain and enable an API key:
#
#     https://developers.google.com/maps/documentation/javascript/get-api-key
#
# Replace the value below with your personal API key:


day_to_digit = {
	'M' 	: 1,
	'F' 	: 5,
	'Th'	: 4,
	'Tu'	: 2,
	'W'		: 3
}

term_index = 0;
# terms = ["FA16"];
for term in terms:
	# term = "FA16"
	filename = "./geospatialData/" + term + "-geospatial.csv";
	li = defaultdict(dict);
	with open(filename, "r") as f:
		f.readline();
		for line in f:
			elements = line.split(',');
			if elements[-2] not in li[elements[-3]]:
				li[elements[-3]][elements[-2]] = [];
			li[elements[-3]][elements[-2]].append(elements);

	for day in li.keys():
		for hour in li[day].keys():
			lat_list = [float(ele[1]) for ele in li[day][hour]]
			lon_list = [float(ele[2]) for ele in li[day][hour]]
			size_list = [int(ele[-1]) for ele in li[day][hour]]

			plot = GMapPlot(x_range=Range1d(), y_range=Range1d(), map_options=map_options)
			plot.title.text = "UCSD Campus - " + term + " day: " + day + " hour: " + hour;
			plot.api_key = "AIzaSyA0u5heBnNk8IayxQmCus7S6SmLNeAjmhU";
			for i in range(1, len(size_list)):
				source = ColumnDataSource(
				    data=dict(
				        lat=[lat_list[i]],
				        lon=[lon_list[i]],
				    )
				)
				# print size_list[i];
				circle = Circle(x="lon", y="lat", size=sqrt(size_list[i])/1.3, fill_color="blue", fill_alpha=0.8, line_color=None)
				plot.add_glyph(source, circle)
			plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
			# output_file("./geoSpatialPlots/"+day+"-"+hour+"-"+"gmap_plot.html");
			output_file_name = "./geoSpatialPlots/"+str(term_index)+"-"+str(day_to_digit[day])+"-"+hour+"-"+"geoMap.png"
			export_png(plot, filename = output_file_name);
			print term + "-" + day + "-" + hour + ": done"
			# show(plot)
	term_index += 1;