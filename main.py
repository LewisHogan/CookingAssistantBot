import time

from YummlyModule import YummlyModule

yum = YummlyModule()

from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "pepper.local", 9559)
tablet = ALProxy("ALTabletService", "pepper.local", 9559)

tts.setVolume(0.5)

def say(prompt, debug=True):
    if debug:
        print prompt
    else:
        tts.say(prompt)

def find_recipe(search_term, max_results=5):
    say("Searching for {}".format(search_term))

    current_recipe_index = 0
    found_recipe = False
    
    recipes = yum.find_recipes(search_term.split(" "), max_results)

    if recipes == None:
        say("I couldn't find a recipe!")
        return None

    while not found_recipe and current_recipe_index < len(recipes):
        say("I found a recipe called {}".format(recipes[current_recipe_index]["recipeName"]))

        recipe = yum.get_recipe(recipes[current_recipe_index]['id'])
        # If there are any images of the recipe, we show it on the tablet
        if len(recipe['images']) > 0:
            if recipe['images'][0]['hostedLargeUrl']:
                tablet.showImage(str(recipe['images'][0]['hostedLargeUrl']))
            elif recipe['images'][0]['hostedMediumUrl']:
                tablet.showImage(str(recipe['images'][0]['hostedMediumUrl']))
            elif recipe['images'][0]['hostedSmallUrl']:
                tablet.showImage(str(recipe['images'][0]['hostedSmallUrl']))
        # TODO: Ask if the user wants that recipe

        say('Would you like to make it?')

        # TEMP VAR, REMOVE WHEN USER VOICE INPUT READY

        response = raw_input()

        if response.lower() in  ["no", "nah", "nope", "negative", "no thanks", "n"]:
            if current_recipe_index < len(recipes)-1:
                say("Let's try another recipe then")
            else:
                say("Looks like I'm all out of ideas")
                return None
    
            current_recipe_index += 1
            continue
        else:
            found_recipe = True
            say("Looks like we're making {}".format(recipe["name"]))

    # If user says no, give them the next recipe in the list
    # If we have finished the list, give up

    # If the user says yes however, then we can print the ingredients and show the webpage of the food

    return recipe

def display_recipe(recipe):
    # Show webpage on tablet
    # List instructions via voice
    say("The ingredients for {} are".format(recipe["name"]))

    if tablet.loadUrl(str(recipe["source"]["sourceRecipeUrl"])):
        tablet.showWebview()

    for ingredient in set(recipe["ingredientLines"]):
        say(ingredient)

    say("I don't quite know how to read the instructions yet, but you can see them on my chest")

while True:
    say("What would you like to make?")
    # TODO: Replace with user voice input
    search_term = raw_input()
    if search_term in ["quit", "exit", "stop"]:
        break

    recipe = find_recipe(search_term)

    if recipe == None:
        continue
    else:
        display_recipe(recipe)
        break
    