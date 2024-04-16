from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Penguin(Context, event.Event):
    '''Encounter with a penguin. Uses the parser to decide what to do about it.'''
    def __init__ (self):
        super().__init__()
        self.name = "Penguin named Gunter"
        self.Penguin  = 1
        self.verbs['Swim'] = self
        self.verbs['feed'] = self
        self.verbs['help'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "Swim"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "the penguin will swim away."
                if (self.Penguin > 1):
                    self.Penguin = self.Penguin - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "luckly, the penguin swam away."
                else:
                    self.result["message"] = c.get_name() + " is targeted by a magical penguin."
                    if (c.inflict_damage (self.seagulls, "Pecked to death by penguin")):
                        self.result["message"] = ".. " + c.get_name() + " is pecked to death by the penguins!"

        elif (verb == "feed"):
            self.Penguin = self.Penguin + 1
            self.result["newevents"].append (Penguin())
            self.result["message"] = "the penguins are happy"
            self.go = True
        elif (verb == "help"):
            print ("the penguin will hunt you down unless you feed him")
            self.go = False
        else:
            print ("it seems the only options here are to feed or chase")
            self.go = False



    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.Penguin) + " Penguin Gunter has appeared what do you want to do?")
            Player.get_interaction ([self])

        return self.result
