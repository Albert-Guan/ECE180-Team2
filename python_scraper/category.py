'''
	This is a library used to get subjects for certain
	quarter
'''

import requests
import json

subj_endpoint = "https://act.ucsd.edu/scheduleOfClasses/subject-list.json?selectedTerm="
dept_endpoint = "https://act.ucsd.edu/scheduleOfClasses/department-list.json?selectedTerm="

def checkQuat(quarter):
	assert isinstance(quarter, str); # quarter should be string

def getSubjects(quarter):
	checkQuat(quarter)
	response = requests.get(subj_endpoint+quarter);
	return [subject["code"] for subject in json.loads(response.content)];

def getDepartments(quarter):
	checkQuat(quarter)
	response = requests.get(dept_endpoint+quarter);
	return [dept["code"] for dept in json.loads(response.content)];

'''
	Test
'''
quarter = "FA17"
getSubjects(quarter);
getDepartments(quarter);