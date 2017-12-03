'''
	This file contains data which is used to scrape data
	from ucsd website
'''

from bs4 import BeautifulSoup
from category import * 
import bs4
import requests
import lxml.html as lh

endpoint_url = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm?page=";
error_log_file = "error_log_file.txt";

'''
	All parameters check functions
'''
def checkTerm(term):
	assert isinstance(term, str);

def checkSubj(subject):
	assert isinstance(subject, str);

def checkPageNum(pageNum):
	assert isinstance(pageNum, int);
	assert pageNum > 0;

def checkDept(department):
	assert isinstance(department, str);

def checkFormData(form_data):
	assert isinstance(form_data, dict);

def checkContents(contents):
	assert isinstance(contents, list);

def clean(contents):
	'''
		Remove the None value and 
		remove prevailing and ending space for a string
		@parameters: contents: content list
		@return:	 cleaned string list	
	'''
	checkContents(contents);
	return [str(content.strip()) if isinstance(content, str) else str(content.string.strip()) for content in [content for content in contents if isinstance(content,str) or content.string != None]];

'''
	data scraper functions
'''
def isValid(contents):
	'''
		Check if contents contain "Cancelled" or "TBA" or "FI"
		@parameters: contents: content list
		@return:	 cleaned content list	
	'''
	checkContents(contents);
	cleanedContents = set(clean(contents));
	return not ("Cancelled" in cleanedContents or "TBA" in cleanedContents or "FI" in cleanedContents);

def scrapeClassData(pageNum, form_data):
	'''
		Scrape data with page number and query input
		@parameters: pageNum: number of page for a certian query input
					 form_data: dictionary containing the query requirement
		@return:	 query result in form of string
	'''	
	checkPageNum(pageNum);
	checkFormData(form_data);
	res = [];
	# try the query
	try:
		url = endpoint_url + str(pageNum);
		reponse = requests.post(url, data = form_data);
		# create beatysoup tree by the retrieving stream
		soup = BeautifulSoup(reponse.content,"lxml").find(attrs = {"class" : "tbrdr"});
		if soup == None:
			return None;
		else:
			for d in soup.find_all('tr'):
				if d.has_attr("class") and isValid(d.contents):
					res.append(clean(d.contents));
				else:
					for i,tag in enumerate(d.find_all(attrs = {"class" : "crsheader"})):
						if i % 4 == 1:
							res.append(str(tag.contents[0]));
		# if no error, return the value
		return res;

	# handle connection exception
	except requests.exceptions.RequestException as e: 
		# log the error
		with open(error_log_file,"a") as f:
			f.write(str(form_data) + ": " + str(pageNum) + "exceptions: " + str(e)+"\n");

	# redo the scrape
	return scrapeClassData(pageNum, form_data);

'''
	scape data by subject
'''
def scrapeByTermAndSubject(term, subject, pageNum):
	'''
		Scrape the data by term and subject
		@parameters: term: string representing the term
					 subject: string representing subject
					 pageNum: int representing pageNum
		@return:	 result of scraping	
	'''
	checkTerm(term);
	checkSubj(subject);
	checkPageNum(pageNum);

	# construct the query data
	form_data = {
		"selectedTerm": term,
		"selectedSubjects": [subject]
	}

	# get the result in form of list
	res = scrapeClassData(pageNum, form_data)
	return res;

'''
	scrape data for all subjects
	save to file res.txt
'''
filename = "res.txt";
terms = ["FA16","WI17","SP17","S117","S217","S317","SU17","SA17","FA17"]
directory = "./classData/"
# terms = ["FA17"];
testSubjects = ["CSE"];

for term in terms:
	filename = directory+term+".txt";
	nextSubject = False;
	with open(filename, "w") as f:
		for subject in getSubjects(term):
			f.write(subject+"\n");
			for pageNum in range(1,50):
				print "term: " + term + ", subject: " + str(subject) + ", pageNum " + str(pageNum);
				lineGen = scrapeByTermAndSubject(term, str(subject), pageNum);
				if lineGen == None:
					break;
				for line in lineGen:
					# if line == None:
					# 	nextSubject = True;
					f.write(str(line)+"\n");
					f.flush();
				if nextSubject:
					nextSubject = False;
					break;
					
'''
	scape data by department
	@TODO: Seems does not work, need to check the reason
'''
def scrapeByTermAndDept(term, department, pageNum):
	checkTerm(term);
	checkPageNum(pageNum);
	checkDept(department);

	form_data = {
		"selectedTerm": term,
		"selectedDepartments": [department],
	}

	res = scrapeClassData(pageNum, form_data)
	return res;

'''
	Test
'''
scrapeByTermAndSubject("FA17", "AWP", 1)
scrapeByTermAndDept("FA17", "AWP", 1)

