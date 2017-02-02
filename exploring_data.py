import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

def count_tags(filename):
    tags = defaultdict(int)
    tag_iter = ET.iterparse(filename)
    
    while True:
        try:
            tags[tag_iter.next()[1].tag]+=1
        except StopIteration:
            break
    
    pprint.pprint(tags)
    return tags
    
def count_keys(filename):
    node_keys = defaultdict(int)
    way_keys = defaultdict(int)
    
    for event, elem in ET.iterparse(filename, events=("start",)):  
        if elem.tag == "node":
            for tag in elem.iter("tag"):
                node_keys[tag.attrib['k']] += 1  
        elif elem.tag == "way":
            for tag in elem.iter("tag"):
                way_keys[tag.attrib['k']] += 1 
    print "Node Keys: \n"
    pprint.pprint(sorted( ((v,k) for k,v in node_keys.iteritems()), reverse=True))
    print "\nWay Keys: \n"
    pprint.pprint(sorted( ((v,k) for k,v in way_keys.iteritems()), reverse=True))
    return [node_keys,way_keys]        

def test():

    tags = count_tags('boston_massachusetts.osm')
    keys = count_keys('boston_massachusetts.osm')
    
if __name__ == "__main__":
    test()