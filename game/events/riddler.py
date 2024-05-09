from game import event
from game.player import Player
from game.context import Context
import game.config as config

class Riddler(Context, event.Event):
    """Encounter a man who forces you to answer his riddles"""
    def __init__(self):
        super().__init__()
        self.name = "Riddler"
        self.man = 1
        self.verbs['solve'] = self
        self.answer1 = ['envelope']
        self.answer2 = ['sponge']
        self.answer3 = ['promise']
        self.correct_answers = 0  
        self.wrong_answers = 0  
        self.result = {}
        self.puzzle_ended = False
        self.go = False
    
    def process_verb(self, verb, cmd_list, nouns):
        if verb == 'solve':
            for n in self.answer1:
                print("What starts with an 'e' and ends with an 'e' but only has one letter in it?")
                answer = input().lower().strip()
                if answer != n:
                    print('Incorrect')
                    self.wrong_answers += 1
                else:
                    print('Correct')
                    self.correct_answers += 1
            for n in self.answer2:
                print("What is full of holes but still holds water?")
                answer = input().lower().strip()
                if answer != n:
                    print('Incorrect')
                    self.wrong_answers += 1
                else:
                    print('Correct')
                    self.correct_answers += 1
            for n in self.answer3:
                print("Which word becomes shorter when you add two letters to it?")
                answer = input().lower().strip()
                if answer != n:
                    print('Incorrect')
                    self.wrong_answers += 1
                else:
                    print('Correct')
                    self.correct_answers += 1
            print("You finished the riddles")
            self.puzzle_ended = True
            if self.correct_answers == 3:
                self.go = True
            elif self.wrong_answers == 3:
                self.go = True
                print("You failed to answer the riddles")

    def process(self, world):
        self.go = False
        self.result = {}
        self.result['Riddler'] = [self]
        self.result["message"] = "default message"
        while not self.go:
            print(str(self.name) + " riddler has appeared, type solve to amswer his riddles")
            Player.get_interaction([self])
        return self.result
