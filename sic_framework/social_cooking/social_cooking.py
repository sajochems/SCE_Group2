from sic_framework.devices import Pepper
from sic_framework.services.dialogflow.dialogflow import Dialogflow, DialogflowConf, GetIntentRequest
from SCE_Group2.recipe_manager import Recipe, RecipeManager


IP_ADDRESS = '192.168.1.109'
DIALOGFLOW_KEYFILE = 'SCE_Group2\socialcooking-jcqe-2706875d925d' 

class PepperSocialCooking:

    def __init__(self, ip:str, conf):
        self.pepper = Pepper(IP_ADDRESS)
        self.dialogflow = Dialogflow(ip='localhost', conf=conf)
        self.dialogflow.connect(self.pepper.mic)
        #self.dialogflow.register_callback(on_dialog)
    
    def on_dialog(self, ):
        intent = self.dialogflow.request(GetIntentRequest())
        # TODO: Here we identify all the possible intents

    def set_cookingSession(self, recipeManager):
        self.session = CookingSession(recipeManager)

class CookingSession:

    def __init__(self, recipeManager):
        self.recipe_manger = recipeManager
        self.current_step = 0


if __name__ == '__main__':
    # Set up configirations for dialogflow
    conf = DialogflowConf(keyfile_json=DIALOGFLOW_KEYFILE)

    # Create pepper
    pepper = PepperSocialCooking(IP_ADDRESS, conf)