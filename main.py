"""
main.py
Entry point for the application

created by lh16674 14/12/17
"""

import time

from YummlyModule import YummlyModule

yum = YummlyModule()

from naoqi import ALProxy

pepper_ip = "pepper.local"

# TODO: Change from storing location of pepper bot from hardcoded to config option in file

tts = ALProxy("ALTextToSpeech", pepper_ip, 9559)
animated_speech = ALProxy("ALAnimatedSpeech", pepper_ip, 9559)
tablet = ALProxy("ALTabletService", pepper_ip, 9559)

# When read to run for real/with voice, change debug to False
def say(prompt, debug=True, volume=0.5):
    if debug:
        print prompt
    else:
        tts.setVolume(volume)
        animated_speech.say(prompt, {"bodyLanguagemode": "contextual"})

def find_recipe(search_term, max_results=5):
    say("Searching for {}".format(search_term))

    current_recipe_index = 0
    found_recipe = False
    
    recipes = yum.find_recipes(search_term.split(" "), max_results)

    if recipes == None or len(recipes) < 1:
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

        say('Would you like to make it?')

        # TODO: TEMP VAR, REMOVE WHEN USER VOICE INPUT READY

        response = raw_input()

        # If user says no, give them the next recipe in the list
        # If we have finished the list, give up
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
    # TODO: Set volume to higher than 0.0 when not annoying people with the noise
    say("^start(animations/Stand/Gestures/Excited_1) What would you like to make?")
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
