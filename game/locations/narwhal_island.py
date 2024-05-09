from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class Narwhal_island (location.Location):
    
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Narwhal Island"
        self.symbol = "NWI"
        self.visitable = True
        self.starting_location = jungle_with_ship(self)
        self.locations = {}
        
        self.locations["Jungle"] = self.starting_location
        self.locations["cave"] = Cave(self)
        self.locations["abandon village"] = Abandon_village(self)
        self.locations["mountain"] = mountain(self)
    def enter (self, ship):
        print("arrived at Narwhal Island")
        
    def visit (self):
        
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        
class jungle_with_ship (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "jungle"
        self.verbs["north"] = self
        self.verbs['west'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.event_chance = 25
        self.events.append(drowned_pirates.DrownedPirates())
       
       
    def enter (self):
        announce ("arrive at the the jungle. your ship is located near a located east random dock")
        
    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "east"):
            announce("you walk back towards your ship")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Cave"]
            announce("You walk in to a cave. Do you proceed?")
        elif (verb == "south"):
            announce("While you walk south you come acroos a village. What now?")
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["mountain"]
            announce("there is large mountain in front of you, you can decide to climb it or just go back")
        
class Cave (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
        #including a coupleitems to pick up
        self.verbs['take'] = self
        self.item_in_cave = Item.Sword()
        self.item_in_cave = Item.Artifact()
        
        self.event_chance = 100
        self.events.append(drowned_pirates.DrownedPirates())
    
    

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        # add a couple items as a demo. 
        description = "pass the jungle, you walk in a dark cave"
        if edibles == False:
            description = description + 'You look around and found nothing to eat'

        #add a couple items as a demo
        if self.item_in_cave != None:
            description = description + 'in a shadow in the cave'
        announce (description)
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["jungle"]
             #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_cave == None:
                announce("you dont see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False # track if you pick up an item, print message 
                item = self.item_in_cave
                if item != None and (cmd_list[1]) == item.name or cmd_list[1] == "all":
                    announce("You pick up the "+item.name+" out of the cave")
                    config.the_player.add_to_inventory([item])
                    self.item_in_cave = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_cave
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name or cmd_list[1] == "all")
                    config.the_player.add_to_inventory([item])
                    self.item_in_caves = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")
                        
                    
                    
class mountain (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = mountain
        self.verbs['climb'] = self
        self.verbs['go back'] = self
        self.verbs['east'] = self
        
        self.event_chance = 100
        
    def eneter (self):
        description = "you climb on top of a mountain"
        announce(description)
        
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations["jungle"]
            config.the_player.go = True
        if (verb == 'climb'):
              config.the_player.next_loc = self.main_location.locations["mountain"]
        if (verb == 'go back'):
            config.the_player.next_loc = self.main_location.locations["jungle"]
            config.the_player.go = True
        

            
            
            
                    
class Abandon_village (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Abandon village"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['enter'] = self
        
        #change event when finished
        self.event_chance = 75
        self.events.append(seagull.Seagull())
        
    def enter (self):
        description = "You walk west from your ship and you see an abadon village\n there seems to be nothing much here"
        announce(description)
        
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Cave"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["jungle"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["mountain"]
        if (verb == "enter"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["abandon house"]    
    
    
class abandon_house (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "abandon house"
        self.verbs['exit'] = self
    
        
        self.event_chance = 100
        self.events.append(seagull.Seagull())
        
    def eneter(self):
        description = "You enter a house thats mostly destroyed\n a zombie pirate rises from the ground"
        announce(description)
        
    def process_verb(self, verb, cmd_list, nouns):
       if verb == "exit or leave":
            config.the_player.next_loc = self.main_location.locations["abandon village"]
            config.the_player.go = True
        
class ZombiePirate (event.Event):
    def __init__(self):
        self.name = "zombie attack"
           
    def process(self, world):
        result = {}
        Zombie = ZombiePirate()
        announce("a zombie pirate")
        combat.Combat([Zombie]).combat()
        announce('the zombie is limp')
        #set new events to an empty list
        result["newevents"]= []
        # Set the result message to an empty string, as we are printing our own strings at the right time.
        result["message"] = ""
        
        announce("In the house you find a katana")
        config.the_player.add_to_invrntory([Sword])
        
        return result

class Sword(Item):
    def __init__(self):
        super.__init__("sword", 400)
        self.damage = (20, 125)
        self.skill = "slash"
        self.verb = "hit"
        self.verb2 = "double slash"
    
    def pickTargets(self, action, attacker, allies, enemies):
        if (len(enemies) <= self.NUMBER_OF_ATTACKS): # If less than or equal to two targets, hit everyone
            return enemies
        else:
            options = []
            for t in enemies:
                options.append("attack " + t.name)
            targets = []

            while(len(targets) < self.NUMBER_OF_ATTACKS): # While loop so that it keeps going until the player picks two different targets.
                print(f"Pick target number {len(targets)}.")
                choice = menu(options)
                if(not choice in targets):
                    targets.append(enemies[choice])
            return targets
        


