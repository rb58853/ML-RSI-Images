from gramatic.global_position.parser import GlobalLocationLexer, GlobalLocationParser

text = ' at the left side of the image there is a dog, there are a cat hunting on top of dog. texto texto on right, on right are a couch. Random text, asd qqq. on the top right there is a cat. In the buttom left side are a bed and a bedside table. There is a monkey in the top of a green tree with apples at the top of the image. there is a cat sleeping in the left of a dog on a couch at the left of the photo.'
# text = 'A monkey in top of a green tree with apples.'
# text = 'at the left side of the image there is a dog on a couch.'
# text = 'there is a cat sleeping in the left of a dog on a couch at the left.'
# text = 'at the left side of the image there is a dog j.'
# text = 'are un gato comiendo on top of dog. are texto texto on right .'
# text = 'there is a cat sleeping in the left of a dog on a couch at the left of the photo.'
lexer = GlobalLocationLexer()
parser = GlobalLocationParser()

parser.parse(lexer.tokenize(text))
for key in parser.subtexts:
    for item in parser.subtexts[key]:
        print(f'- {key}: {item}')