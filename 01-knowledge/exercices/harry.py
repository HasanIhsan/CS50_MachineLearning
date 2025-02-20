from logic import *

rain = Symbol("rain") # it is raining
hagrid = Symbol("hagrid") # harry visited hagrid
dumbledore = Symbol("dumbledore") # harry visited dumberdore


knowledge = And(
    Implication(Not(rain), hagrid), # if it is not raning then harry visited hagrid
    Or(hagrid, dumbledore), # harry visited hagrid or dumbledore
    Not(And(hagrid, dumbledore)), #harry didn't visit both hagrid or dumbledore
    dumbledore # hharry visited dumbledore
)

print(knowledge.formula())
print(model_check(knowledge, rain))
