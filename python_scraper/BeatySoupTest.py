import bs4
from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# open with a string
soup = BeautifulSoup(html_doc,"lxml")

# find the first tag
tag = soup.p;
# this will give you a dictionary of attributes
tag.attrs;

# this will give you a string of content:
tag.string;

# this wil give you all tags named 'p'
tags = soup.find_all(attrs = {"class": "story"});

for tag in tags:
	# return a list of children of current tag
	tag.contents
	# return all descendants of a tag
	tag.descendants
	print tag.name
	print type(tag.contents[0]) == bs4.element.Tag
