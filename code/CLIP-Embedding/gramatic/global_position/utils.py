import spacy
nlp = spacy.load('en_core_web_sm')
def tokenize(text):
    doc = nlp(text)
    return {token.text:token.pos_ for token in doc}
