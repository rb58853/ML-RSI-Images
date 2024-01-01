from sly import Lexer
from gramatic.gramatical_rules.gramatic import Gramatic

class GlobalLocationLexer(Lexer):
    def __init__(self) -> None:
        super().__init__()
        self.category:dict[str:str] = {}
        self.ignores = [r' ', r'\t', r'\n', 'there', 'the']
        self.my_tokens = []
        self.is_token_not_word = []
        self.count = -1
        self.is_tokenized = False

    tokens = {
        ON, OF, AND, IS, POS, POSITION, IMAGE, WORD,  NUM,
    }

    literals = { '.', '|', ';'}

    keywords = {
        'on': ['in', 'on', 'at', 'near', 'to','find'],
        'of': ['of'],
        'and' : ['and'],
        'is': ['is', 'are', "there's", 'find'],
        'pos': ['left', 'right', "buttom", "bottom","top","down","up","lower","center","middle","corner"],
        'position': ['position', 'pos', "side","location"],
        'image': ['image', 'picture', 'photo'],
        'near':['next', 'near']
        }
    
    ignore = r' '
    ignore_tab = r'\t'
    ignore_newline = r'\n'
    
    word = r"[a-zA-Z'][a-zA-Z0-9']*"
    NUM = r'\d+'
    COMA = ','
    # NUM = r'[0-9]*[.][0-9]*'

    def word(self, token):
        if token.value.lower() in self.ignores:
            self.index = token.end
            return

        self.count+=1
        if self.is_tokenized:
            while self.my_tokens[self.count] in self.literals:
                self.count +=1
            if not self.is_token_not_word[self.count]:
                token.type = "WORD"
                return token         

        for key in self.keywords:
            if token.value.lower() in self.keywords[key]:
                token.type = key.upper()
                return token

        token.type = "WORD"
        return token
    
    
    def COMA(self, token):
        token.type = ','
        self.count+=1
        if self.is_tokenized:
            while self.my_tokens[self.count] in self.literals:
                self.count +=1
            if not self.is_token_not_word[self.count]:
                token.type = "WORD"
        return token         

    def NUM(self,token):
        self.count +=1
        if self.is_tokenized:
            while self.my_tokens[self.count] in self.literals:
                self.count +=1
            if not self.is_token_not_word[self.count]:
                token.type = "WORD"
        return token
    
    def error(self, t):
        #ignora lo que considere error
        pass    

    def tokenize(self, text, lineno=1, index=0):
        self.is_tokenized = False
        self.my_tokens = [token.type for token in super().tokenize(text)]
        self.is_token_not_word = GramaticalRules().get_tokens(self.my_tokens)
        self.is_tokenized = True
        self.count = -1    
        return super().tokenize(text, lineno, index)

class GramaticalRules(Gramatic):
    '''
    `!TOKEN` indica que compara que sea distinto de TOKEN
    '''
    use_preference = True #si ya se esta usando un token como token de posicion entonces no usar otros tokens con relacion a este ditinto de la relacion original, ergo segun el orden de las `relation`, si hay ambiguedad usa el primero, puede quedar ambiguo igual, pero menos
    relation = [
                'ON pos IS WORD',
                'ON pos OF IMAGE IS WORD',
                'ON pos OF IMAGE IS WORD',
                # 'ON pos OF IMAGE WORD',
                'ON pos WORD',
                
                'IS text ON pos OF IMAGE',
                'IS text ON pos ,',
                'IS text ON pos !OF',
                'text ON pos ,',
                'text ON pos !OF',
                'text ON pos OF IMAGE',

                'ON pos , IS WORD',
                'ON pos OF IMAGE , IS WORD',
                'ON pos OF IMAGE , WORD',
                'ON pos , WORD',
                ]
    def __init__(self, relation=None) -> None:
        super().__init__(relation)
        self.relation = GramaticalRules.relation
        self.relation_coma()
        self.coma_relation()
        
    