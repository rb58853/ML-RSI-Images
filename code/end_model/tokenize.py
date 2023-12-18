from tokenization.process import get_keys

def start(caption):
    return get_keys(caption)

test = start('singapore merlion fountain.  singapores marina bay sands is the worlds tallest building.  singapore merlion fountain at sunset')
for token in test:
    print (token)