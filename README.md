# XML-parsing
patent_parse.py:
  - File formerly named XMLparse.py
  - Takes patent XML and collects introduction, citations, and tables
  
  Steps:
  1. Call function, patent_parse(file_name), where 'file_name' is the path of patent XML file
  2. patent_parse(file_name) returns 'patcit', 'nplcit', 'tables', 'intro' in this order.
    a. patcit: array containing patcit citations
    b. nplcit: array containing nplcit citations
    c. tables: dictionary containing all tables. To get specific table, use num attribute (ex table['0004'] gets table 4)



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
  2. When prompt 'Search: ' appears, enter desired name; can use any desired attribute (name, ecnumber, etc)
  3. Function prints all occurences of searched item; some searches are too much to be displayed in terminal.
