import numpy as numpy
import xml.etree.ElementTree as ET
import re

# Information about each entry

file1 = 'largetest.xml'
file2 = 'largetest2.xml'
file3 = 'uniprot_sprot.xml'

def large_parse(file_name):
    protein_attributes = dict() # Dictionary entry for protein names
    path = []   # List of all ancestors of current element
    entries = []  # list of protein entries
    name_group = []  # List of children

    # Paths of each feature so program knows what the current element is
    protein_path = ['uniprot','entry','protein']
    name_path = ['uniprot','entry','name']
    recommendedName_path = [protein_path,'recommendedName','fullName']
    ecNumber_path = [protein_path,'recommendedName','ecNumber']
    alternativeName_path = [protein_path,'alternativeName']

    # Flag for when program encounters last child
    global last
    last = False

    # Name space of xml elements
    ns = "{http://uniprot.org/uniprot}"


    # When program encounters a protein. Method reads children of protein, looking for text
    def parse_protein(protein,protein_attributes,path):
        global last
        
        for name in protein.iter():
            if name.tag == (ns + 'protein'):
                continue
            else:
                current_tag = name.tag.replace(ns,'')
                path.append(current_tag)

                # Program encounter element without text
                if not re.search('[a-zA-Z0-9]',name.text):
                    # Tier that encompasses the different names (ie 'recommendedName')
                    if len(name_group) != 0 and name == name_group[-1][-1]:
                        last = True
                    name_group.append(list(name))
                    
                else:
                    protein_attributes.setdefault('/'.join(path),[]).append(name.text)
                    path.pop()

                    # Check if encountered last child of parent elments
                    if len(name_group) != 0 and name == name_group[-1][-1]:
                        name_group.pop()
                        path.pop()
                        if last:
                            name_group.pop()
                            path.pop()
                            last = False
                
        
        return protein_attributes

    # Alternate method using 'paths' to determine category
    # Keeps information about the hierarchy


    for event, elem in ET.iterparse(file_name, events=("start", "end")):

        if event == 'start':
            current_tag = elem.tag.replace(ns,'')
            path.append(current_tag)
            # Test to find all tags under 'protein'
        # Remove when finished
        
        elif event == 'end':
            # process the tag
            if elem.tag == (ns + 'name') and path == name_path:
                protein_attributes['/'.join(path)] = elem.text
            elif elem.tag == (ns + 'protein'):
                protein_attributes = parse_protein(elem,protein_attributes,path)
                entries.append(protein_attributes)
                protein_attributes = dict()
            elif elem.tag == (ns + 'entry'):
                elem.clear()
        
            path.pop()
    return entries


test = large_parse(file2)
print(test[0])



