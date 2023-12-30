from sly import Lexer


class GlobalLocationLexer(Lexer):
    def __init__(self) -> None:
        super().__init__()
        self.category:dict[str:str] = {}
        self.ignores = [r' ', r'\t', r'\n', 'there', 'the']
        self.my_tokens = []
        self.is_token_not_word = []
        self.count = -1

    tokens = {
        ON, OF, AND, IS, POS, POSITION, IMAGE, WORD,  NUM,
    }

    literals = { ',', '.', '|'}

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

        self.count+=1
        if len(self.my_tokens) > 0:
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
    
    def NUM(self,token):
        self.count +=1
        return token
    
    def error(self, t):
        #ignora lo que considere error
        pass    

    def tokenize(self, text, lineno=1, index=0):
        if self.my_tokens == []:        
            self.my_tokens = [token.type for token in super().tokenize(text)]
            self.is_token_not_word = GramaticalRules.get_tokens(self.my_tokens)
        self.count = -1    
        return super().tokenize(text, lineno, index)

class GramaticalRules:
    relation = [
                'ON POS IS',
                'ON POS OF IMAGE IS',
                'ON POS OF IMAGE',
                'ON POS',
                'ON POS POSITION IS',
                'ON POS POSITION OF IMAGE IS',
                'ON POS POSITION OF IMAGE',
                'ON POS POSITION',

                'ON POS POS IS',
                'ON POS POS OF IMAGE IS',
                'ON POS POS OF IMAGE',
                'ON POS POS',
                'ON POS POS POSITION IS',
                'ON POS POS POSITION OF IMAGE IS',
                'ON POS POS POSITION OF IMAGE',
                'ON POS POS POSITION',
                
                'ON POS POS POS IS',
                'ON POS POS POS OF IMAGE IS',
                'ON POS POS POS OF IMAGE',
                'ON POS POS POS',
                'ON POS POS POS POSITION IS',
                'ON POS POS POS POSITION OF IMAGE IS',
                'ON POS POS POS POSITION OF IMAGE',
                'ON POS POS POS POSITION',
                ]
    
    def match(sentence, text):
        result = []
        for i in range(len(text)):
            temp = []
            for j in range(len(sentence)):
                if text[i] == sentence[j]:
                    temp +=[i]
                    i+=1
                else:
                    break
                if j == len(sentence)-1:
                    result += temp
        return result

    def get_tokens(text):
        result = [False]*len(text)
        for sentence in GramaticalRules.relation:
            indexs = GramaticalRules.match(sentence.split(" "),text)
            for index in indexs:
                result[index] = True
        return result