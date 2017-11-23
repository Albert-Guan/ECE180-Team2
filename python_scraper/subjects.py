'''
	This is a library used to get subjects for certain
	quarter
'''

import requests
import json

endpoint = "https://act.ucsd.edu/scheduleOfClasses/subject-list.json?selectedTerm="

def getSubjects(quarter):
	assert isinstance(quarter, str);
	response = requests.get(endpoint+quarter);
	return [subject["code"] for subject in json.loads(response.content)];

'''
	Test
'''
