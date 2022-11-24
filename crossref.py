import json
import requests

# List of DOIs we want to process, could get this from a file
dois = ["10.5962/p.304567", "10.1002/mmnd.18580020307"]

# Create header for TSV file
delimiter = "\t"
keys = ['DOI', 'title', 'container-title', 'ISSN', 'volume', 'issue', 'page', 'author', 'issued']
print(delimiter.join(keys))

# Loop through each DOI, resolve in CrossRef and output a row of data for each DOI
for doi in dois:

	response = requests.get("https://api.crossref.org/works/" + doi)
	data = response.json()
	
	# csl holds data in CSL-JSON format
	csl = data['message']

	# intiialsie row to hold data
	row = []
	
	# For each data element that we want, test whether it exists, if it does then output it
	for key in keys:
		if key in csl.keys():
			# A list of author objects, we concatenate given and family names and create a list
			if (key == 'author'):
				authorlist = [];
				for author in csl['author']:
					authorlist.append(author['given'] + ' ' + author['family'])
				# To store multiple authors in one field we concatenate using ";"
				author_delimiter = ";"
				row.append(author_delimiter.join(authorlist))
				
			elif (key == 'issued'):
				# Dates have a complicated structure
				row.append(str(csl['issued']['date-parts'][0][0]))
				
			elif (key == 'ISSN'):
				# ISSN is an array of one or more values, output the first
				row.append(csl['ISSN'][0])
				
			elif (key == 'title'):
				# Annoyingly, may be a string or an array
				if (type(csl['title']) == list):
					row.append(csl['title'][0])
				else:
					row.append(csl['title'])
					
			elif (key == 'container-title'):
				# Annoyingly, may be a string or an array
				if (type(csl['container-title']) == list):
					row.append(csl['container-title'][0])
				else:
					row.append(csl['container-title'])
					
			else:
				# A simple value such as a string or number
				# Make sure we cast it to a string otheriwse "join" will fail
				row.append(str(csl[key]))
		else:
			# This key doesn't exist so we have no data for it
			row.append("")

	# output row
	print(delimiter.join(row))


