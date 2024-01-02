from features.features import Text
from gramatic.get import globals_pos, relation_pos

class TextFeature:
    def __init__(self, text:str) -> None:
        self.origin:Text = Text(text)
        self.texts:list[Text] = []#[self.text]
        self.get_parsed_text()
        
    def get_parsed_text(self):
        self.texts = self.analize_text()    
    def analize_text(self):
        global_texts = globals_pos(self.origin.text)
        global_Texts:list[Text] = []        
        for key in global_texts:
            for text in global_texts[key]:
                global_Texts.append(Positions.text_to_Text(key_text=(key,text)))

        end_texts=[]
        for text in global_Texts:
            end_texts += Positions.separe_text(text)

        return end_texts 
    
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
    relational_labels = {
        
        "beside": 'beside',
        "next": 'next',

        "center": 'in',
        "middle": 'in',
        "in": 'in',

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
    
    def separe_text(text:Text):
        texts = relation_pos(text.text)
        return Positions.get_text_from_dict(texts,text.position)        

    def get_text_from_dict(text_dic,position):
        result = []
        
        count_none = 0
        for text_key in text_dic:
            if text_key is not None:
                text = Text(text_key,position)
            else:
                if len(text_dic[text_key][None])>0:
                    result.append(Text(text_dic[text_key][None][count_none],position))
                    count_none+=1
                    continue
                    
            for pos in text_dic[text_key]:
                texts_pos = text_dic[text_key][pos]
                for text_pos in texts_pos:
                    temp = Text(text_pos,position)
                    text.add_neighbord(temp, Positions.combine_labels_for_locals(pos))
                    result.append(text)
        return result        
    
    def combine_labels_for_locals(labels):
        if labels is None:
            return None
        labels = [Positions.relational_labels[label] for label in labels.split(" ")] 
        if len(labels) == 1:
            return labels[0]            
        
        label = ''
        if 's' in labels:
            label+='s'
        elif 'n' in labels:    
            label+='n'
        
        if 'e' in labels:
            label+='e'
        elif 'w' in labels:    
            label+='w'
        
        return label