import numpy as numpy
import xml.etree.ElementTree as ET
import re
import pickle
import bisect


# when ec number encountered, attach to last FULLNAME
# Information about each entry 
file1 = 'C:/Users/cjaik/Documents/vscode/largetest.xml'
file2 = 'C:/Users/cjaik/Documents/vscode/largetest2.xml'
file3 = 'C:/Users/cjaik/Documents/vscode/uniprot_sprot.xml'

def UNIPROT_parse(file_name):

    # Path to directory of pickled variables
    # TODO
    FILE_PATH = 'C:/Users/cjaik/Documents/vscode/'

    protein_attributes = dict() # Dictionary entry for protein names
    organism_attributes = dict() # Dictionary entry for organism name
    path = []   # List of all ancestors of current element
    entries = []  # list of protein entries
    child_group = []  # List of children
    all_names = [] # List of all names to be used for searching

    # Paths of each feature so program knows what the current element is
    extra_path = ['uniprot','entry']  # Path segment in all entries; to be removed
    name_path = ['uniprot','entry','name']   

    
    last = False # Flag for when program encounters last child

    ec_name = ""  # Name associated with EC Number
    
    ns = "{http://uniprot.org/uniprot}" # Name space of xml elements
    
    index = 0   # Index of each entry

    remove = dict.fromkeys(map(ord,'(),'), None)  # Characters that should be removed for search function

    # When program encounters a protein. Method reads children of protein, looking for text
    def parse_element(element,elem_attributes,path):
        nonlocal last
        nonlocal ec_name

        searchable = '' # String that will be used in search function

        for name in element.iter():
            if name.tag == (ns + 'protein') or name.tag == (ns + 'organism'):
                continue
            else:
                current_tag = name.tag.replace(ns,'')
                path.append(current_tag)

                # Program encounter element without text
                if list(name) != [] and (name.text == None or not re.search('[a-zA-Z0-9]',name.text)):
                    # Tier that encompasses the different names (ie 'recommendedName')
                    if len(child_group) != 0 and name == child_group[-1][-1]:
                        last = True
                    child_group.append(list(name))
                    
                else:
                    
                    # truncate repetitive path members
                    short_path = [x for x in path if x not in extra_path]
                    
                    # Set text incase encounter ec_number next iteration
                    if name.tag == (ns + 'fullName'):
                        ec_name = name.text
                        elem_attributes.setdefault('/'.join(short_path),[]).append(name.text)

                    # If ecNumber encountered, attach associated name
                    elif name.tag == (ns + 'ecNumber'):
                        elem_attributes.setdefault('/'.join(short_path),[]).append(name.text+' ('+ec_name+')')
                    else:
                        elem_attributes.setdefault('/'.join(short_path),[]).append(name.text)
                    
                    
                    # Add name to list of all names
                    if name.text != None:
                        searchable += name.text + ' '
                        #searchable = name.text.translate(remove)
                        #all_names.append(searchable.lower()+':::'+str(index))

                    path.pop()

                    # Check if encountered last child of parent elments
                    if len(child_group) != 0 and name == child_group[-1][-1]:
                        child_group.pop()
                        path.pop()
                        if last:
                            child_group.pop()
                            path.pop()
                            last = False
        
        searchable = searchable.translate(remove)
        all_names.append(searchable.lower()+':::'+str(index))               
        
        return elem_attributes

    for event, elem in ET.iterparse(file_name, events=("start", "end")):

        if event == 'start':
            current_tag = elem.tag.replace(ns,'')
            path.append(current_tag)
        
        elif event == 'end':
            # process the tag
            if elem.tag == (ns + 'name') and path == name_path:
                short_path = [x for x in path if x not in extra_path]
                protein_attributes['/'.join(short_path)] = elem.text
                
                searchable = elem.text.translate(remove)
                all_names.append(searchable.lower()+':::'+str(index))

            elif elem.tag == (ns + 'protein'):
                protein_attributes = parse_element(elem,protein_attributes,path)
            
            elif elem.tag == (ns + 'organism'):
                organism_attributes = parse_element(elem,organism_attributes,path) 

            elif elem.tag == (ns + 'entry'):
                elem.clear()

                index += 1
                entries.append((protein_attributes,organism_attributes))
                protein_attributes = dict()
                organism_attributes = dict()
            path.pop()
    
    all_names.sort()

    #Change to desired path
    pickle.dump(entries,open(FILE_PATH + "protein_dict.p","wb"))
    pickle.dump(all_names,open(FILE_PATH + "names_list.p","wb"))



