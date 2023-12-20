from tokenization.process import get_keys

def start(caption):
    return get_keys(caption)

test = start(' a gray and white kitten is walking on a bed')
for token in test:
    print (token)