import xml.etree.ElementTree as ET
import re
import sys

class XMLDoc:
    def __init__(self, filename, title=False, abstract=False,intro=False, tables=False, citations=False):
        self.title = ""
        self.abstract = ""
        self.intro = self.summary = ""
        self.tables = None
        self.nplcit_table = []

        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.abstract_section = self.root.find('abstract')
        self.citations = self.root.find('us-bibliographic-data-grant').find('us-references-cited')
        self.data = self.root.find('description')

        #self.f = self.parse_section("field of invention")
        #self.f = re.sub(r'\s\([a-zA-Z,.\s&]*\s*\d{4}[\)]','',self.f)
        if title:
            self.title = self.root.find('us-bibliographic-data-grant').find('invention-title').text
        if abstract:
            self.abstract = self.parse_abstract()
        if intro:
            self.intro = self.parse_section("background")
            self.intro = re.sub(r'\s\([a-zA-Z,.\s&]*\s*\d{4}[\)]','',self.intro)
            self.summary = self.parse_section("summary")
            self.summary = re.sub(r'\s\([a-zA-Z,.\s&]*\s*\d{4}[\)]','',self.summary)
        if tables:
            self.tables = self.parse_all_tables()
        if citations and self.citations:
            self.nplcit_table = self.parse_citations()

    #Collect abstract from patent
    def parse_abstract(self):
        abstract = ''
        for elem in self.abstract_section:
            if elem.tag == 'p' and elem.text != None:
                abstract += elem.text

        return abstract

    #Read XML file and collect introduction (Background)
    def parse_section(self, header):
        section = ''

        #Flag indicating if introduction found
        start = False #Search for 'p' section with introduction
        for elem in self.data:

            #If introduction already found, exit loop
            if elem.tag == 'heading' and start:
                break

            elif elem.text == None:
                continue

            #Start of introduction
            elif elem.tag == 'heading' and header in elem.text.lower():
                start = True
            
            #Body of introduction
            elif elem.tag == 'p' and start and re.search('[a-zA-Z0-9]',elem.text):
                for child in elem.iter():
                    if (child.tag in ['sub', 'sup']) and child.text != None and re.search('[a-zA-Z0-9]',child.text):
                        section += '^'+child.text+'*'
                    elif child.text != None and re.search('[a-zA-Z0-9]',child.text):
                        section += child.text
                        if child.text[-1] == '.':
                            section += ' '

                    if child.tail != None and re.search('[a-zA-Z0-9]',child.tail):
                        section += child.tail
            
        return section 
 

    #Read XML file and organizes all citations into two table based on type
    def parse_citations(self):
        #Gets citations from xml file
        nplcit_table = []

        for cit in self.citations.iter('us-citation'):
            if cit[0].tag == 'nplcit' and cit[0][0].text:
                cit_name = cit[0][0].text
                if '“' in cit_name:
                    cit_name = cit_name.split('“')[1]
                if '”' in cit_name:
                    cit_name = cit_name.split('”')[0]
                    nplcit_table.append(cit_name)
                
        return nplcit_table


#function looks for keyword in sections. If keyword encountered, collects the next n sentences
# defined by num_sentences 
def keyword_section(doc, keyword, num_sentences):

    # compiles sentences that contain or surround keyword
    sentences = ''
    
    if doc.abstract:
        abstract = doc.abstract.split('.')
        for s in abstract:
            if keyword in s and s not in sentences:
                num_collected = 0
                index = abstract.index(s)
                while(index < len(abstract) and num_collected < num_sentences):
                    sentences += s
                    num_collected += 1
                    index += 1

    if doc.intro:
        intro = doc.intro.split('.')
        for s in intro:
            if keyword in s and s not in sentences:
                num_collected = 0
                index = intro.index(s)
                while(index < len(intro) and num_collected < num_sentences):
                    sentences += s
                    num_collected += 1
                    index += 1

    if doc.summary:
        summary = doc.summary.split('.')
        for s in summary:
            if keyword in s and s not in sentences:
                num_collected = 0
                index = summary.index(s)
                while(index < len(summary) and num_collected < num_sentences):
                    sentences += s
                    num_collected += 1
                    index += 1
    
    return sentences

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        doc = XMLDoc(filename, title=True, abstract=True, intro=True, citations=True)
        print(doc.title)
        print(doc.abstract)

        # find sentences that surround keyword
        keyword = 'invention'   # keyword
        num_sentences = 2   # number of subsequent sentences to collect
        sentences = keyword_section(doc,keyword,num_sentences)
        
    except:
        print('Usage: python parse_patent.py patent_file.xml')