import spacy
nlp = spacy.load('en_core_web_lg')

def getkeywords(sentence):
    text = sentence
    doc = nlp(text)
    return (doc.ents)

if __name__ == "__main__":
    text = """spaCy is an open-source software library for advanced natural language processing, 
written in the programming languages Python and Cython."""
    print(getkeywords(text))