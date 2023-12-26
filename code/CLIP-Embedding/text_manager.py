from features import Text

class TextFeature:
    def __init__(self, text) -> None:
        self.text:Text = text
        self.texts:list[Text] = []#[self.text]

    def analize_text(self):
        raise NotImplementedError()
    
    def __getitem__(self, index)-> Text:
       return self.texts[index]
    
    def __len__(self):
        return len(self.texts)
   