import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import string

OSMFILE = "boston_massachusetts.osm"

def audit_city_name(city_names, city_name):
    city_names[city_name] += 1

def is_city_name(elem):
    return (elem.attrib['k'] == 'addr:city')

def audit(osmfile):
    city_names = defaultdict(int)
    
    osm_file = open(osmfile, 'r')
    
    for event, elem in ET.iterparse(osmfile, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_city_name(tag):
                    audit_city_name(city_names, tag.attrib['v']);
               
    osm_file.close()
    
    return city_names


def update(name):
    
    city_name = name
    
    #Deal with unique case
    if city_name == "2067 Massachusetts Avenue":
        city_name = "Cambridge"
    else:    
        city_name = re.sub(re.compile(r'(\.|,)\s\S+$', re.IGNORECASE),"", city_name) # Deals with city names ending with the state. ie Watertown, MA or Cambridge, Massachusetts. Removes the state name.
        city_name = re.sub(re.compile(r'^(\.|,)\s'),"", city_name) # Deals with the ', Arlington, MA' case and other potential cases with the same form, presumably copied and pasted from an address without removing the preceding delimeter
        city_name = string.capwords(city_name) # Puts the city name into our desired first-letter-of-each-word-capitalized format.
    
    return city_name
    

def test():
    city_names = audit(OSMFILE)
    pprint.pprint(dict(city_names))
    
    for city_name, count in city_names.iteritems():
            better_name = update(city_name)
            if better_name != city_name:
                print city_name, "=>", better_name

if __name__ == '__main__':
    test()