
from Resources.cardDetection.sim2.card import Card
from random import shuffle, randrange


class InvalidDeckNumber(ValueError):
  pass

class Shoe:

    # Example
    # new_shoe = Shoe(8, 0.75)
    # first_dealt_card = new_shoe.deal_one()

    # Once the cut card is dealt, keep dealing out that round,
    # then replace the shoe with a new shoe.

    # Returns None if the deck is empty

    # Shoe contains num_decks with the cut card at the index
    # represented by the float cut_card_placement. Typically this is 0.75
    # at a real 8 deck casino and 0.50 at an online casino.
    # Note: the float is exact, so if you want to mimic a semirandom
    # cut_card_placement of range 0.70-0.80, then you must generate your own
    # random float before calling this constructor

    # cut_card_placement: 0.0 means top of deck (first card delt)
    # cut_card_placement: 1.0 means last card in the deck (last card delt)
    def __init__(self, num_decks: int, cut_card_placement: float):

        if num_decks <= 0:
            raise InvalidDeckNumber(f"Please enter a valid number of decks, you gave: {num_decks}")
        self.deck = Shoe.get_shuffled_shoe(num_decks)
        # note: the top of the deck is the last index in the list,
        # so for index reasons, we need a (1 - cut_card_placement)
        index_of_cut_card = int((1 - cut_card_placement) * len(self.deck))
        self.deck.insert(index_of_cut_card, Card('C', 't'))
        self.cut_card_reached = False
        self.decks_left = self.get_decks_left()


    def __str__(self):
        """String representation of the list of cards in the shoe, including the cut card"""
        return str(self.deck)

    def __repr__(self):
        return str(self)

    def deal_one(self):
        """pops a card off the top of the deck and returns it"""
        if len(self.deck) <= 0:
            return None

        curr_card = self.deck.pop()

        if curr_card.card_face == 'C':
            self.cut_card_reached = True
            curr_card = self.deck.pop()

        return curr_card

    def get_decks_left(self):
        if self.cut_card_reached:
            return len(self.deck) / 52
        return (len(self.deck) - 1) / 52

    # This should never be touched again, sorry it's gross looking
    # Returns a list of 52 unique Cards in order
    @staticmethod
    def get_ordered_deck():
        return [
                Card('a', 's'), Card('k', 's'), Card('q', 's'), Card('j', 's'), Card('10', 's'), Card('9', 's'), Card('8', 's'), Card('7', 's'), Card('6', 's'), Card('5', 's'), Card('4', 's'), Card('3', 's'), Card('2', 's'),
                Card('a', 'c'), Card('k', 'c'), Card('q', 'c'), Card('j', 'c'), Card('10', 'c'), Card('9', 'c'), Card('8', 'c'), Card('7', 'c'), Card('6', 'c'), Card('5', 'c'), Card('4', 'c'), Card('3', 'c'), Card('2', 'c'),
                Card('a', 'd'), Card('k', 'd'), Card('q', 'd'), Card('j', 'd'), Card('10', 'd'), Card('9', 'd'), Card('8', 'd'), Card('7', 'd'), Card('6', 'd'), Card('5', 'd'), Card('4', 'd'), Card('3', 'd'), Card('2', 'd'),
                Card('a', 'h'), Card('k', 'h'), Card('q', 'h'), Card('j', 'h'), Card('10', 'h'), Card('9', 'h'), Card('8', 'h'), Card('7', 'h'), Card('6', 'h'), Card('5', 'h'), Card('4', 'h'), Card('3', 'h'), Card('2', 'h'),
        ]

    @staticmethod
    def random_insert(lst, item):
        lst.insert(randrange(len(lst)+1), item)

    # returns a shuffled list of Cards containing n of decks
    # Note: does not include the cut card
    @staticmethod
    def get_shuffled_shoe(num_decks: int):
        deck = []
        
        # makes list of n ordered decks
        for i in range(num_decks):
            for card in Shoe.get_ordered_deck():
                deck.append(card)

        shuffle(deck)

        return deck
