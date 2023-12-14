from googlelens import GoogleLens

lens = GoogleLens()
search_result = lens.search_by_file("/home/raul/Storage/Computation Sience/Tesis/images_RIS-ML-Conv-NLP/code/features/google_lens/norris.jpg")
print(search_result)