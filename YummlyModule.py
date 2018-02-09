"""
YummlyModule.py
Module for the Robot that allows querying recipe information from an online source
created by lh16674 12/12/17
"""
import requests
import json

class YummlyModule:

    def __init__(self):
        try:
            with open("keys.json") as config_file:
                config = json.loads(config_file.read())
                self.set_app_id(config["yummly_app_id"])
                self.set_api_key(config["yummly_api_key"])
        # TODO: Proper exception handling
        except Exception as err:
            print("Error setting up Yummly Module")
            print(err)

    def set_app_id(self, new_id):
        self.app_id = new_id

    def set_api_key(self, new_api_key):
        self.api_key = new_api_key

    
    def search_yummly(self, search_params):
        """
        Searches Yummly API using given parameters,
        see (https://developer.yummly.com/documentation) for params list

        Args:
            search_params: str[]

        Returns:
            A request object which contains a json of the found results
        """

        url = "http://api.yummly.com/v1/api/recipes?_app_id=" + self.app_id + "&_app_key=" + self.api_key + "&" + "&".join(search_params)
        return requests.get(url)

    def get_recipe(self, recipe_id):
        """
        Fetches a specific recipe's information in detail from YUMMLY
        See (https://developer.yummly.com/documentation) for a list of attributes
    
        Args:
            recipe_id: str

        Returns:
            A json object with the details of the requested recipe
        """
        
        try:
            url = "http://api.yummly.com/v1/api/recipe/" + recipe_id + "?_app_id=" + self.app_id + "&_app_key=" + self.api_key
            return requests.get(url).json()
        except ValueError:
            # TODO: Implement response to failing to convert json
            return None
    
    def find_recipes(self, ingredients, limit=5):
        """
        Searches Yummly API for the top n recipes containing a certain ingredient
    
        Args:
            ingredients : str[]
            limit : int

        Returns:
            A list of all found recipes (up to size n)
        """

        try:
            params = [
                "q=" + " ".join(ingredients),
                # Disable if we decide not to go with the "Use Robot chest to display image"
                "requirePictures=true",
                "maxResult=" + str(limit)
            ]
            search_results = self.search_yummly(params).json()

            return search_results["matches"]
        except ValueError:
            # If we are unable to obtain and parse the recipes
            return None
