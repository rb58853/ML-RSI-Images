from features import Text

class TextFeature:
    def __init__(self, text) -> None:
        self.text = text
        self.texts:list[Text] = [self.text]

    def analize_text(self):
        raise NotImplementedError()
