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

for i in range(10,11):
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

	# res = [{"date": tag.contents[11].string.strip(), 
	# 	 	"time": tag.contents[13].string, 
	# 	 	"building": tag.contents[15].string} 
	# 	 	for tag in soup.find_all(attrs = {"class": "sectxt"}) 
	# 	 	if (len(tag.find_all(attrs = {"class": "ertext"})) == 0 or tag.find_all(attrs = {"class": "ertext"})[0].string != "Cancelled")]

	def clean(contents):
		return [content.strip() if isinstance(content, str) else content.string.strip() for content in [content for content in contents if isinstance(content,str) or content.string != None]];


	res = [ clean(tag.contents)
		 	for tag in soup.find_all(attrs = {"class": "sectxt"}) 
		 	]

	res2 = [tag.contents for i,tag in enumerate(soup.find_all(attrs = {"class" : "crsheader"})) if i % 4 == 1]

	soup2 = soup.find_all(attrs = {"class" : "tbrdr"})[0];
	
	with open(filename2,"a") as f:
		for d in soup2.find_all('tr'):
			if d.has_attr("class"):
				print str(d.contents) + "\n";
			else:
				for i,tag in enumerate(d.find_all(attrs = {"class" : "crsheader"})):
					if i % 4 == 1:
						print tag.contents;
		f.close();


