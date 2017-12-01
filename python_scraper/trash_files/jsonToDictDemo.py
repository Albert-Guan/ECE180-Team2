import json;
from collections import defaultdict
# Test to read data from json file
directory = "./classData/"
# get json string from file and transform to dictionary
loaded_json = json.loads(open(directory+"WI17"+".json").readline());

# key: subject-courseNum
# value: arrays of class info
def num_students(line):
	if line[-2] == '':
		return int(line[-1]);
	return int(line[-1]) - int(line[-2]);
for key in loaded_json.keys():
	print key + ": "
	num_student = defaultdict(lambda:0);
	num_classes = defaultdict(lambda:0);
	for line in loaded_json[key]:
		if (line[1] == "SE" or line[1] == "TU") and line[-1] == '':
			line[-1] = str(0);
		# print line
		if line[1] == "LA":
			num_classes["LA"] += 1;
		if line[1] == "DI":
			num_classes["DI"] += 1;
		if line[1] == "LE":
			num_classes["LE"] += 1;

		if line[1] == "LA" and line[-1] != '':
			num_student["LA"] += num_students(line);
		elif line[1] == "DI" and line[-1] != '':
			num_student["DI"] += num_students(line);
		elif line[1] == "LE" and line[-1] != '':
			num_student["LE"] = num_students(line);

	max_num_students = max([num_student["LA"], num_student["DI"], num_student["LE"]]);
	for line in loaded_json[key]:
		if "LE" in line and line[-1] == '':
			line[-1] = str(max_num_students / num_classes["LE"]);
		if "DI" in line and line[-1] == '':
			line[-1] = str(max_num_students / num_classes["DI"]);
		if "LA" in line and line[-1] == '':
			line[-1] = str(max_num_students / num_classes["LA"]);

	for line in loaded_json[key]:
		print line;
		assert line[-1].isdigit();