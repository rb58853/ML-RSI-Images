from gramatic.parser import CaptionLexer,CaptionParser

caption0 = 'a dog eating fruit two cats playing in the snow.'
caption1 = 'a tall dog and two cats playing in the snow.'
caption2 = 'two cats and a dog sitting on an orange couch, dog with a blue collar and a brown nose'
# caption2='two cats and a dog sitting on an orange couch, a cartoon dog laying on a pillow, a cartoon cat with a smile on its face, cartoon illustration of a cat and dog lying on a couch cartoon, dog with a blue collar and a brown nose'

lexer = CaptionLexer()
parser = CaptionParser()

parser.parse(lexer.tokenize(caption2)) 
for t in parser.sintagmas:
    print(t)   