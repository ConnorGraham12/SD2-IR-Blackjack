from Resources.cardDetection.sim2.card import Card


class GameLogicError(Exception):
    pass


class Hand:
    def __init__(self, cards_list=None):
        if cards_list is None:
            self.hand = []
        else:
            self.hand = cards_list

    def __str__(self):
        return str([card for card in self.hand])

    def __repr__(self):
        return f"<Hand {self.hand}>"

    # note: must be EXACT same hand, so order matters
    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.hand == other.hand
        return False

    def delete_hand(self):
        del self

    def clear_hand(self):
        self.hand.clear()


    def add_card(self, card):
        self.hand.append(card)

    def has_ace(self):
        for card in self.hand:
            if card.is_ace():
                return True
        return False

    def is_pair(self):
        if len(self.hand) != 2:
            return False
        if self.hand[0].card_face != self.hand[1].card_face:
            return False
        return True

    def get_pairs_hard_hand_value(self):
        if self.is_pair():
            if self.hand[0].card_face == 'A':
                return 12
            if self.hand[0].card_face == 'K' or self.hand[0].card_face == 'Q' or self.hand[0].card_face == 'J':
                return 20
            return 2*int(self.hand[0].card_face)

        raise GameLogicError('Nonpair hand cannot be converted to hard value here')

    def is_blackjack(self):
        if len(self.hand) != 2:
            return False
        if self.hand[0].is_ace():
            if self.hand[1].get_hard_value() == 10:
                return True
        if self.hand[1].is_ace():
            if self.hand[0].get_hard_value() == 10:
                return True
        return False

# returns a tuple giving the hand type
# and the hand value as a string
    def get_hand_value(self):
        """Returns a tuple containing the hand's value: ('hand_type','value'). The value can be an 'A'. """
        if self.hand == []:
            return None

        if self.is_pair():
            if self.hand[0].is_ace():
                return ('pair', 'A')
            return ('pair', str(self.hand[0].get_hard_value()))

        total_value = 0
        num_aces = 0
        for card in self.hand:
            if card.is_ace():
                num_aces +=1
                continue
            total_value += card.get_hard_value()
        if num_aces == 0:
            return ('hard', str(total_value))
        # now we have to determine if its a hard ace or not
        # Hard hands with aces occur when no Ace can be 11
        # If it's 21, you stand no matter what, so being hard or soft doesn't matter
        if total_value + num_aces-1 + 11 > 21:
            return ('hard', str(total_value + num_aces))
        return ('soft', str(total_value + num_aces-1 + 11))

    # returns   'blackjack'
    #           'win'
    #           'lose'
    #           'push'
    def get_hand_result(self, dealer_hand):

        if self.is_blackjack():
            if dealer_hand.is_blackjack():
                return 'push'
            return 'blackjack'

        dealer_hand_value_tuple = dealer_hand.get_hand_value()
        if dealer_hand_value_tuple == ('pair', 'A'): # dealing with soft 12s
            dealer_hand_value = 12
        else:
            dealer_hand_value = int(dealer_hand_value_tuple[1])
            if dealer_hand.is_pair():
                dealer_hand_value = 2*dealer_hand_value

        if self.get_hand_value() == ('pair', 'A'): # dealing with soft 12s
            player_hand_value = 12
        else:
            player_hand_value = int((self.get_hand_value())[1])
            if self.is_pair():
                player_hand_value = 2*player_hand_value # pairs return single card's value

        if player_hand_value > 21:
            return 'lose'

        if dealer_hand_value > 21:
            return 'win'

        if player_hand_value == dealer_hand_value:
            return 'push'

        if player_hand_value > dealer_hand_value:
            return 'win'
        return 'lose'
