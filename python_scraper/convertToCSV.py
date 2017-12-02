import json
attributes = "CourseNum,SectionID,ClassType,Section,Day,Time,Building,Room,StudentsNumber"
terms = ["FA16","WI17","SP17","S117","S217","S317","SU17","SA17","FA17"]
directory = "./classData/"
csv_directory = "./csvData/"

def convertToCSV(term):
	loaded_json = json.loads(open(directory+term+"-cleaned.json").readline());
	with open(csv_directory+term+"-cleaned.csv", "w") as f:
		f.write(attributes + "\n");
		for key in loaded_json.keys():
			for line in loaded_json[key]:
				lineCSV = str(key);
				for ele in line:
					lineCSV += "," + ele;
				f.write(lineCSV + "\n");

# convert all json file to csv file
for term in terms:
	convertToCSV(term);

