from gramatic.object_relation_pos.lexer import PosRelationLexer
from sly import Parser

class PosRelationParser(Parser):
    '''
    ## <pos>
    `<pos> ::= pos`\n
    \t\t`| num, num`\n
    \t\t`| num num`\n
    \t\t`| <pos> <pos>`\n
    \t\t`| <pos>, <pos>`\n
    \t\t`| <pos> POSITION`\n
    \t\t`| (<pos>)`\n
    \t\t`| [<pos>]`\n

    ## <text>
    `<text> ::= WORD`\n
    \t\t`| WORD ","`\n
    \t\t`| <text> <text>`\n

    ## <right_relation>
    `<right_relation> ::= ON <pos> IS <text>`\n
    \t\t\t\t\t`| <pos> IS <text>`\n
    \t\t\t\t\t`| ON <pos> OF IMAGE IS <text>`\n
    \t\t\t\t\t`| <pos> <text>`\n
    \t\t\t\t\t`| <pos> OF IMAGE <text>`\n
    \t\t\t\t\t`| <right_relation> <text>`\n

    ## <middle_relation>
    `<middle_relation> ::= IS <text> ON <pos>`\n
    \t\t\t\t\t`| IS <text> <pos>`\n
    \t\t\t\t\t`| IS <text> ON <pos> OF IMAGE `\n
    
    ## <left_relation>
    `<left_relation> ::= <text> ON <pos>`\n
    \t\t\t\t\t`| <text> ON <pos> OF IMAGE`\n
    \t\t\t\t\t`| <text> <left_relation>`\n

    ## precedence
        `('right', 'WORD')`\n
        `('left', '","', '"."', 'AND')`\n
        # `('left', 'ON', 'IS')`\n
    
    '''
    tokens = PosRelationLexer.tokens
    start = 'sentence'  
    # start = 'sentence'  
    precedence = (
        # ('right', 'POS'),
        ('right', 'ON', 'IS', 'OF', 'POS', 'POSITION', 'TO'),
        # ('right', ',', '.','|','AND','WORD'),
        ('left', ',', '.','|','AND','WORD'),
        )
    
    def __init__(self) -> None:
        super().__init__()
        self.subtexts:dict[str,dict] = {}

    def add_subtext(self,text_key, pos, text):
        if text_key not in self.subtexts:
            self.subtexts[text_key]={pos:[text]}
        
        if pos not in self.subtexts[text_key]:
            self.subtexts[pos]=[text]
        else:
            if not text in self.subtexts[text_key][pos]:
                self.subtexts[text_key][pos].append(text)

    def error(self, token):
        pass
    
    @_( 
        'sentence sentence',
        'sentence "|" sentence',
        'sentence "." sentence',
        'sentence "," sentence',
        'sentence ";" sentence',
    )
    def sentence (self,p):
        if isinstance(p.sentence0,list): sentence0 = p.sentence0 
        else: sentence0= [p.sentence0]
        if isinstance(p.sentence1,list): sentence1 = p.sentence1
        else: sentence1= [p.sentence1]
        return sentence0 + sentence1
     
    
    @_(
        'relation',
        'relation ","',
    )
    def sentence(self, p):
        return p[0]
    
    @_('text',
        'text ","',
        # '"," text',
    #    'text "."',
    #    'text "|"',
       )
    def sentence(self, p):
        self.add_subtext( None, None,p.text)    
        return p[0]
#POS___________________________________________________
    #<pos> ::=
    #|num num
    #|num num
    #|<pos> <pos>
    #|<pos>, <pos>
    #|(<pos>)
    #|[<pos>]
    
    @_('POS')
    def pos(self, p):
        '''`<pos> ::= POS`'''
        return p.POS    
    
    @_('pos pos')
    def pos(self, p):
        '''`<pos> ::= pos pos`'''
        return ' '.join([p[0], p[1]])
    
    @_('POS POSITION')
    def pos(self, p):
        '''`<pos> ::= POS`'''
        return p.POS
        return ' '.join([p[0], p[1]])
        
#WORD________________________________________________    
    # @_('WORD','","')
    @_('WORD')
    def word(self, p):
        return p[0]
    
