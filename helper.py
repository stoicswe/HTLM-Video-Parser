import requests
from lxml import html
import argparse
import re
import json

def extract_flashvars(text):
    # Using regex to find a line starting with "var flashvars_"
    match = re.search(r'var flashvars_\w+\s*=\s*({.*?});', text, re.DOTALL)
    if match:
        # Extract just the JSON part
        json_str = match.group(1)
        try:
            # Parse the JSON data
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError:
            return json_str
    return None

def can_convert_to_int(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False

def find_item_by_quality(items_list, quality_value=1080):
    highest_quality = 0
    highest_quality_item = None
    for item in items_list:
        if item.get('quality') == str(quality_value):
            return item
        if (item.get('quality') != None):
            if can_convert_to_int(item.get('quality')) and int(item.get('quality')) > highest_quality:
                highest_quality = int(item.get('quality'))
                highest_quality_item = item
    return highest_quality_item

# Begin program, get args
parser = argparse.ArgumentParser(description='')
parser.add_argument('-u', '--url', type=str, help='URL to parse')
args = parser.parse_args()

# Fetch the page
URL_STR = args.url
response = requests.get(URL_STR)
tree = html.fromstring(response.text)

# Find elements using XPath
elements = tree.xpath('//div[@class="original mainPlayerDiv"]/script[@type="text/javascript"]')

# Extract text
if elements:
    text = elements[0].text_content()
    # at this point, we have the text (ie. script) that controls the player div
    # we need to grab the URI where the content is located from this text
    subtext = extract_flashvars(text)
    # Obtain the list of media definitions that are on the page
    mediaTypes = subtext.get("mediaDefinitions")
    mediaDef = find_item_by_quality(mediaTypes)
    mediaURI = mediaDef.get("videoUrl")
    print(mediaURI)