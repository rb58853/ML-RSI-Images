from sly import Lexer
from tokens.utils import is_noun, is_verb, is_num, is_adj, tokenize

class CaptionLexer(Lexer):
    def __init__(self) -> None:
        super().__init__()
        self.category:dict[str:str] = {}

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

        if self.category[token.value] == "NOUN":
            token.type = "NOUN"
            return token
        
        if self.category[token.value] == "VERB":
            token.type = "VERB"
            return token
        
        if self.category[token.value] == "NUM":
            token.type = "NUM"
            return token
        
        if self.category[token.value] == "ADJ":
            token.type = "ADJ"
            return token

    def error(self, t):
        #ignora lo que considere error
        pass    

    def tokenize(self, text, lineno=1, index=0):
        tokens = tokenize(text)
        for value, key in zip(tokens.values(), tokens.keys()):
            self.category[key] = value
            
        return super().tokenize(text, lineno, index)
  
