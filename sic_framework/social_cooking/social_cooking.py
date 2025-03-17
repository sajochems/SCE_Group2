import json
import numpy as np
from typing import Optional
from sic_framework.devices import Pepper
from sic_framework.services.dialogflow.dialogflow import Dialogflow, DialogflowConf, GetIntentRequest
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.devices.common_desktop.desktop_microphone import DesktopMicrophone

from recipe_manager import Step, Recipe, RecipeManager



IP_ADDRESS = '192.168.1.109'
DIALOGFLOW_KEYFILE_PATH = 'socialcooking-jcqe-b2a7e0f860e5.json'
# socialcooking-jcqe-ff31f337e816
# socialcooking-jcqe-b2a7e0f860e5
# socialcooking-jcqe-2706875d925d


def on_dialog(message):
    if message.response:
        if message.response.recognition_result.is_final:
            print("Transcript:", message.response.recognition_result.transcript)

class PepperSocialCooking:
    
    pepper = None
    dialogflow = None

    def __init__(self, ip:str, conf):
        # Create pepper and dialogflow component
        print("hi")
        self.pepper = Pepper(IP_ADDRESS)
        self.dialogflow = Dialogflow(ip='localhost', conf=conf)
        self.dialogflow.register_callback(on_dialog)
        self.dialogflow.connect(self.pepper.mic)

class DesktopSocialCooking:
    
    dialogflow = None

    def __init__(self, conf):
        # Create pepper and dialogflow component
        print("hello")
        microphone = DesktopMicrophone(ip='localhost')
        self.dialogflow = Dialogflow(ip='localhost', conf=conf)
        self.dialogflow.register_callback(on_dialog)
        self.dialogflow.connect(microphone)

class CookingSession:

    current_step_index = -1
    current_step = None
    recipe = None

    def __init__(self):
        print("making a recipe manager")
        self.recipe_manager = RecipeManager()
        

    def set_recipe(self, recipe_name) -> Optional[Recipe]:
        """Sets the recipe if the recipe_name exists in the recipe_manager"""
        
        try:
            self.recipe = self.recipe_manager.get_recipe_by_name(recipe_name)
        except TypeError:
            print(f"The recipe {recipe_name} does not exist.")

        return self.recipe
    
    
    def next_step(self) -> Optional[Step]:
        """Returns the next step if a recipe is set and the current step is not the final step."""
        
        if self.recipe != None:
            try:
                next_step = self.recipe.steps[self.current_step_index + 1]
                self.current_step = next_step
                self.current_step_index = self.current_step_index + 1
                return next_step
            except IndexError:
                print("The recipe contains no further steps")
                return None
        else:
            print("There is no recipe selected")
            return TypeError
        
    
    def is_final_step(self) -> bool:
        """Returns true if the current step is the final step"""

        if self.current_step_index == (len(self.recipe.steps) - 1):
            return True
        else: 
            return False


if __name__ == '__main__':
    print("starting main")
    # Set up configirations for dialogflow
    dialog_flow_keyfile = json.load(open(DIALOGFLOW_KEYFILE_PATH))

    #conf = DialogflowConf(keyfile_json=dialog_flow_keyfile, sample_rate_hertz=16000)

    # Create pepper
    #pepper = PepperSocialCooking(IP_ADDRESS, conf)

    print("setting up dialogflowConf...")
    #when switching to desktop
    conf = DialogflowConf(keyfile_json=dialog_flow_keyfile, sample_rate_hertz=44100, language="en")
    print("creating pepper")
    pepper = DesktopSocialCooking(conf)

    # Start conversation
    #pepper.pepper.tts.request(NaoqiTextToSpeechRequest("Hello! My name is pepper. What would you like to cook today?"))
    print("Hello! My name is pepper. What would you like to cook today?")

    # Set the current cooking session to the Egg Salad Sandwich
    cooking_session = CookingSession()
    cooking_session.set_recipe("Egg Salad Sandwich")

    # Randomly generate an id for the intent request
    intent_id = np.random.randint(10000)

    # This loop defines how many times pepper will listen (at maximum) before the conversation is ended

    try: 
        for i in range(25):
            print("---- Conversation turn", i)
            reply = pepper.dialogflow.request(GetIntentRequest(intent_id))

            #TODO: I am not sure this is the way the intent type will be returned. Can be tested with example on video.
            print(reply.intent)
            if reply.intent == "Finished Step":

                # Check if the current step is the final step
                if cooking_session.is_final_step():
                    #pepper.pepper.tts.request(NaoqiTextToSpeechRequest("Enjoy your meal! Let me know if you would like to cook something else next time!"))
                    print("Enjoy your meal! Let me know if you would like to cook something else next time!")

                    # Conversation ended, break out of loop
                    pepper.dialogflow.stop()
                    break
                else:
                    # Otherwise, reply with a default reply
                    text = reply.fulfillment_message
                    #pepper.pepper.tts.request(NaoqiTextToSpeechRequest(text))
                    print(text)

                    # Read the next step
                    step = cooking_session.next_step()
                    if step != None:
                        #pepper.pepper.tts.request(NaoqiTextToSpeechRequest(step.description))
                        print(step.description)
            
              #TODO: If necessary, define other types of intent and define what pepper should do in these cases
            
    except KeyboardInterrupt:
        print("Stop the dialogflow component.")
        pepper.dialogflow.stop()
