from tokenization.gramatic.parser import CaptionLexer,CaptionParser
from tokenization.gramatic.parser_left import CaptionParserLeft

def get_keys(caption):
    caption = caption.replace(' is ', ' ').replace(' Is ', ' ')
    captions = caption.split(".")
    lexer = CaptionLexer()
    parser_right = CaptionParser()
    parser_left = CaptionParserLeft()

    #Esto reduce siempre a la izquierda, esto sirve cuando hay que reducir por ejemplo:  `adj and adj noun`, aqui ambos adjetivos modifican al sustantivo
    for caption in captions:
        parser_right.parse(lexer.tokenize(caption))
        for i in range(len(caption)):
            if caption[i] == " ":
                parser_right.parse(lexer.tokenize(caption[i+1:]))
    
    #Esto reduce siempre a la izquierda, esto sirve cuando hay que reducir por ejemplo:  `adj and adj noun`, aqui ambos adjetivos modifican al sustantivo
    parser_left.sintagmas = parser_right.sintagmas
    for caption in captions:
        parser_left.parse(lexer.tokenize(caption))
        for i in range(len(caption)):
            if caption[i] == " ":
                parser_left.parse(lexer.tokenize(caption[i+1:]))

    return parser_left.sintagmas