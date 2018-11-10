# XML-parsing

UNIPROT_parse.py:
  -Program takes directory to UNIPROT dataset
  -Gene and protein names are stored in dictionary where keys are "path" of XML element (e.g. uniprot/entry/protein/recommendedName)
  -Each entry stored in list where elements are dictionaries holding the protein information
  -Program stores list of dictionaries and list of names to disk for quick access to relevant data
  
  Steps:
  0. Recommended: close all other programs during run-time
  1. Download and extract Uniprot database to desired directory
  2. Find variable, FILE_PATH, and set to desired path where pickles variables will be saved
  3. Call function, UNIPROT_parse(file_name), with full path to Uniprot database as the argument
  4. Find variable, FILE_PATH, and set to desired path where pickles variables will be saved
  
  
protein_search.py:
  -Program accesses files holding list of protein dictionaries and list of names
  -Once data loaded, enter desired feature and program will print list of protein dictionaries
  
  Steps: 
  1. Find variable, FILE_PATH, and set to path of pickle files
  2. Call function, search(name), where 'name' is desired search term.
