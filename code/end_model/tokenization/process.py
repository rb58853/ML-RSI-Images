from tokenization.gramatic.parser import CaptionLexer,CaptionParser

def get_keys(caption):
    captions = caption.split(".")
    lexer = CaptionLexer()
    parser = CaptionParser()

    #Esto hace shift siempre
    parser.right_precedence()
    for caption in captions:
        parser.parse(lexer.tokenize(caption))
        for i in range(len(caption)):
            if caption[i] == " ":
                parser.parse(lexer.tokenize(caption[i:]))
    
    #Esto reduce siempre a la izquierda, esto sirve cuando hay que reducir por ejemplo:  `adj and adj noun`, aqui ambos adjetivos modifican al sustantivo
    parser.left_precedence()
    for caption in captions:
        parser.parse(lexer.tokenize(caption))
        for i in range(len(caption)):
            if caption[i] == " ":
                parser.parse(lexer.tokenize(caption[i:]))

    return parser.sintagmas            