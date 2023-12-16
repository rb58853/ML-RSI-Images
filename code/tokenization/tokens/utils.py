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
    # for token in doc:
    #     token[token.text] = token.pos_
    #     # print (f'{token.text} ({token.pos_ })')


tokenize('a cat with a tail and eyes closed')
# print(is_noun('dog'))
# print(is_noun('tall'))
# print(is_verb('eat'))
# print(is_verb('sleeping'))
# print(is_verb('cat'))