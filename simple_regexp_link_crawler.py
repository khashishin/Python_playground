from urllib.request import urlopen
import re
import sys

# connect to a URL
website = urlopen(sys.argv[1])

# read html code
html = website.read()

# use re.findall to get all the links
links = re.findall('(?:src=|href=)[\"|\'](?=http|https)(.*?)[\"\']', str(html))

print (sorted(links,reverse=True))