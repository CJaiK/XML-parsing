import wikipedia
import re


# Function gathers text from initial page and from all wiki pages internally linked
# arg: page- title of initial wikipedia page
def wiki_scrape(page):

    # TODO
    # set to directory where text file should be saved
    DIR = ''

    # removes section titles, formulas, newlines, and single char words
    def clean_text(text):
        # remove short words
        tokens = text.split()
        tokens = [word for word in tokens if len(word) > 1]

        text = ' '.join(tokens)

        match = re.search('=+ (([0-9A-Za-z-:.()]+)\s)+=+',text)
        while match != None:
            text = re.sub('=+ (([0-9A-Za-z-:.()]+)\s)+=+',' ',text)
            match = re.search('=+ (([0-9A-Za-z-:.()]+)\s)+=+',text)

        # Remove new line characters from text
        while re.search(r'^\n+',text,) != None:
            re.sub(r'^\n+',' ', text)

        return text


    with open(DIR + 'wikitext.txt','w', encoding='utf-8') as text_file:

        main_page = wikipedia.page(page)
        links = main_page.links

        # Get text, remove section titles and newline chars, write to file
        text = main_page.content
        text = clean_text(text)
        text_file.writelines(text)
        
        for l in links:

            print(l)
            link_page = wikipedia.page(l)

            # Get text, remove section titles and newline chars, write to file
            text = link_page.content
            text = clean_text(text)
            text_file.writelines(text)

    