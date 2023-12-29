from retrieval_system.data import ImagesDataset

class Retrieval:
    def __init__(self, data_path) -> None:
        self.data = ImagesDataset()
        self.data.load_from_path(data_path)

    def find_from_text(self, text):
        pass

    def soft_ranking(self,text):
        #Ranking en O(n). Organiza primero por embedding de imagen principal contra texto
        pass
    
    def hard_ranking(self, text):
        #tien en cuenta todas los calculos para establecer el ranking
        pass


