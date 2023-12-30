from gramatic.global_position.parser import GlobalLocationLexer, GlobalLocationParser

text = 'at the left side of the image there is a dog, and un gato comiendo on top are the sky. texto texto on right are a couch. Random text here. on the top right there is a cat. In the buttom left side are a bed and a bedside table. A monkey in the top of a green tree with apples.'
# text = 'A monkey in top of a green tree with apples.'
# text = 'at the left side of the image there is a dog on a couch.'
text = 'there is a cat sleeping in the left of a dog on a couch at the left.'
# text = 'there is a cat sleeping on a couch at the left.'
lexer = GlobalLocationLexer()
parser = GlobalLocationParser()

parser.parse(lexer.tokenize(text))
for key in parser.subtexts:
    for item in parser.subtexts[key]:
        print(f'- {key}: {item}')
