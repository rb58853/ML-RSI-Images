from process import get_keys
from tokens.lexer import CaptionLexer

captions = [
    "Wild animals are standing in a field",
    "A plate of healthy food" ,
    "A woman wearing a hat is walking down a sidewalk",
    "A bird sits near to the water" ,
    "A family standing next to the ocean on a sandy beach with a surf board",
    "A group of people sitting around a table in a restaurant",
    "A mountain range with a clear blue sky",
    "A cat and a dog playing in a park",
    'two cats and a dog sitting on an orange couch. a cartoon dog laying on a pillow. a cartoon cat with a smile on its face. cartoon illustration of a cat and dog lying on a couch cartoon. dog with a blue collar and a brown nose',
    "a cat and dog lying on a couch. cartoon dog with a blue collar and a brown nose. cartoon cat with a tail curled up and eyes closed",
    'a dog eating fruit. two cats playing in the snow.',
    'a big dog and two cats playing in the snow.',
    'two cats and a dog sitting on an orange couch.  a cartoon dog laying on a pillow.  a cartoon cat with a smile on its face'
]

# caption0 = 'a dog eating fruit. two cats playing in the snow.'
# caption1 = 'a big dog and two cats playing in the snow.'
# caption2 = 'two cats and a dog sitting on an orange couch, dog with a blue collar and a brown nose'
caption2='two cats and a dog sitting on an orange couch. a cartoon dog laying on a pillow. a cartoon cat with a smile on its face. cartoon illustration of a cat and dog lying on a couch cartoon. dog with a blue collar and a brown nose'
# caption2='a cartoon cat with a smile on its face.'
caption = "a cat and dog lying on a couch. cartoon dog with a blue collar and a brown nose. cartoon cat with a tail curled up and eyes closed"
# caption = "cartoon cat with a tail curled"# up and eyes closed"
# caption = "cartoon illustration of a cat and dog lying on a couch. cartoon dog with a blue collar and a brown nose. cartoon cat with a tail curled up and eyes closed"
# caption = "cartoon cat with a ball and eyes closed"
# caption = "long tail and eyes closed"
# caption = "cat with a long tail and eyes closed"
# caption = "cartoon cat with a ball"

for caption in captions:
    print(f'########### {caption} ##########')
    for token in get_keys(caption):
        print(token)   
    print(f'#################################################################\n')
