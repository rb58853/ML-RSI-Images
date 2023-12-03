import requests
import json

def search_images(image_url):
   """Searches for similar images."""
   params = {
       "engine": "google_lens",
       "url": image_url
   }

   response = requests.get("https://serpapi.com/search", params=params)
   data = response.json()

   for result in data["knowledge_graph"]:
       print("Title: ", result["title"])
       print("Link: ", result["link"])
       print("Thumbnail: ", result["thumbnail"])
       print("---")

   for result in data["visual_matches"]:
       print("Title: ", result["title"])
       print("Link: ", result["link"])
       print("Thumbnail: ", result["thumbnail"])
       print("---")
