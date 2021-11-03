class InvalidCardInitalization(ValueError):
  pass

class Card:
    # Card('A', 's')
    # s -> spades, h -> hearts, c -> clubs, d -> diamonds
    # 2-10, J, Q, K, A
    # Card('C', 't') represents cut card because im lazy
    def __init__(self, card_face: str, suit: str):
        # still allows for any character to be initalized in a card
        if type(card_face) != str or type(suit) != str or len(card_face) > 2 or len(suit) != 1:
            raise InvalidCardInitalization(f"Please enter a valid card, you gave: {card_face}{suit}")
        self.card_face = card_face.upper()
        self.suit = suit.lower()

    def __str__(self):
        return f"{self.card_face}{self.suit}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.card_face == other.card_face and self.suit == other.suit
        return False


    def is_cut_card(self):
        if self.card_face == 'C':
            return True
        return False

    def is_ace(self):
        if self.card_face == 'A':
            return True
        return False

    def get_hard_value(self):
        if self.card_face == 'A':
            return 1

        if self.card_face == 'K' or self.card_face == 'Q' or self.card_face == 'J':
            return 10;

        return int(self.card_face)

    # shorthand methods for developing
    @classmethod
    def ace(cls):
        return Card('a', 's')

    @classmethod
    def king(cls):
        return Card('k', 's')

    @classmethod
    def jack(cls):
        return Card('j', 's')

    @classmethod
    def ten(cls):
        return Card('10', 's')

    @classmethod
    def nine(cls):
        return Card('9', 's')

    @classmethod
    def eight(cls):
        return Card('8', 's')

    @classmethod
    def seven(cls):
        return Card('7', 's')

    @classmethod
    def six(cls):
        return Card('6', 's')

    @classmethod
    def five(cls):
        return Card('5', 's')

    @classmethod
    def four(cls):
        return Card('4', 's')

    @classmethod
    def three(cls):
        return Card('3', 's')

    @classmethod
    def two(cls):
        return Card('2', 's')
