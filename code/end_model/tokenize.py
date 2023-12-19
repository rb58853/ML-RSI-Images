from tokenization.process import get_keys

def start(caption):
    return get_keys(caption)

test = start('cartoon illustration of a cat and dog lying on a couch.  cartoon dog with a blue collar and a brown nose.  cartoon cat with a tail curled up and eyes closed')
for token in test:
    print (token)