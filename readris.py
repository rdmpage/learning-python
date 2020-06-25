#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import os
from pprint import pprint
import rispy
filepath = 'export.ris'
with open(filepath, 'r') as bibliography_file:
    entries = rispy.load(bibliography_file)
    for entry in entries:
        #print(entry['primary_title'])
        #print(entry['first_authors'])
        print(entry)
