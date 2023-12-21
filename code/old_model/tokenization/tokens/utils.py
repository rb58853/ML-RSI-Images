import spacy
nlp = spacy.load('en_core_web_sm')

def is_noun(text):
    doc = nlp(text)
    return doc[0].pos_ == 'NOUN' or doc[0].pos_ == 'PROPN'

def is_verb(text):
    doc = nlp(text)
    return doc[0].pos_ == 'VERB'

def is_num(text):
    doc = nlp(text)
    return doc[0].pos_ == 'NUM'

def is_adj(text):
    doc = nlp(text)
    return doc[0].pos_ == 'ADJ'

def tokenize(text):
    doc = nlp(text)
    return {token.text:token.pos_ for token in doc}

# test = 'a black and white pillow'
# tokens = tokenize(test)
# for token in tokens:
#     print(f'{token}:{tokens[token]}')