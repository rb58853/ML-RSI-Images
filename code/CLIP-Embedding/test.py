from gramatic.global_position.parser import GlobalLocationLexer, GlobalLocationParser

text = 'at the left side of the image there is a dog on top are the sky. texto texto on right are a couch. Random text here. on the top right there is a cat. In the buttom left side are a bed and a bdeside table.'
# text = 'a dog on right are a couch.'
# text = 'at the left side of the image there is a dog on a couch.'
lexer = GlobalLocationLexer()
parser = GlobalLocationParser()

parser.parse(lexer.tokenize(text))
for key in parser.subtexts:
    for item in parser.subtexts[key]:
        print(f'- {key}: {item}')
