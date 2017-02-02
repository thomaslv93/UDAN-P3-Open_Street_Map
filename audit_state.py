import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

OSMFILE = "boston_massachusetts.osm"

MAPPING = { "MA": "MA",
            "MA- MASSACHUSETTS": "MA",
            "MASSACHUSETTS": "MA",
            "Ma": "MA",
            "Massachusetts": "MA",
            "ma":"MA"
            }

def audit_state_name(state_names, state_name):
    state_names[state_name] += 1

def is_state_name(elem):
    return (elem.attrib['k'] == 'addr:state')

def audit(osmfile):
    state_names = defaultdict(int)
    
    osm_file = open(osmfile, 'r')
    
    for event, elem in ET.iterparse(osmfile, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_state_name(tag):
                    audit_state_name(state_names, tag.attrib['v']);
               
    osm_file.close()
    
    return state_names


def update(name, mapping=MAPPING):
    if name in mapping.keys():
        return mapping[name]
    else:
        return name;

def test():
    state_names = audit(OSMFILE)
    pprint.pprint(dict(state_names))

if __name__ == '__main__':
    test()