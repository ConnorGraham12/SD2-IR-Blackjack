from Resources.cardDetection.sim2.hand import Hand

class Dealer:
    def __init__(self):
        # Upcard will always be hand[0]
        # to access the list of cards in the hands object,
        # You must call dealer.hand.hand
        # Looks wonky, but I'm not renaming everything at this point
        self.hand = Hand()

    def __str__(self):
        return f"Dealer hand: {self.hand}"

    def __repr__(self):
        return f"<Dealer hand: {self.hand}>"

    def get_up_card(self):
        if self.hand.hand == []:
            return None
        return self.hand.hand[0]

    def receive_card(self, card):
        self.hand.add_card(card)

    def get_hand(self):
        return self.hand

    def clear_hand(self):
        self.hand.clear_hand()
