import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

OSMFILE = "boston_massachusetts.osm"

def audit_phone_num(phone_nums, phone_num):
    phone_nums[phone_num] += 1

def is_phone_num(elem):
    return (elem.attrib['k'] == 'phone')

def audit(osmfile):
    phone_nums = defaultdict(int)
    
    osm_file = open(osmfile, 'r')
    
    for event, elem in ET.iterparse(osmfile, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_phone_num(tag):
                    audit_phone_num(phone_nums, tag.attrib['v']);
               
    osm_file.close()
    
    return phone_nums


def update(num):
   
    phone_num = num
    
    #Deal with unique cases
    if phone_num == "617442299" or phone_num == "+1 - 617-466-207": #These don't have enough digits to be phone numbers. Typos have made these useless.
        phone_num = ""
    elif phone_num == "+1617958DELI": #Translate this to numbers
        phone_num = "617-958-3354"
    elif phone_num == "+1 617 357 LUCK": #Translate this to numbers
        phone_num = "617-357-5825"
    else:
        temp = re.findall(re.compile(r'[02-9][0-9]{2}[^0-9]*[0-9]{3}[^0-9]*[0-9]{4}'),phone_num)
        # The above finds two groups of 3 digits and one group of 4 digits separated by non-numerical characters and specifies that the first digit cannot be 1
        for i in range(len(temp)):
            temp[i] = re.sub(re.compile(r'[^0-9]+'),"", temp[i])
            temp[i] = temp[i][:3] + '-' + temp[i][3:6] + '-' + temp[i][6:]
            if i == 0:
                phone_num = temp[i]
            else:
                phone_num = phone_num + ', ' + temp[i]
                # multiple phone numbers can be stored   
    
    return phone_num
    

def test():
    phone_nums = audit(OSMFILE)
    pprint.pprint(dict(phone_nums))
    
    for phone_num, count in phone_nums.iteritems():
            better_num = update(phone_num)
            print phone_num, "=>", better_num
            
            
if __name__ == '__main__':
    test()