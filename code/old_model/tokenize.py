from tokenization.process import get_keys

def start(caption):
    return get_keys(caption)

test = start('tom cat is blue and white')
for token in test:
    print (token)