from sly import Lexer


class GlobalLocationLexer(Lexer):
    def __init__(self) -> None:
        super().__init__()
        self.category:dict[str:str] = {}
        self.ignores = [r' ', r'\t', r'\n', 'there', 'the']

    tokens = {
        ON, OF, AND, IS, POS, POSITION, IMAGE, WORD,  NUM,
    }

    literals = { ',', '.'}

    keywords = {
        'on': ['in', 'on', 'at', 'near', 'to'],
        'of': ['of'],
        'and' : ['and'],
        'is': ['is', 'are', "there's", 'find'],
        'pos': ['left', 'right', "buttom","top","down","up","lower","center","middle"],
        'position': ['position', 'pos', "side","location"],
        'image': ['image', 'picture', 'photo'],

        }
    
    ignore = r' '
    ignore_tab = r'\t'
    ignore_newline = r'\n'
    
    word = r'[a-zA-Z][a-zA-Z0-9]*'
    NUM = r'\d+'
    # NUM = r'[0-9]*[.][0-9]*'

    def word(self, token):
        if token.value.lower() in self.ignores:
            self.index = token.end
            return
        
        for key in self.keywords:
            if token.value.lower() in self.keywords[key]:
                token.type = key.upper()
                return token

        token.type = "WORD"
        return token

    def error(self, t):
        #ignora lo que considere error
        pass    