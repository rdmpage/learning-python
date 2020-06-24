import os
import rispy
entries = [
{'type_of_reference': 'JOUR',
 'id': '42',
 'primary_title': 'The title of the reference',
 'first_authors': ['Marxus, Karlus', 'Lindgren, Astrid']
 },{
'type_of_reference': 'JOUR',
 'id': '43',
 'primary_title': 'Reference 43',
 'abstract': 'Lorem ipsum'
 }]
filepath = 'export.ris'
with open(filepath, 'w') as bibliography_file:
    rispy.dump(entries, bibliography_file)
    