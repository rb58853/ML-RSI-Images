from sly import Lexer
from tokens.utils import is_noun, is_verb, is_num, is_adj

class CaptionLexer(Lexer):
    def __init__(self) -> None:
        super().__init__()

    tokens = {
        WITH, IS, IN, ON, OF, AND, NOUN, VERB, ADJ, NUM
    }

    literals = { ',', '.' }

    keyword = [ 'with', 'and', 'in', 'on', 'of', 'is' ]

    ignore = r' '
    ignore_tab = r'\t'
    ignore_newline = r'\n'

    word = r'[a-zA-Z][a-zA-Z0-9]*'
    
    def word(self, token):
        if token.value.lower()== 'a' or token.value.lower() == 'an':
            token.type = "NUM"
            return token

        if token.value.lower() in self.keyword:
            token.type = token.value.upper()
            return token

        if is_noun(token.value):
            token.type = "NOUN"
            return token
        
        if is_verb(token.value):
            token.type = "VERB"
            return token
        
        if is_num(token.value):
            token.type = "NUM"
            return token
        
        if is_adj(token.value):
            token.type = "ADJ"
            return token

    def error(self, t):
        #ignora lo que considere error
        pass    

  
