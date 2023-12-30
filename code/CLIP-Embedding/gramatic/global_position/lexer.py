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
    '''
    `!TOKEN` indica que compara que sea distinto de TOKEN
    '''
    relation = [

                'IS text ON POS !OF',
                'IS text ON POS OF IMAGE',
                'text ON POS !OF',
                'text ON POS OF IMAGE',
                'IS text ON POS POSITION !OF',
                'IS text ON POS POSITION OF IMAGE',
                'text ON POS POSITION !OF',
                'text ON POS POSITION OF IMAGE',
                
                'IS text ON POS POS !OF',
                'IS text ON POS POS OF IMAGE',
                'text ON POS POS !OF',
                'text ON POS POS OF IMAGE',
                'IS text ON POS POS POSITION !OF',
                'IS text ON POS POS POSITION OF IMAGE',
                'text ON POS POS POSITION !OF',
                'text ON POS POS POSITION OF IMAGE',

                

                'ON POS IS WORD',
                'ON POS OF IMAGE IS WORD',
                'ON POS OF IMAGE WORD',
                'ON POS WORD',
                'ON POS POSITION IS WORD',
                'ON POS POSITION OF IMAGE IS WORD',
                'ON POS POSITION OF IMAGE WORD',
                'ON POS POSITION WORD',

                'ON POS POS IS WORD',
                'ON POS POS OF IMAGE IS WORD',
                'ON POS POS OF IMAGE WORD',
                'ON POS POS WORD',
                'ON POS POS POSITION IS WORD',
                'ON POS POS POSITION OF IMAGE IS WORD',
                'ON POS POS POSITION OF IMAGE WORD',
                'ON POS POS POSITION WORD',
                
                'ON POS POS POS IS WORD',
                'ON POS POS POS OF IMAGE IS WORD',
                'ON POS POS POS OF IMAGE WORD',
                'ON POS POS POS WORD',
                'ON POS POS POS POSITION IS WORD',
                'ON POS POS POS POSITION OF IMAGE IS WORD',
                'ON POS POS POS POSITION OF IMAGE WORD',
                'ON POS POS POS POSITION WORD',
                ]
    
    def text_case(sentence, text, i, j, temp):
        #caso especial que hay que tratar
        j+=1
        break_next = False
        while i<len(text):
            i+=1
            if i>=len(text): break

            if break_next:
                i -= 1
                return (True,i)
            
            if text[i] == '.' or text[i] =='|':
                break_next = True


            temp_i = i
            temp_j = j
            temp_temp = [value for value in temp]

            while text[i] == sentence[j] or (sentence[j][0] == '!' and sentence[j][1:] != text[i]):
                if text[i] != 'WORD':
                    temp +=[i]
                
                if j == len(sentence)-1:
                    return (i,j,temp)
                i+=1
                j+=1
                
            #Si llega a aqui no matcheo. Luego hay que buscar otro x donde comience a matchaer
            i = temp_i
            j = temp_j
            temp = temp_temp

        return False    
    
    def match(sentence, text):
        result = []
        i= -1

        while i < len(text)-1:
            i+=1
            temp = []
            j= -1
            while j < len(sentence)-1:
                j+=1
                if sentence[j] == 'text' and len(sentence) > j+1:
                    text_analiced = GramaticalRules.text_case(sentence,text,i,j,temp)
                    if text_analiced == False:
                        return result
                    elif text_analiced[0] == True:
                        i = text_analiced[1]
                        break
                    else:    
                        i,j,temp = text_analiced
                        result += temp
                        break

                if text[i] == sentence[j] or (sentence[j][0] == '!' and sentence[j][1:] != text[i]):
                    if text[i] != 'WORD':
                        temp += [i]
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