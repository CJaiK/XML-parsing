# XML-parsing

UNIPROT_parse.py:
  -Program takes directory to UNIPROT dataset
  -Gene and protein names are stored in dictionary where keys are "path" of XML element (e.g. uniprot/entry/protein/recommendedName)
  -Each entry stored in list where elements are dictionaries holding the protein information
  -Program stores list of dictionaries and list of names to disk for quick access to relevant data
  
protein_search.py:
  -Program accesses files holding list of protein dictionaries and list of names
  -Once data loaded, enter desired feature and program will print list of protein dictionaries
