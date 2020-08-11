#--------------------------------------------------------------------------------------------------------
# The script has been verified to run with Python 3.6.
# July 21, 2020
#--------------------------------------------------------------------------------------------------------

import urllib.parse     # URL Libraries for interacting with the BHL API
import urllib.request
import json             # JSON library for extracting informaion from the API responses
import re               # Regular Expression library for validating values
import csv              # Comma-separated value library for writing delimited data

#--------------------------------------------------------------------------------------------------------
# FUNCTIONS

# Execute an API method and return the response
def get_data_from_api(parameters):
    url = service_url + urllib.parse.urlencode(parameters)
    url_handler = urllib.request.urlopen(url)
    return url_handler.read().decode('utf-8')

# Load the supplied data into a JSON object and validate it
def load_json(data):
    json_data=json.loads(data)
    if 'Status' not in json_data or json_data['Status'] != 'ok':      # Successful API invocation?
        print('=== Failure to Retrieve ===')                          # Exit if unsuccessful
        print(data)
        exit()
    return json_data

# Read the value of the specified key from the supplied json
def get_json_value(json, key):
    value = ''
    if key in json:
        value = json[key]
    return value

#--------------------------------------------------------------------------------------------------------
# MAIN PROGRAM

# BHL API Key
# If you need a key, or have forgotten your key, go to https://www.biodiversitylibrary.org/getapikey.aspx
bhl_key = 'YOUR_API_KEY_GOES_HERE'

# BHL API endpiont
service_url = 'https://www.biodiversitylibrary.org/api3?'

# Get the BHL Title ID for which to accumulate segment data
title_id = input('Enter BHL Title ID: ')

# Validate the Title ID
# 1) Check the length of the value to make sure that something was entered.
# 2) Use the regular expression library (re) to make sure the entered value is numeric.
if len(title_id) < 1 or None == re.fullmatch(r'\d+',title_id):  
    print('You must enter the numeric BHL Title ID')
    exit()

# Create the output file for writing (overwrites the file if it already exists)
output_file = open('BHLTitleSegments.csv','w+', newline='', encoding='utf-8')

# Open a writer for sending Excel tab-delimited data (dialect='excel-tab') to the output file
writer = csv.writer(output_file, dialect='excel-tab')
writer.writerow(('Title ID', 'Item ID', 'FullTitle', 'Volume', 'PublicationYears', 'Year', 'EndYear', 'HoldingInstitution', 'Segment ID', 'SegmentTitle', 'SegmentAuthors', 'Pages', 'DOI', 'BioStor ID', 'Creation Date'))

# Call the GetTitleMetadata API method to get the title information, including a list of associated Items
title_data = get_data_from_api({'op':'GetTitleMetadata','id':title_id,'items':'t','format':'json','apikey':bhl_key})

# Load the API response into a JSON object
title_json = load_json(title_data)

# Read the Title metadata from the JSON
title = title_json['Result'][0]
full_title = get_json_value(title, 'FullTitle')
publication_years = get_json_value(title, 'PublicationDate')

# Loop through every Item associated with the Title
for item in title_json['Result'][0]['Items']:

    # Get the Item ID
    item_id = item['ItemID']

    # Call the GetItemMetadata API method to get the item information, including a list of associated parts (segments)
    item_data = get_data_from_api({'op':'GetItemMetadata', 'id': item_id, 'pages':'f', 'ocr':'f', 'parts':'t', 'format': 'json','apikey':bhl_key})

    # Load the API response into a JSON object
    item_json = load_json(item_data)

    # Read the Item metadata from the JSON
    item_result = item_json['Result'][0]
    volume = get_json_value(item_result, 'Volume')
    start_year = get_json_value(item_result, 'Year')
    end_year = get_json_value(item_result, 'EndYear')
    holding_institution = get_json_value(item_result, 'HoldingInstitution')

    # Make sure the Item has Parts
    if 'Parts' in item_result:

        # Loop through every Part (segment) for this Item
        for part in item_result['Parts']:

            # Get the Part ID
            part_id = part['PartID']

            # Call the GetPartMetadata API method to get the part information
            part_data = get_data_from_api({'op':'GetPartMetadata','id':part_id,'pages':'f','names':'f','format':'json','apikey':bhl_key})

            # Load the API response into a JSON object
            part_json = load_json(part_data)

            # Read the Part metadata from the JSON
            part_result = part_json['Result'][0]
            segment_title = get_json_value(part_result, 'Title')
            pages = get_json_value(part_result, 'PageRange')
            doi = get_json_value(part_result, 'Doi')
            creation_date = get_json_value(part_result, 'CreationDate')

            # Get the BioStor ID for the Part
            biostor_id = ''
            if 'Identifiers' in part_result:
                for identifier in part_result['Identifiers']:
                    if identifier['IdentifierName'].lower() == 'biostor':
                        biostor_id = identifier['IdentifierValue']

            # Read the author metadata from the JSON and build a list of authors
            authors = ''
            if 'Authors' in part_result:
                
                # Loop through every Author for this Part
                for author in part_result['Authors']:

                    # Read the author metadata from the JSON
                    author_name = get_json_value(author, 'Name')
                    fuller_form = get_json_value(author, 'FullerForm')

                    # Add the author to the list
                    authors = authors + '|' + (author_name.strip() + ' ' + fuller_form).strip()

                # Remove the | prefix from the author list
                authors = authors.lstrip('|')

            # Write the metadata to the output file
            writer.writerow((title_id, item_id, full_title, volume, publication_years, start_year, end_year, holding_institution, part_id, segment_title, authors, pages, doi, biostor_id, creation_date))

    else:
        # No Parts for this Item, so just write the Title and Item metadata to the output file
        writer.writerow((title_id, item_id, full_title, volume, publication_years, start_year, end_year, holding_institution, '', '', '', '', '', '', ''))

# Close the output file
output_file.close()
