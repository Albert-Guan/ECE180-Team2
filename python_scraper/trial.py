'''
	This is a file used to test to extract html data
	By POST operation
'''
url = "https://www.w3schools.com/action_page.php";
filename = "res.html"
import requests
import lxml.html as lh

form_data = {
	"lname": "Haha",
	"fname": "Who"
}

response = requests.post(url, data = form_data)

with open(filename, "w") as f:
	f.write(response.content);


