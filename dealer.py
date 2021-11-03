from hand import Hand

class Dealer:
    def __init__(self):
        # Upcard will always be hand[0]
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
