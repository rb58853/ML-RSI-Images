from sly import Parser
from tokenization.tokens.lexer import CaptionLexer

class CaptionParserLeft(Parser):
    tokens = CaptionLexer.tokens
    start = 'text'  
    precedence = (
        ('left', 'IN', 'ON', 'OF', 'NOUN', 'VERB', 'NUM', 'AND', 'WITH',',','ADJ'),
        )
    
    def __init__(self) -> None:
        super().__init__()
        self.sintagmas = []

    def add_token(self,token):
        if token not in self.sintagmas:
            self.sintagmas.append(token)

    def error(self, token):
        
        pass
    
    @_( 'adj',  
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
    
    @_('NUM ADJ noun')
    def noun(self, p):
        phrase =' '.join([p.NUM, p.ADJ, p.noun])
        self.add_token(phrase)
        return phrase
    
    @_('adj noun')
    def nouns(self, p):
        if isinstance(p[0], list):
            result = [' '.join([', '.join(p[0]), p[1]])]

            for adj in p[0]:
                phrase =' '.join([adj, p.noun])
                result.append(phrase)

            for token in result:
                self.add_token(token)
            return result        

        else:
            phrase =' '.join([p.adj, p.noun])
            self.add_token(phrase)
            return [phrase]
    
    @_('noun adj')
    def nouns(self, p):
        if isinstance(p[1], list):
            result = [' '.join([', '.join(p[1]), p[0]])]

            for adj in p[1]:
                phrase =' '.join([adj, p.noun])
                result.append(phrase)

            for token in result:
                self.add_token(token)
            return result        

        else:
            phrase =' '.join([p.adj, p.noun])
            self.add_token(phrase)
            return [phrase]

    @_('NOUN noun')
    def noun(self, p): 
        phrase =' '.join([p[0], p[1]])
        self.add_token(phrase)
        return phrase
    
    # @_('noun IS adj')
    # def noun(self,p):
    #     phrase = ' '.join([p.ADJ, p.noun])
    #     self.add_token(phrase)
    #     return phrase
    
    # @_('noun IS NOUN')
    # def noun(self,p):
    #     phrase = ' '.join([p[2], p[0]])
    #     self.add_token(phrase)
    #     return phrase
    
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
    
    @_('NUM ADJ')
    def adj(self,p):
        #ADJ
        return ' '.join([p[0],p[1]])

    @_('ADJ')
    def adj(self,p):
        #ADJ
        return p[0]
    
    @_('noun AND adj')
    def adj(self,p):
        #beauty and black
        if  isinstance(p[2],list):
            return [p[0]]+p[2]
        if not isinstance(p[2],list): 
            return [p[0]]+[p[2]]

    @_('adj AND adj')
    def adj(self,p):
        #beauty and tall
        if isinstance(p[0],list) and isinstance(p[2],list): 
            return p[0]+p[2]
        if isinstance(p[0],list) and not isinstance(p[2],list): 
            return p[0]+[p[2]]
        if not isinstance(p[0],list) and isinstance(p[2],list): 
            return [p[0]]+p[2]
        if not isinstance(p[0],list) and not isinstance(p[2],list): 
            return [p[0]]+[p[2]]
    
    @_('adj "," adj')
    def adj(self,p):
        #beauty, tall
        if isinstance(p[0],list) and isinstance(p[2],list): 
            return p[0]+p[2]
        if not isinstance(p[0],list) and isinstance(p[2],list): 
            return [p[0]]+p[2]
        if isinstance(p[0],list) and not isinstance(p[2],list): 
            return p[0]+[p[2]]
        if not isinstance(p[0],list) and not isinstance(p[2],list): 
            return [p[0]]+[p[2]]
    
#endregion
    @_('nouns VERB')
    def verbal_list(self, p): 
        result = []
        nouns: str = p.nouns
        for noun in nouns:
            result.append(' '.join([noun, p.VERB]))
            self.add_token(' '.join([noun, p.VERB]))
        return result
    
    @_('verbal AND verbal')
    def verbal_list(self, p): 
        return [p[0],p[2]]
    @_('verbal "," verbal')
    def verbal_list(self, p): 
        return [p[0],p[2]]
    
    @_('verbal "," verbal_list')
    def verbal_list(self, p): 
        return [p[0]]+p[2]
    
    @_('verbal AND verbal_list')
    def verbal_list(self, p): 
        return [p[0]]+p[2]
    
    # @_('noun IS VERB')
    # def verbal(self, p): 
    #     phrase = ' '.join([p[0], p[2]])
    #     self.add_token(phrase)
    #     return phrase    

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
    
    @_('noun on nouns')
    def nominal(self, p): 
        result = []
        for noun in p[2]:
            phrase = ' '.join([p[0], p[1], noun])
            result.append(phrase)

        for token in result:    
            self.add_token(token)
        
        return result
    
    @_('nouns on nouns')
    def nominal(self, p): 
        result = []
        for noun1 in p[0]:
            for noun2 in p[2]:
                phrase = ' '.join([noun1, p[1], noun2])
                result.append(phrase)
        for token in result:    
            self.add_token(token)
        return result
    
    @_('verbal on adj noun')
    def nominal(self, p): 
        phrase = ' '.join([p[0], p[1], p.noun])
        self.add_token(phrase)
        return phrase
    
    @_('verbal on nouns')
    def nominal(self, p): 
        result = []
        for noun in p[2]:
            phrase = ' '.join([p[0], p[1], noun])
            result.append(phrase)

        for token in result:    
            self.add_token(token)
        
        return result
    
    @_('verbal_list on nouns')
    def nominal(self, p): 
        result = []
        for verbal in p[0]:
            for noun in p[2]:
                phrase = ' '.join([verbal, p[1], noun])
                result.append(phrase)
        for token in result:    
            self.add_token(token)
        return result

    # @_('noun IS on noun')
    # def nominal(self,p):
    #     phrase = ' '.join([p[0], p[2], p[3]])
    #     self.add_token(phrase)
    #     return phrase
   
    @_('verbal on noun')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase
    
    @_('nouns on noun')
    def nominal_list(self, p):
        result = []
        nouns: list = p.nouns
        for noun in nouns:
            result.append(' '.join( [noun, p[1], p[2]]))
            self.add_token(' '.join([noun, p[1], p[2]]))
        return result

    # @_('nouns IS on noun')
    # def nominal_list(self, p):
    #     result = []
    #     nouns: list = p.nouns
    #     for noun in nouns:
    #         result.append(' '.join( [noun, p[2], p[3]]))
    #         self.add_token(' '.join([noun, p[2], p[3]]))
    #     return result

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
    
    @_('noun WITH nominal')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase
    
    @_('noun WITH verbal')
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
    
    @_('noun WITH verbal_list')
    def sintagma(self, p): 
        result = []
        verbals: list = p.verbal_list
        for verbal in verbals:
            result.append(' '.join([p[0], p[1], verbal]))
            self.add_token(' '.join([p[0], p[1], verbal]))
        return result
    
    @_('nouns WITH verbal_list')
    def sintagma(self, p): 
        result = []
        verbals: list = p.verbal_list
        for verbal in verbals:
            result.append(' '.join([p[0], p[1], verbal]))
            self.add_token(' '.join([p[0], p[1], verbal]))
        return result

    @_('noun OF noun')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase
    
    @_('sintagma AND sintagma')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1], p[2]])
        self.add_token(phrase)
        return phrase

    @_('verbal noun')
    def sintagma(self, p): 
        phrase = ' '.join([p[0], p[1]])
        self.add_token(phrase)
        return phrase   
    
    @_('verbal_list on noun WITH noun')
    def sintagma_list(self, p):
        # verbal_list on noun es tambien un sintagma, cuando pasa por aqui no parsea el sintagma, luego hay que agregar ese token desde aqui
        result = []
        verbals: list = p.verbal_list
        for verbal in verbals:
            result.append(' '.join([verbal, p[1], p[2]]))
            result.append(' '.join([verbal, p[1], p[2],'with', p[4] ]))
            result.append(' '.join([verbal,'with', p[4] ]))
            noun = " ".join(verbal.split(" ")[:-1])
            result.append(' '.join([noun,'with', p[4] ]))
        for token in result:
            self.add_token(token)
        return result
    
    @_('verbal on noun WITH noun')
    def sintagma_list(self, p):
        # verbal on noun es tambien un sintagma, cuando pasa por aqui no parsea el sintagma, luego hay que agregar ese token desde aqui
        result = []
        verbal: list = p.verbal
        result.append(' '.join([verbal, p[1], p[2]]))
        result.append(' '.join([verbal, p[1], p[2],'with', p[4] ]))
        result.append(' '.join([verbal,'with', p[4] ]))
        noun = " ".join(verbal.split(" ")[:-1])
        result.append(' '.join([noun,'with', p[4] ]))
        for token in result:
            self.add_token(token)
        return result
