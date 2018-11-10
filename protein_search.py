import pickle

def search(name):
    
    # Path to deirectory of pickled variables
    # TODO
    FILE_PATH = 'C:/Users/cjaik/Documents/vscode/'

    # Load variables from disk
    entries = pickle.load(open(FILE_PATH + 'protein_dict.p','rb'))
    all_names = pickle.load(open(FILE_PATH + 'names_list.p','rb'))
    names_only = [x.split(':::')[0] for x in all_names]
    indeces_only = [x.split(':::')[1] for x in all_names]

    # Remove list of names appended with index
    del all_names

    # List of indeces where desried name is found
    indeces = []

    for i in range(len(names_only)):
        if names_only[i] == name.lower():
            indeces.append(i)
    
    if indeces != []:
        for i in indeces:
            print(entries[int(indeces_only[i])])
    
    else:
        print('Name not found')
