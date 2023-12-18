from tokenization.process import get_keys

def start(caption):
    return get_keys(caption)

test = start('a cat and dog laying on a bed with a knife. a close up of a dog with a long nose')
for token in test:
    print (token)