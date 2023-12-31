from gramatic.global_position.parser import GlobalLocationLexer, GlobalLocationParser
from gramatic.object_relation_pos.parser import PosRelationLexer, PosRelationParser

def globals_pos(text):
    lexer = GlobalLocationLexer()
    parser = GlobalLocationParser()
    result = parser.parse(lexer.tokenize(text))
    return parser.subtexts

def relation_pos(text):
    lexer = PosRelationLexer()
    parser = PosRelationParser()
    result = parser.parse(lexer.tokenize(text))
    return parser.subtexts