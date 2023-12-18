from tokenization.process import get_keys

def start(caption):
    return get_keys(caption)

test = start('a small dog sitting on a black and white pillow')
for token in test:
    print (token)