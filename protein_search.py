import pickle
import bisect
import random

def search():

    # Path to directory of pickled variables
    # TODO
    FILE_PATH = ''

    def display(indeces):
        for i in indeces:
            print(entries[int(indeces_only[i])]) 

    def find(names_only,name,indeces):
        for i in range(len(names_only)):
            if names_only[i] == name:
                indeces.append(i)
                i+=1
                while(i < len(names_only) and names_only[i] == name):
                    indeces.append(i)
                    i+=1
                break
        if indeces != []:
            display(indeces)
        else:
            print('Name not Found')

    # load variable from disk
    entries = pickle.load(open(FILE_PATH + "protein_dict.p","rb"))
    all_names = pickle.load(open(FILE_PATH + "names_list.p","rb"))
    names_only = [x.split(':::')[0] for x in all_names]
    indeces_only = [x.split(':::')[1] for x in all_names]

    # Remove list of names appended with indexmyca
    del all_names

    run = 1
    
    # List of indeces where desired name is found
    indeces = []

    while(run):

        name = input('Search: ').lower()

        # Generate a random name for testing
        if name == 'genname':
            print(names_only[random.randint(0,len(names_only)-1)])
            continue

        if name == 'end':
            break
        
        
        find(names_only,name,indeces)
        indeces = []
        
search()

