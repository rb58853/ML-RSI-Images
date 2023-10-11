import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("a cat sleeping next to a dog eating")

for chunk in doc.noun_chunks:
    print(chunk.text)
