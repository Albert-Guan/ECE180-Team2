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
for term in terms:
	input_filename = directory+term+".txt" # input_filename for the txt file
	output_filename = directory+term+".json" # output_filename for json file

	# dictionary for store data: 
	# key: subject-courseNum
	# value: list of classes associated with subject-courseNum
	json_data = defaultdict(list); 

	# store the class info into dictionary
	with open(input_filename, "r") as f:
		for line in f:
			# get courseNum
			if line[0].isdigit():
				courseNum = line.strip();
			# get class info
			elif '[' in line:
				lines = ast.literal_eval(line);
				# remove classes without location
				if (len(lines) < 10):
					continue;
				json_data[subject+"-"+courseNum].append(ast.literal_eval(line));
			# get subject
			else:
				subject = line.strip();

	# form json str from dictionary and sove to the file 
	json_str = json.dumps(json_data);
	with open(output_filename,"w") as f:
		f.write(json_str);
	print term+".txt transform has been transformed to json"

print "All files have been transformed to json!"