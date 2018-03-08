"""
main.py
Entry point for the application

created by lh16674 14/12/17
"""

import time

from YummlyModule import YummlyModule
from TescoModule import TescoModule

yum = YummlyModule()
tesco = TescoModule()

from naoqi import ALBroker
from naoqi import ALProxy

pepper_ip = "pepper.local"
broker_port = 9559

# TODO: Change from storing location of pepper bot from hardcoded to config option in file

tts = ALProxy("ALTextToSpeech", pepper_ip, broker_port)
animated_speech = ALProxy("ALAnimatedSpeech", pepper_ip, broker_port)
speech = ALProxy("ALTextToSpeech", pepper_ip, broker_port)
tablet = ALProxy("ALTabletService", pepper_ip, broker_port)

# When read to run for real/with voice, change debug to False
def say(prompt, debug=False, volume=0.5, animated=True, force_speech = False):
    prompt = prompt.encode("ascii", "ignore")
    if debug:
        print prompt

    if force_speech or not debug:
        tts.setVolume(volume)

        if animated:
            animated_speech.say(prompt, {"bodyLanguagemode": "contextual"})
        else:
            speech.say(prompt)
        

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

    if tablet.loadUrl(str(recipe["source"]["sourceRecipeUrl"])):
        tablet.showWebview()

    say("The ingredients for {} are".format(recipe["name"]))

    for ingredient in set(recipe["ingredientLines"]):
        say(ingredient, debug=True)
        say(ingredient)

    recipe_price = tesco.estimate_costs(recipe["ingredientLines"])
    say("I've been looking online, and I think the recipe should cost {} pounds".format(recipe_price))
    say("I'm still learning how to read instructions, in the mean time, try looking at my chest")

def show_conversions():
    # Loads the webpage with a selection of conversion options onto the tablet
    if tablet.loadUrl("http://privatewww.essex.ac.uk/~lh16674/tempConversion.html"):
        tablet.showWebview()

def make_recipe():
    while True:
        # TODO: Set volume to higher than 0.0 when not annoying people with the noise
        say("^start(animations/Stand/Gestures/Excited_1) What would you like to make?", debug=True, force_speech=True)
        # TODO: Replace with user voice input
	
	# From looking at the documentation available http://doc.aldebaran.com/2-1/naoqi/audio/alspeechrecognition-api.html#alspeechrecognition-api
	# It looks like we need to subscribe to an event
	# Then we can unsubscribe and continue here
        search_term = raw_input(":")
	# Put a loop here until we get an event, might need a global/nonlocal to say if we've encountered a word yet to break out
        if search_term in ["quit", "exit", "stop"]:
            break

        recipe = find_recipe(search_term)

        if recipe == None:
            say("Sorry, I couldn't find a recipe for that")
            continue
        else:
            display_recipe(recipe)
            break

while True:
    say("What would you like to do?")
    say("cook, convert or shut me down?")
    response = raw_input(":")

    if response in ["cook", "bake", "food", "make"]:
        make_recipe()
    elif response in ["convert"]:
        show_conversions()
    else:
        say("Shutting down...")
        break
