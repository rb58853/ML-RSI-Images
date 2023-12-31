from features.features import Text
from gramatic.get import globals_pos

class TextFeature:
    def __init__(self, text:str) -> None:
        self.text:Text = Text(text)
        self.texts:list[Text] = []#[self.text]
        self.analize_text()
        
    def analize_text(self):
        global_texts = globals_pos(self.text.text)
        global_Texts:list[Text] = []        
        for key in global_texts:
            for text in global_texts[key]:
                global_Texts.append(Positions.text_to_Text(key_text=(key,text)))
        raise NotImplementedError("Not Implemented")
    
    def __getitem__(self, index)-> Text:
       return self.texts[index]
    
    def __len__(self):
        return len(self.texts)

class Positions:
    labels={
        "center": 'center',
        "middle": 'center',

        "corner": 'corner',
        
        'left': 'w',

        'right': 'e',

        'top': 'n',
        'up': 'n',
        'over': 'n',

        'bottom': 's',
        'buttom': 's',
        'down': 's',
        'lower': 's',
    }
    global_positions= {
        'e':(0.833, 0.5),
        'w':(0.167, 0.5),
        'n':(0.5, 0.167),
        's':(0.5, 0.833),
        
        'sw':(0.167, 0.833),
        'se':(0.833, 0.833),
        
        'nw':(0.167, 0.167),
        'ne':(0.833, 0.167),
        
        'center':(0.5,0.5),
        
        'nwcenter':(0.333,0.333),
        'necenter':(0.666,0.333),
        'swcenter':(0.333,0.666),
        'secenter':(0.666,0.666),

        'nwcorner':(0,0),
        'necorner':(1,0),
        'swcorner':(0,1),
        'secorner':(1,1),

    }

    def text_to_Text(key_text):
        if key_text[0] is None:
            return Text(key_text[1],None)
                    
        labels = [Positions.labels[pos] for pos in key_text[0].split(" ")]
        if len(labels) == 1:
            return Text(key_text[1],Positions.global_positions[labels[0]])            
        
        label = ''
        if 's' in labels:
            label+='s'
        elif 'n' in labels:    
            label+='n'
        
        if 'e' in labels:
            label+='e'
        elif 'w' in labels:    
            label+='w'
        
        if 'center' in labels:
            label+='center'
        elif 'corner' in labels:    
            label+='corner'    

        return Text(key_text[1],Positions.global_positions[label])            