from features import Text

class TextFeature:
    def __init__(self, text:str) -> None:
        self.text:Text = Text(text)
        self.texts:list[Text] = []#[self.text]

    def analize_text(self):
        raise NotImplementedError()
    
    def __getitem__(self, index)-> Text:
       return self.texts[index]
    
    def __len__(self):
        return len(self.texts)
   