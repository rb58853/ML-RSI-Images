from gramatic.global_position.parser import GlobalLocationLexer, GlobalLocationParser

text = 'A cat and a dog playing.\
    at the left side of the image there is a dog, there are a cat hunting on top of dog.\
    texto texto on right, on right are a couch.\
    Random text, asd qqq. \
    on the top right there is a lamp.\
    In the buttom left side are a bed and a bedside table. \
    There is a monkey in the top of a green tree with apples at the top right of the image.\
    there is a cat sleeping in the left of a dog on a couch at the left of the photo, is a gray cat.\
    there is a cat roaring on a table at the left of the photo, a lion playing on the buttom.'

# text = 'A cat , on the left side of the image are a dog playing.'
# text = 'there is a cat roaring on a table at the left of the photo, is a gray cat on the right of photo.'

lexer = GlobalLocationLexer()
parser = GlobalLocationParser()

result = parser.parse(lexer.tokenize(text))
print(result)
for key in parser.subtexts:
    for item in parser.subtexts[key]:
        print(f'- {key}: {item}')