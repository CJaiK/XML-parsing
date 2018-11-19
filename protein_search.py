import pickle
import time
# closure, clojure, scheme/lisp, haskell

def create_search_fn():
    
    # Path to deirectory of pickled variables
    # TODO
    FILE_PATH = 'C:/Users/cjaik/Documents/vscode/'

    # Load variables from disk
    
    entries = pickle.load(open(FILE_PATH + 'protein_dict.p','rb'))
    all_names = pickle.load(open(FILE_PATH + 'names_list.p','rb'))
    names_only = [x.split(':::')[0] for x in all_names]
    indices_only = [x.split(':::')[1] for x in all_names]

    # Remove list of names appended with index
    del all_names

    # Get intersection of keyword occurences
    def intersection(indices):
        initial_encounter = set()
        intersect = []

        for x in indices:
            if x not in initial_encounter:
                initial_encounter.add(x)
            elif x not in intersect:
                intersect.append(x)
        return intersect

        
    def search(word):
        # List of indices where desried word is found
        indices = []

        for keyword_i in range(len(word)):

            # number of occurences for individual keyword
            keyword_occurence = set() 
            for name_i in range(len(names_only)):
                #Save the tokenized string in variable and remove '()
                current_name = names_only[name_i].split(' ')

                if word[keyword_i].lower() in current_name:
                    keyword_occurence.add(int(indices_only[name_i]))
            
            if len(keyword_occurence) == 0:
                return None

            indices += list(keyword_occurence)
        
        # if multiple keywords entered, need to find intersection
        if len(word) > 1: 
            indices = intersection(indices)

        #change so function returns list, not print
        if indices != []:
            result = []
            for i in indices:
                result.append(entries[i])    
        else:
            print('Entry not found')
            return None
        
        return result
    
    # Function to batch search multiple entries; takes a list of lists containing search keywords
    def search_fn(word_lists):
        result_lists = []
        for list_i in range(len(word_lists)):
            result_lists.append(search(word_lists[list_i]))
        return result_lists
    
    return search_fn
