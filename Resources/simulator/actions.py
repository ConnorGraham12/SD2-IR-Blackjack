from enum import Enum

class Actions(Enum):
    HIT = 1
    STAND = 2
    DOUBLE = 3
    SPLIT = 4

    # only do these at a true 3 or higher
    # theyre actually the same thing from an EV point of view
    INSURANCE = 5
    EVEN_MONEY = 6
