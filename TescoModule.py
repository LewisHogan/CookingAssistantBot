"""
TescoModule.py
Module for the Robot that allows querying price information from an online source
created by lh16674 10/02/18
"""
import requests
import json

class TescoModule():
   
    def __init__(self):
        try:
            with open("keys.json") as config_file:
                config = json.loads(config_file.read())
                self.set_api_key(config["tesco_api_key"])
        # TODO: Proper exception handling
        except Exception as err:
            print("Error setting up Tesco Module")
            print(err)


    def set_api_key(self, tesco_api_key):
        self.tesco_key = tesco_api_key

    def search_for_ingredient(self, search_term, limit=1):
        headers = {
            "Ocp-Apim-Subscription-Key": self.tesco_key
        }
        url = "https://dev.tescolabs.com/grocery/products/?query=" + search_term + "&offset=0&limit=" + str(limit)
        return requests.get(url, headers=headers).json()["uk"]["ghs"]["products"]["results"]

    def estimate_cost(self, ingredient):
        search_results = self.search_for_ingredient(ingredient)
        return search_results[0]["price"] if len(search_results) > 0 else 0

    def estimate_costs(self, ingredients):
        total = sum([self.estimate_cost(x) for x in ingredients])

        return total
