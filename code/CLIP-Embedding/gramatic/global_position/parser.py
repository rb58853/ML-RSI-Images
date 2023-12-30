from gramatic.global_position.lexer import GlobalLocationLexer
from sly import Parser

class GlobalLocationParser(Parser):
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
    tokens = GlobalLocationLexer.tokens
    start = 'sentence'  
    precedence = (
        # ('right', 'POS'),
        ('right', 'ON', 'IS', 'OF', 'IMAGE', 'POS', 'POSITION'),
        ('left', ',', '.','|','AND'),
        ('left', 'WORD'),
        )
    
    def __init__(self) -> None:
        super().__init__()
        self.subtexts:dict[str,list] = {}

    def add_subtext(self,text, pos):
        if pos not in self.subtexts:
            self.subtexts[pos]=[text]
        else:
            self.subtexts[pos].append(text)

    def error(self, token):
        pass
    
    @_('relation',
    'relation "|"',
    'relation ","',
    'relation AND',
    'relation "."',
    'sentence sentence',
    )
    def sentence(self, p):
        print(p[0])
        return p[0]
    
    @_('text "."',
       'text')
    def sentence(self, p):
        self.add_subtext(p.text, None)    
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
        
#WORD________________________________________________    
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
        return ' '.join([p[0], p[1]])
    
    @_('text "," text')
    def text(self, p):
        '''`<text> ::= <text> , <text>`'''
        return ' '.join([p[0], p[1], p[2]])


#RIGHT_RELATION____________________________________________
    # <right_relation> ::= ON <pos> IS <text>
    #                     | <pos> IS <text>
    #                     | ON <pos> OF IMAGE IS <text>
    #                     | <pos> <text>
    #                     | <pos> OF IMAGE <text>
    #                     | <right_relation> <text>
    
    @_('ON pos IS text')
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
        return ' '.join([p.ON, p.pos, p.IS, p.text])
    
    @_('ON pos OF IMAGE IS text')
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> OF IMAGE IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
        return ' '.join([p.ON, p.pos, p.OF, p.IMAGE, p.IS, p.text])
    
    #ANALIZAR si en el ingles se usa esto de alguna forma, me parece que no
    @_('ON pos text')
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
        return ' '.join([p.ON, p.pos, p.text])
    
    @_('ON pos OF IMAGE text')
    def right_relation(self, p):
        '''`<right_relation> ::= ON <pos> OF IMAGE IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
    
    @_('pos OF IMAGE IS text')
    def right_relation(self, p):
        '''`<right_relation> ::= <pos> OF IMAGE <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
    
    @_('right_relation text')
    def right_relation(self, p):
        '''`<right_relation> ::= <pos> OF IMAGE <text>`'''
        pos = p.right_relation[1]
        text = p.right_relation[0] + " "+p.text
        self.add_subtext(text,pos)
        return (text, pos)
        return ' '.join([p.right_relation, p.text])

    @_('right_relation "," text')
    def right_relation(self, p):
        '''`<right_relation> ::= <pos> OF IMAGE <text>`'''
        pos = p.right_relation[1]
        text = p.right_relation[0] + ", " + p.text
        self.add_subtext(text,pos)
        return (text, pos)
        return ' '.join([p.right_relation, p.text])

#LEFT RELATION___________________________________________________
    @_('IS text ON pos')
    def left_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
    
    @_('IS text ON pos OF IMAGE')
    def left_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
    
    @_('text ON pos OF IMAGE')
    def left_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
    
    @_('text ON pos')
    def left_relation(self, p):
        '''`<right_relation> ::= ON <pos> IS <text>`'''
        self.add_subtext(p.text,p.pos)
        return (p.text,p.pos)
    
#RELATION
    @_('right_relation',
       'left_relation')
    def relation(self, p):
        return p[0]