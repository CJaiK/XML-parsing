import pickle
import bisect
def search():

    def display(indeces):
        for i in indeces:
            print(entries[int(indeces_only[i])])

    def find(names_only,name,indeces):
        i = bisect.bisect_left(names_only,name)

        if i != len(names_only) and names_only[i] == name:
            # Find names that exist in multiple entries
            indeces.append(i)
            i += 1
            while(i < len(names_only) and names_only[i] == name):
                indeces.append(i)
                i += 1
            display(indeces)
            indeces = []
        else:
            print('Name not Found')
    
    def find_linear(names_only,name,indeces):
        for i in range(len(names_only)):
            if names_only[i] == name:
                indeces.append(i)
                i+=1
                while(i < len(names_only) and names_only[i] == name):
                    indeces.append(i)
                    i+=1
        if indeces != []:
            display(indeces)
        else:
            print('Name not Found')

    # load variable from disk
    entries = pickle.load(open("C:/Users/cjaik/Documents/vscode/protein_dict.p","rb"))
    all_names = pickle.load(open("C:/Users/cjaik/Documents/vscode/names_list.p","rb"))
    names_only = [x.split(':::')[0] for x in all_names]
    indeces_only = [x.split(':::')[1] for x in all_names]

    # Remove list of names appended with indexmyca
    del all_names

    run = 1
    
    # List of indeces where desired name is found
    indeces = []

    index = 530000
    while(run):
        print(names_only[index])
        index += 500
        name = input('Search: ').lower()

        if name == 'end':
            break
        
        find_linear(names_only,name,indeces)
        indeces = []
    """
        i = bisect.bisect_left(names_only,name)

        if i != len(names_only) and names_only[i] == name:
            # Find names that exist in multiple entries
            indeces.append(i)
            i += 1
            while(i < len(names_only) and names_only[i] == name):
                indeces.append(i)
                i += 1
            display(indeces)
            indeces = []
        else:
            print('Name not Found')
    """


search()

