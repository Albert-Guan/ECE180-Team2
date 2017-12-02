import json
from collections import defaultdict

'''
	sample code to read data
'''

term = "FA16"
directory = "./classData/"

loaded_json = json.loads(open(directory+term+"-cleaned.json").readline());

for key in loaded_json.keys():
	# print "courseNum:" + key;
	for line in loaded_json[key]:
		# line is a list of length 8, all elements are string
		# index 0 -> section number: some may not have(like some lectures)
		# index 1 -> class type ("LE","LA","DI","SE"...)
		# index 2 -> section (A01, A02 ...)
		# index 3 -> day (Mo, Tu, Wed...)
		# index 4 -> time period (10.00a - 10:50a)
		# index 5 -> building (APM,YORK,...)
		# index 6 -> room number
		# index 7 -> number of students(12, 34 ....)
		# print line;
		len(line)

# make use of the information above, do where ever you want:
# for example, if you want to get the statics for different subject
subjects_num_student = defaultdict(lambda : 0);

for key in loaded_json.keys():
	# print "courseNum:" + key;
	subj = key.split("-")[0];
	num = 0;
	for line in loaded_json[key]:
		# line is a list of length 8, all elements are string
		# index 0 -> section number: some may not have(like some lectures)
		# index 1 -> class type ("LE","LA","DI","SE"...)
		# index 2 -> section (A01, A02 ...)
		# index 3 -> day (Mo, Tu, Wed...)
		# index 4 -> time period (10.00a - 10:50a)
		# index 5 -> building (APM,YORK,...)
		# index 6 -> room number
		# index 7 -> number of students(12, 34 ....)
		num += int(line[-1]);
	subjects_num_student[subj] = num;

# print the result:
# for key in subjects_num_student:
# 	print "number of students for subj: " + key + " is: " + str(subjects_num_student[key]);

def getDays(days):
	assert isinstance(days, str);
	import re;
	pattern = re.compile("^M|W|F|Th|Tu");
	return re.findall(pattern, days);
