import numpy as numpy
import xml.etree.ElementTree as ET
import re
import pickle
import bisect

# Information about each entry
file1 = 'C:/Users/cjaik/Documents/vscode/largetest.xml'
file2 = 'C:/Users/cjaik/Documents/vscode/largetest2.xml'
file3 = 'C:/Users/cjaik/Documents/vscode/uniprot_sprot.xml'

def large_parse(file_name):

    index = 0   # Index of each entry

    protein_attributes = dict() # Dictionary entry for protein names
    path = []   # List of all ancestors of current element
    entries = []  # list of protein entries
    child_group = []  # List of children
    all_names = [] # List of all names to be used for searching

    # Paths of each feature so program knows what the current element is
    protein_path = ['uniprot','entry','protein']
    name_path = ['uniprot','entry','name']
    recommendedName_path = [protein_path,'recommendedName','fullName']
    ecNumber_path = [protein_path,'recommendedName','ecNumber']
    alternativeName_path = [protein_path,'alternativeName']

    # Flag for when program encounters last child
    global last
    last = False

    global ec_name
    ec_name = ""  # Name associated with EC Number

    # Name space of xml elements
    ns = "{http://uniprot.org/uniprot}"


    # When program encounters a protein. Method reads children of protein, looking for text
    def parse_protein(protein,protein_attributes,path):
        global last
        global ec_name

        for name in protein.iter():
            if name.tag == (ns + 'protein'):
                continue
            else:
                current_tag = name.tag.replace(ns,'')
                path.append(current_tag)

                # Program encounter element without text
                if not re.search('[a-zA-Z0-9]',name.text):
                    # Tier that encompasses the different names (ie 'recommendedName')
                    if len(child_group) != 0 and name == child_group[-1][-1]:
                        last = True
                    child_group.append(list(name))
                    
                else:

                    # If ecNumber encountered, attach associated name
                    if name.tag == (ns + 'ecNumber'):
                        protein_attributes.setdefault('/'.join(path),[]).append(name.text+' ('+ec_name+')')
                    else:
                        protein_attributes.setdefault('/'.join(path),[]).append(name.text)
                    
                    # Set text incase encounter ec_number next iteration
                    ec_name = name.text

                    # Add name to list of all names
                    #all_names.append(name.text+':'+str(index))
                    bisect.insort_left(all_names,name.text.lower()+':::'+str(index))

                    path.pop()

                    # Check if encountered last child of parent elments
                    if len(child_group) != 0 and name == child_group[-1][-1]:
                        child_group.pop()
                        path.pop()
                        if last:
                            child_group.pop()
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
                #all_names.append(elem.text+':'+str(index))
                bisect.insort_left(all_names,elem.text.lower()+':::'+str(index))

            elif elem.tag == (ns + 'protein'):
                protein_attributes = parse_protein(elem,protein_attributes,path)
                entries.append(protein_attributes)
                protein_attributes = dict()
                #index += 1

            elif elem.tag == (ns + 'entry'):
                elem.clear()
                # try increment index after clearing last entry
                index += 1
            path.pop()
    
    #all_names = sorted(all_names)
    #all_names = [x.lower() for x in all_names]

    return entries,all_names


entries,all_names = large_parse(file3)
pickle.dump(entries,open("C:/Users/cjaik/Documents/vscode/protein_dict.p","wb"))
pickle.dump(all_names,open("C:/Users/cjaik/Documents/vscode/names_list.p","wb"))