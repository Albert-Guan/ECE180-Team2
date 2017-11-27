import json;
# Test to read data from json file
directory = "./classData/"
# get json string from file and transform to dictionary
loaded_json = json.loads(open(directory+"FA17"+".json").readline());

# key: subject-courseNum
# value: arrays of class info
for key in loaded_json.keys():
	print key + ": "
	for line in loaded_json[key]:
		print line