#TEXT________________________________________________    
    @_('word')
    def text(self, p):
        '''`<text> ::= WORD`'''
        return p.word

    @_('text text')
    def text(self, p):
        '''`<text> ::= <text> <text>`'''
        text = ' '.join([p[0], p[1]])
        return ' '.join([p[0], p[1]])
    
#RIGHT_RELATION____________________________________________
    
    @_('ON text pos IS text',
       'ON text pos "," IS text',
       'ON text pos "," text'
       )
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text0,p.pos, p.text1)
        return (p.text0,p.pos, p.text1)
    
    @_('ON pos OF text IS text',
       'ON pos OF text "," IS text',
       'ON pos OF text "," text',
       'TO pos OF text IS text',
       'TO pos OF text "," IS text',
       'TO pos OF text "," text',
       
       'ON pos TO text IS text',
       'ON pos TO text "," IS text',
       'ON pos TO text "," text',
       'TO pos TO text IS text',
       'TO pos TO text "," IS text',
       'TO pos TO text "," text',
       
       'pos TO text IS text',
       'pos TO text "," IS text',
       'pos TO text "," text',
       
       'pos OF text IS text',
       'pos OF text "," IS text',
       'pos OF text "," text',
       )
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> OF IMAGE IS <text>`'''
        self.add_subtext(p.text0,p.pos, p.text1)
        return (p.text0,p.pos, p.text1)
    
    @_( 'NEXT TO text IS text',
        'NEXT TO text "," text',
        'NEXT OF text IS text',
        'NEXT OF text "," text',
       )
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> OF IMAGE IS <text>`'''
        self.add_subtext(p.text0,'next', p.text1)
        return (p.text0,'next', p.text1)
    
    @_('right_relation "," text')
    def right_relation(self, p):
        '''`<right_relation> ::= <pos> OF IMAGE <text>`'''
        pos = p.right_relation[1]
        text = p.right_relation[0] + " "+p.text
        self.add_subtext(text,pos)
        return (text, pos)

#LEFT RELATION___________________________________________________
    @_('IS text ON pos OF text',
       'text ON pos OF text',
    #    'IS text "," ON pos OF text',
    #    'text "," ON pos OF text',
       'IS text TO pos OF text',
    #    'IS text "," TO pos OF text',
    #    'text "," TO pos OF text',
       
       'IS text ON pos TO text',
    #    'IS text "," ON pos TO text',
    #    'text "," ON pos TO text',
       'text ON pos TO text',
       'IS text TO pos TO text',
    #    'IS text "," TO pos TO text',
    #    'text "," TO pos TO text',
       
       'IS text pos TO text',
       'text pos TO text',
    #    'IS text "," pos TO text',
    #    'text "," pos TO text',

       'IS text pos OF text',
       'text pos OF text',
    #    'IS text "," pos OF text',
    #    'text "," pos OF text',
       )
    def left_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text1,p.pos,p.text0)
        return (p.text1,p.pos,p.text0)
    
    @_( 'IS text NEXT TO text',
        'text NEXT TO text',
        'text "," NEXT TO text',
        
        'IS text NEXT OF text',
        'text NEXT OF text',
        'text "," NEXT OF text',
       )
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> OF IMAGE IS <text>`'''
        self.add_subtext(p.text0,'next', p.text1)
        return (p.text0,'next', p.text1)
   
#RELATION
    @_('right_relation',
       'left_relation')
    def relation(self, p):
        return p[0]
    
    @_('relation "," sentence',
       'sentence "," relation',
       )
    def relation(self,p):
        if isinstance(p.sentence, str):
            pos = p.relation[1]
            text_key = p.relation[0]
            text = p.relation[2] + ", " +p.sentence
            
            self.add_subtext(text_key,pos,text)
            self.subtexts[None][None].remove(p.sentence)
            self.subtexts[text_key][pos].remove(text)
            return (text_key,pos,text)
        
        return (text_key,pos,text)
        return[p.sentence, p.relation]
    
    @_('relation sentence',
       'sentence relation',
       )
    def relation(self,p):
        if isinstance(p.sentence, str):
            pos = p.relation[1]
            text_key = p.relation[0]
            text = p.relation[2] + p.sentence
            
            self.add_subtext(text_key,pos,text)
            self.subtexts[None][None].remove(p.sentence)
            self.subtexts[text_key][pos].remove(text)
            return (text_key,pos,text)
         
        return (text_key,pos,text)
        return[p.sentence, p.relation]
