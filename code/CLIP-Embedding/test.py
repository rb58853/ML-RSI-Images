from gramatic.global_position.parser import GlobalLocationLexer, GlobalLocationParser

text = 'on the left side of the image there is a dog. texto random en medio. on the left there is a cat.'
lexer = GlobalLocationLexer()
parser = GlobalLocationParser()

parser.parse(lexer.tokenize(text))

for key in parser.subtexts:
    print(key)
    for item in parser.subtexts[key]:
        print(item)
