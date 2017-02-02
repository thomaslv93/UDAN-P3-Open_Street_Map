import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

OSMFILE = "boston_massachusetts.osm"

MAPPING = { 
            }

def audit_postcode(postcodes, postcode):
    postcodes[postcode] += 1

def is_postcode(elem):
    return (elem.attrib['k'] == 'addr:postcode')

def audit(osmfile):
    postcodes = defaultdict(int)
    
    osm_file = open(osmfile, 'r')
    
    for event, elem in ET.iterparse(osmfile, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_postcode(tag):
                    audit_postcode(postcodes, tag.attrib['v'])
                    
                    #Test out the special case of 0239
                    if tag.attrib['v'] == '0239':
                        print "************************************"
                        for tag in elem.iter('tag'):
                            print (tag.attrib['k'],tag.attrib['v'])
                        print "************************************"
               
    osm_file.close()
    
    return postcodes


def update(code):
    
    postcode = code
    
    #Deal with unique cases
    if postcode == "0239": #After investigation, we realize this is a typo for 02139
        postcode = "02139"
    elif postcode == "MA" or postcode == "Mass Ave": #These contain no postcode information
        postcode = ""
    else:
        postcode = re.sub(re.compile(r'-[0-9]{4}$', re.IGNORECASE),"", postcode) # remove the dash and four extra digits of the zip+4 format
        postcode = re.sub(re.compile(r'^[a-z]+\b', re.IGNORECASE),"", postcode) # remove any letters at the beginning of the code, usually from the state, presumably from copying and pasting the postcode from an address
        
    #Remove postcodes beginning in 01. They are incorrect since there are no zipcodes beginning with 01 in the Greater Boston Area; all postcodes begin with 02.
    if re.search(re.compile(r'^01'),postcode):
        postcode = ""
    
    return postcode
    

def test():
    postcodes = audit(OSMFILE)
    pprint.pprint(dict(postcodes))
   
    for postcode, count in postcodes.iteritems():
            better_code = update(postcode)
            if better_code != postcode:
                print postcode, "=>", better_code
                

if __name__ == '__main__':
    test()