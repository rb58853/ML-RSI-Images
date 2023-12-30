from gramatic.get import globals_pos, GlobalLocationLexer

texts = [ 
'A cat and a dog playing. at the left side of the image there is a dog, there are a cat hunting on top of dog.texto texto on right, on right are a couch. Random text, asd qqq. on the top right there is a lamp.In the buttom left side are a bed and a bedside table.There is a monkey in the top of a green tree with apples at the top right of the image.there is a cat sleeping in the left of a dog on a couch at the left of the photo, is a gray cat. there is a cat roaring on a table at the left of the photo, a lion playing on the buttom.',

"In the top left corner of the image, there is a red apple. Next to the apple, there is a book. Below the book, there is a blue pen lying on its side. On the right side of the image, there is a white wall. In the middle of the image, there is a glass of water. Below the glass, there is a green leaf.",

"At the bottom of the image, there is a black car parked on the street. Beside the car, there is a traffic light. In front of the car, there is a sign indicating 'No Parking'. Beyond the car, there is a row of houses. On the right side of the image, there is a blue sky. In the middle of the image, there is a yellow bird perched on a branch. Above the bird, there is a blue flower.",

"In the top right corner of the image, there is a yellow sun. Below the sun, there is a clear blue sky. On the left side of the image, there is a tall tree. In the middle of the image, there is a group of people sitting on a bench. One person is reading a newspaper. Another person is eating an ice cream cone. At the bottom left corner of the image, there is a small dog running across the grass.",

"In the middle of the image, there is a large painting hanging on the wall. Beside the painting, there is a wooden chair. On the right side of the chair, there is a small table with a vase of flowers. In front of the painting, there is a woman sitting at a desk writing in a journal. On the left side of the woman, there is a window with curtains drawn.",

"there is a cat sleeping in the left of a dog on a couch at the left of the photo, is a gray cat."
]

for text in texts:
    print (f'\n{text[:10]}... {text[-10:]}')
    subtexts = globals_pos(text)
    for key in subtexts:
        for item in subtexts[key]:
            print(f'  - {key}: {item}')
