import pickle

# extract all used names from dictionary files

entries = pickle.load(open('dictionaries/protein_dict.p','rb'))
names   = pickle.load(open('dictionaries/names_list.p','rb'))

protein_names = []
for pair in names:
    name  = pair.split(':::')[0]
    index = int(pair.split(':::')[1])

    entry = entries[index]
    protein_info = entry[0]
    for key in protein_info:
        if 'ecNumber' in key:
            continue
        elif 'name' == key:
            protein_names.append(protein_info[key].lower())
        else:
            protein_names += [n.lower() for n in protein_info[key]]

name_file = open('output.txt', 'w')
name_file.write('\n'.join(protein_names))
