from sly import Parser
from tokens.lexer import CaptionLexer

class CaptionParser(Parser):
    tokens = CaptionLexer.tokens
    start = 'text'  
    precedence = (
        ('nonassoc',  'WITH', 'IS', 'IN', 'ON', 'OF', 'AND', 'NOUN', 'VERB', 'ADJ', 'NUM'),
        ('left',  ',')
        # ('left',  '.')
        )

    def __init__(self) -> None:
        super().__init__()
        self.sintagmas = []

    def add_token(self,token):
        self.sintagmas.append(token)

    def error(self, token):
        
        pass
    
    @_(   
        'noun',
        'nouns',
        'verbal',
        'verbal_list',
        'nominal', 
        'sintagma ',
        'sintagma_list',
        'text "."',
        'text ","',
        'text AND',
        'text text'
       )
    def text(self, p):
        pass

    @_('IN')
    def on(self, p): 
        return p.IN
    
    @_('ON')
    def on(self, p): 
        return p.ON

#region ############## noun ##################
    @_('NOUN')
    def noun(self, p): 
        phrase = p.NOUN
        self.add_token(phrase)
        return phrase 
    
    @_('NUM noun')
    def noun(self, p): 
        phrase = ' '.join([p.NUM, p.noun])
        # self.add_token(phrase)
        return phrase
    
    @_('ADJ noun')
    def noun(self, p): 
        phrase =' '.join([p.ADJ, p.noun])
        self.add_token(phrase)
        return phrase
    
    @_('NOUN noun')
    def noun(self, p): 
        phrase =' '.join([p[0], p[1]])
        self.add_token(phrase)
        return phrase
    
    @_('noun IS ADJ')
    def noun(self,p):
        phrase = ' '.join([p.ADJ, p.noun])
        self.add_token(phrase)
        return phrase
    
    @_('noun IS NOUN')
    def noun(self,p):
        phrase = ' '.join([p[2], p[0]])
        self.add_token(phrase)
        return phrase
    
    @_('noun "," noun')
    def nouns(self,p):
        return [p[0],p[2]]
    
    @_('noun AND noun')
    def nouns(self,p):
        return [p[0],p[2]]
    
    @_('noun "," nouns')
    def nouns(self,p):
        return [p[0]]+p[2]
    
    @_('noun AND nouns')
    def nouns(self,p):
        return [p[0]]+p[2]
    
#endregion
    @_('nouns VERB')
    def verbal_list(self, p): 
        result = []
        nouns: str = p.nouns
        for noun in nouns:
            result.append(' '.join([noun, p.VERB]))
            self.add_token(' '.join([noun, p.VERB]))
        return result
    
    @_('noun VERB')
    def verbal(self, p): 
        phrase = ' '.join([p[0], p[1]])
        self.add_token(phrase)
        return phrase    

    @_('noun on noun')
    def nominal(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase
    
    @_('noun IS on noun')
    def nominal(self,p):
        phrase = ' '.join([p[0], p[2], p[3]])
        self.add_token(phrase)
        return phrase
   
    @_('verbal on noun')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase
    
    @_('verbal_list on noun')
    def sintagma_list(self, p):
        result = []
        verbals: list = p.verbal_list
        for verbal in verbals:
            result.append(' '.join([verbal, p[1], p[2]]))
            self.add_token(' '.join([verbal, p[1], p[2]]))
        return result

    @_('noun WITH noun')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase
    
    @_('noun WITH nouns')
    def sintagma(self, p):
        result = []
        nouns: list = p.nouns
        for noun in nouns:
            result.append(' '.join([p[0], p[1], noun]))
            self.add_token(' '.join([p[0], p[1], noun]))
        return result
    
    @_('noun OF noun')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase

    @_('verbal noun')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1]])
        self.add_token(phrase)
        return phrase   