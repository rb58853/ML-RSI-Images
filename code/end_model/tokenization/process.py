from tokenization.gramatic.parser import CaptionLexer,CaptionParser

def get_keys(caption):
    captions = caption.split(".")
    lexer = CaptionLexer()
    parser = CaptionParser()

    for caption in captions:
        parser.parse(lexer.tokenize(caption))
        for i in range(len(caption)):
            if caption[i] == " ":
                parser.parse(lexer.tokenize(caption[i:]))
    
    return parser.sintagmas            