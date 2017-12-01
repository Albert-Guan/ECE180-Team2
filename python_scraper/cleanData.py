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

def clean_single_line(line):
	lineList = ast.literal_eval(line);
	if len(lineList) == 20 or len(lineList) == 19:
		return ["",lineList[4],lineList[6],lineList[8],lineList[10],lineList[12],lineList[14],lineList[16],lineList[18]];
	else:
		return [lineList[4],lineList[6],lineList[8],lineList[10],lineList[12],lineList[14],lineList[16],lineList[-5],lineList[-3]];

def num_students(line):
	if line[-2] == '':
		return int(line[-1]);
	return int(line[-1]) - int(line[-2]);

# statistic the number of different type of classes
# such as "LE", "DI" and so on
courseType_num = defaultdict(lambda:0);

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
				if (len(lines) > 10):
					courseType_num[lines[4]] += 1;
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
	# get json string from file and transform to dictionary
	loaded_json = json.loads(open(directory+term+".json").readline());
	cleaned_json = defaultdict(list);
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
			# print line; # used for debug
			# make sure each line ends with a digit
			assert line[-1].isdigit()
			newLine = line[:7] + [(str(num_students(line)))];
			print newLine
			cleaned_json[key].append(newLine);

	with open(directory+term+"-cleaned.json","w") as f:
		json_str = json.dumps(cleaned_json);
		f.write(json_str);
		print term+".json has been cleaned!!!"

for term in terms:
	clean(term);

print "All data have been cleaned"

