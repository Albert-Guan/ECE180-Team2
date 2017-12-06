import ast
import json
from collections import defaultdict

terms = ["FA16","WI17","SP17","S117","S217","S317","SU17","SA17","FA17"]
# terms = ["FA16"];
directory = "./classData/"
courseNum = None;
subject = None;
lenSet = set();
json_data = defaultdict(list);

'''
	All input check functions
'''
def check_line_str(line):
	assert isinstance(line, str);

def check_line_list(line):
	assert isinstance(line, list);

def check_term(term):
	assert isinstance(term, str);

'''
	Main functions
'''
def clean_single_line(line):
	'''
		Leave valid information for a single class line:
			# index 0 -> course number
			# index 1 -> section number: some may not have(like some lectures)
			# index 2 -> class type ("LE","LA","DI","SE"...)
			# index 3 -> section (A01, A02 ...)
			# index 4 -> day (Mo, Tu, Wed...)
			# index 5 -> time period (10.00a - 10:50a)
			# index 6 -> building (APM,YORK,...)
			# index 7 -> room number
			# index 8 -> number of students(12, 34 ....)
		@parameters: line: string separating lines by ","
		@return:	 list containing the valid information
	'''
	check_line_str(line);
	lineList = ast.literal_eval(line);
	if len(lineList) == 20 or len(lineList) == 19:
		return ["",lineList[4],lineList[6],lineList[8],lineList[10],lineList[12],lineList[14],lineList[16],lineList[18]];
	else:
		return [lineList[4],lineList[6],lineList[8],lineList[10],lineList[12],lineList[14],lineList[16],lineList[-5],lineList[-3]];

def num_students(line):
	'''
		Calculate the number of students for a class line. 
		The last element means number of seats
		The last second element means available seats or full if it is empty string
		@parameters: line: list contain valid information
		@return:	 number of students for this line
	'''
	if line[-2] == '':
		return int(line[-1]);
	return int(line[-1]) - int(line[-2]);

# statistic the number of different type of classes
# such as "LE", "DI" and so on
courseType_num = defaultdict(lambda : 0);

# from transfer all data from .txt file to json file
for term in terms:
	input_filename = directory+term+".txt" # input_filename for the txt file
	output_filename = directory+term+".json" # output_filename for json file

	# dictionary for store data: 
	# key: subject-courseNum
	# value: list of classes associated with subject-courseNum
	json_data = defaultdict(list); 

	# store the class info into dictionary
	count = 0;
	with open(input_filename, "r") as f:
		for line in f:
			# get courseNum
			if line[0].isdigit():
				courseNum = line.strip();
			# get class info
			elif '[' in line:
				lines = ast.literal_eval(line);
				# do statistics for course type:
				if (len(lines) > 10):
					if (lines[4] != "" and not lines[4][0].isdigit() and not lines[4][-1].isdigit()):
						courseType_num[lines[4]] += 1;
					if (lines[6] != "" and not lines[6][0].isdigit() and not lines[6][-1].isdigit()):
						courseType_num[lines[6]] += 1;
				# remove classes without location
				if (len(lines) < 10) or not ("LA" in lines or "DI" in lines or "LE" in lines or "SE" in lines or "TU" in lines):
					continue;
				json_data[subject+"-"+courseNum].append(clean_single_line(line));
				if "LE" in lines:
					count += 1;
			# get subject
			else:
				subject = line.strip();

	# form json str from dictionary and sove to the file 
	json_str = json.dumps(json_data);
	with open(output_filename,"w") as f:
		f.write(json_str);
	print term+".txt transform has been transformed to json"


def clean(term):
	'''
		Fill empty student number for some classes
		@parameters: term: string representing term
		@return:	 None
	'''
	# get json string from file and transform to dictionary
	loaded_json = json.loads(open(directory+term+".json").readline());
	cleaned_json = defaultdict(list);
	for key in loaded_json.keys():
		### Uncomment for debugging ###
		# print key + ": "
		num_student = defaultdict(lambda:0);
		num_classes = defaultdict(lambda:0);
		for line in loaded_json[key]:
			if (line[1] == "SE" or line[1] == "TU") and line[-1] == '':
				line[-1] = str(0);
			### Uncomment for debugging ###
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
			### Uncomment for debugging ###
			# print line;
			# make sure each line ends with a digit
			assert line[-1].isdigit()
			newLine = line[:7] + [(str(num_students(line)))];
			### Uncomment for debugging ###
			# print newLine
			cleaned_json[key].append(newLine);

	with open(directory+term+"-cleaned.json","w") as f:
		json_str = json.dumps(cleaned_json);
		f.write(json_str);
		print term+".json has been cleaned!!!"

# clean the data for all terms
for term in terms:
	clean(term);

print "All data have been cleaned"

# plot the graph for class type statistics
import numpy as np
import matplotlib.pyplot as plt;  plt.rcdefaults();
import matplotlib.pyplot as plt;
print "Show the number of classes for different course type: "

f = plt.figure(1);
courseType_num_tuples = [];
for key in courseType_num:
	# PB is listed based on one week. So it should be divided by 12
	if key == "PB":
		courseType_num_tuples.append((key, courseType_num[key] / 12));
	# Same as PB, while average occurs 3 times for a term
	elif key == "RE":
		courseType_num_tuples.append((key, courseType_num[key] / 4));
	else:
		courseType_num_tuples.append((key, courseType_num[key]));

sorted_tuples = sorted(courseType_num_tuples, key = lambda tup : tup[1]);
print sorted_tuples;
courseTypes = tuple([ct[0] for ct in sorted_tuples]);
### Uncomment for debugging ###
# print courseTypes
courseNum = [ct[1] for ct in sorted_tuples];

# Draw the bar chart for classes for different type of classes
y_pos = np.arange(len(courseTypes));
plt.bar(y_pos, courseNum, align = 'center', alpha = 0.5);
plt.xticks(y_pos, courseTypes);
plt.title("Occurences of different class types")
plt.ylabel("Occurances")
plt.xlabel("class types")
f.show();

# Draw the pie chart for classes for different type of classes
g = plt.figure(2);
courseType_num_pie = defaultdict(lambda : 0);
for key in courseType_num:
	if key in set(["DI","LE","LA","SE","TU"]):
		courseType_num_pie[key] = courseType_num[key];
	elif key == "PB":
		courseType_num_pie["Others"] += courseType_num[key] / 12;
	elif key == "RE":
		courseType_num_pie["Others"] += courseType_num[key] / 4;
	else:
		courseType_num_pie["Others"] += courseType_num[key];
courseType_num_pie_tuples = [(key, courseType_num_pie[key]) for key in courseType_num_pie];
courseType_num_tuples = sorted(courseType_num_pie_tuples, key = lambda tup : tup[1]);
print courseType_num_pie;
courseType_num_pie = [ct[1] for ct in courseType_num_pie_tuples];
course_types_pie = [ct[0] for ct in courseType_num_pie_tuples];
plt.pie(courseType_num_pie, labels=course_types_pie,
        autopct='%1.1f%%', shadow=True, startangle=90);
plt.title("Occurences percentage chart")
g.show();
raw_input();