from gramatic.global_position.parser import GlobalLocationLexer, GlobalLocationParser

def globals_pos(text):
    lexer = GlobalLocationLexer()
    parser = GlobalLocationParser()
    result = parser.parse(lexer.tokenize(text))
    return parser.subtexts