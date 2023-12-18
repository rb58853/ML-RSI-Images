from tokenization.process import get_keys

def start(caption):
    return get_keys(caption)

test = start('a cat laying on a red chair with a remote control')
for token in test:
    print (token)