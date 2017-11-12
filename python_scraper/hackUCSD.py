'''
	This is a file used to test to extract html data
	By POST operation from schedule of classes
'''
import bs4
from bs4 import BeautifulSoup
import requests
import lxml.html as lh

filename = "res.html"
filename2 = "res.txt"
with open(filename2, "w") as f:
	f.close();

for i in range(1,9):
	print i;
	url = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm?page="+str(i);

	empty = "";
	term = "FA17";
	subjects = ["AWP"];
	false = "false";
	true = "true";

	form_data = {
		"selectedTerm": term,
		"selectedSubjects": subjects,
		"xsoc_term": empty,
		"loggedIn": false,
		# "tabNum": empty,
		"_selectedSubjects": "1",
		# "schedOption1": true,
		# "_schedOption1": "on",
		# "schedOption11": true,
		# "_schedOption11": "on",
		# "schedOption12": true,
		# "_schedOption12": "on",
		# "schedOption3": true,
		# "_schedOption3": "on",
		# "schedOption7": true,
		# "_schedOption7": "on",
		# "schedOption8": true,
		# "_schedOption8": "on"
	}

	response = requests.post(url, data = form_data)

	with open(filename, "w") as f:
		f.write(response.content);

	soup = BeautifulSoup(open(filename,"r"),"lxml");

	res = [{"date": tag.contents[11].string.strip(), 
		 	"time": tag.contents[13].string, 
		 	"building": tag.contents[15].string} 
		 	for tag in soup.find_all(attrs = {"class": "sectxt"}) 
		 	if (len(tag.find_all(attrs = {"class": "ertext"})) == 0 or tag.find_all(attrs = {"class": "ertext"})[0].string != "Cancelled")]

	# res = [ tag.contents
	# 	 	for tag in soup.find_all(attrs = {"class": "sectxt"}) 
	# 	 	]

	with open(filename2,"a") as f:
		for d in res:
			f.write(str(d)+"\n\n");
		f.close();


