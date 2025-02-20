import termcolor

from logic import *

# all people
mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]

# all rooms
ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

# all weapons
knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

# all character rooms and weapins are symbols
symbols = characters + rooms + weapons


# try to draw  a conclusion from what i know
def check_knowledge(knowledge):
    for symbol in symbols: # loop over symbols
        if model_check(knowledge, symbol): #check if that symbol is true
            termcolor.cprint(f"{symbol}: YES", "green") #print yes in green
        elif not model_check(knowledge, Not(symbol)): # if we're not sure
            print(f"{symbol}: MAYBE") # print maybe


# There must be a person, room, and weapon.
knowledge = And(
    Or(mustard, plum, scarlet), # mustrand or plum or scralet
    Or(ballroom, kitchen, library), # ballroom or kitchen or library
    Or(knife, revolver, wrench) # knife or revoliver or wrench
)

# Initial cards
knowledge.add(And(
    Not(mustard), Not(kitchen), Not(revolver) # NOT mustard AND NOT ktichen AND NOT relvoler
))

# Unknown card
knowledge.add(Or(
    Not(scarlet), Not(library), Not(wrench) # NOT scarlet OR NOT libaray OR NOT weench
))

# Known cards
knowledge.add(Not(plum))
knowledge.add(Not(ballroom))

check_knowledge(knowledge)
