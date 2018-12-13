import pickle
import time
import re
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
    
    def single_field_search(word):
        # List of indices where desried word is found
        indices = []
        

        for name_i in range(len(names_only)):

            # Current name is still candidate for search function
            match = True
            # number of occurences for individual keyword
            keyword_occurence = set() 
            current_name = names_only[name_i].split(' ')
            for keyword_i in range(len(word)):
                #Save the tokenized string in variable and remove '()
                #current_name = names_only[name_i].split(' ')

                if not (word[keyword_i].lower() in current_name):
                    match = False

            if match:
                keyword_occurence.add(int(indices_only[name_i]))

            indices += list(keyword_occurence)
        
        # if multiple keywords entered, need to find intersection
        '''
        if len(word) > 1: 
            indices = intersection(indices)
        '''
        #change so function returns list, not print
        if indices != []:
            result = []
            for i in indices:
                result.append(entries[i])    
        else:
            print('Entry not found')
            return None
        
        return result

    # can match partial words in any field
    def partial_word_search(word):
        # List of indices where desried word is found
        indices = []

        for keyword_i in range(len(word)):

            # number of occurences for individual keyword
            keyword_occurence = set() 
            for name_i in range(len(names_only)):
                #Save the tokenized string in variable and remove '()
                #current_name = names_only[name_i].split(' ')

                if re.search(word[keyword_i].lower(),names_only[name_i]) != None:
                    keyword_occurence.add(int(indices_only[name_i]))
            
            if len(keyword_occurence) == 0:
                print('found nothing')
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

    
    # Finds entries where word appears in any field. All words must appear in
    # a single entry; however, word can occur in any field
    def all_occurence_search(word):
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
                print('found nothing')
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
    def search_fn(word_lists,function=0):
        result_lists = []
        for list_i in range(len(word_lists)):

            if function == 0:
                result_lists.append(all_occurence_search(word_lists[list_i]))
            elif function == 1:
                result_lists.append(partial_word_search(word_lists[list_i]))
            elif function == 2:
                result_lists.append(single_field_search(word_lists[list_i]))
        return result_lists
    
    return search_fn


search = create_search_fn()
start = time.time()
want = search([['CSF1R_HUMAN']])

#diff = [x for x in want[0] if x not in want[1]]
#print(diff)
end = time.time()
print(len(want[0]))
print(want[0][0])

print(end-start)
