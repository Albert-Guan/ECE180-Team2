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

def clean(line):
	lineList = ast.literal_eval(line);
	if len(lineList) == 20 or len(lineList) == 19:
		return ["",lineList[4],lineList[6],lineList[8],lineList[10],lineList[12],lineList[14],lineList[16],lineList[18]];
	else:
		return [lineList[4],lineList[6],lineList[8],lineList[10],lineList[12],lineList[14],lineList[16],lineList[-5],lineList[-3]];

courseType_num = defaultdict(lambda:0);

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
				json_data[subject+"-"+courseNum].append(clean(line));
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

print "All files have been transformed to json!"
print "courseType statistic: "
for key in courseType_num:
	if key == "" or key[0].isdigit() or key[-1].isdigit(): continue;
	print key + ": " +str(courseType_num[key]);