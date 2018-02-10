from naoqi import ALModule

class TescoModule(ALModule):
   
    def __init__(self):
        try:
            with open("keys.json") as config_file:
                config = json.loads(config_file.read())
                self.set_api_key(config["tesco_api_key"])
        # TODO: Proper exception handling
        except Exception as err:
            print("Error setting up Yummly Module")
            print(err)


    def set_api_key(self, tesco_api_key):
        self.tesco_key = tesco_api_key

    def search_for_ingredient(search_term):
        pass
