from Resources.cardDetection.sim2.hand import Hand
from Resources.cardDetection.sim2.card import Card
from Resources.cardDetection.sim2.kelly import kelly_fractional_bet, calc_kelly_frac
from Resources.cardDetection.sim2.rule_set import RuleSet

# TODO:
#
# set base bet when player takes seat at table wrt the ruleset

class BetExceedsStackSize(ValueError):
    pass

class InvalidSeat(IndexError):
    pass

class UnimplementedBetSpread(Exception):
    pass

class HandNotFound(Exception):
    pass

class CannotSplitHand(Exception):
    pass

class PlayerIR():
    def __init__(self,
            _id: int,
            stack_size: int,
            uses_kelly=False,
            ror=None,
            wongs_out=False,
            uses_deviations=False,
        ):
        """
        If a player's bet strategy is not mentioned, then they default
        to flat_betting the table minimum.

        If uses kelly betting, you must have an ror (Risk of Ruin) associated

        When wongs_out, this player will only play
        if the true count is at a +1 or higher.
        """
        self._id = _id
        self.stack_size = stack_size # in dollars
        self.uses_kelly = uses_kelly
        self.uses_deviations = uses_deviations

        if self.uses_kelly:
            self.bet_strat = 'kelly'
            # instantanious Risk of Ruin
            self.ror = ror # Need decimal form
            self.kelly_fract = calc_kelly_frac(ror)
        else:
            self.bet_strat = 'flat-bet'

        self.wongs_out = wongs_out

        # updated and cleared after every round
        self.curr_bet = None
        self.hands = [Hand(),]
        self.curr_hand = 0
        self.times_split = 0
        self.which_hand_doubled = [False,] # Always 1 hand at least
        self.took_insurance = False
        self.surrendered = False

        # used for stats chart
        self.num_hands_played = 0

    def __str__(self):
        return f"player_id:{self._id}, stack_size:{self.stack_size}, hand(s):{self.hands}, num_splits:{self.times_split }, curr_bet:{self.curr_bet}, bet_strat:'{self.bet_strat}, total hands played: {self.num_hands_played}, which hand doubled: {self.which_hand_doubled}"

    def __repr__(self):
        return f"<{str(self)}>"

    def __eq__(self, other):
        if isinstance(other, PlayerIR):
            return self._id == other._id
        return False

    def update_bet_size(self, true_count: int, rules: RuleSet):
        """Updates how much to bet at the start of a round. DOES NOT TAKE TO PAY ANY MONEY"""
        self.curr_bet = self.get_bet_size(true_count, rules)
        return

    # TODO
    # This calculation is *slightly* off. I think it was something to do with
    # the split_aces boolean in rule_set
    def get_bet_size(self, true_count: int, rules: RuleSet):
        """Returns the ammount this player will bet based on how they play, the given the rules, and the current true count"""
        if self.bet_strat == 'flat-bet':
            return rules.min_bet

        if self.bet_strat == 'kelly':
            # Recall, every true +1 corresponds to a 0.5% advantage
            player_edge = -rules.base_house_edge + 0.005*true_count
            percent_to_bet = kelly_fractional_bet(player_edge, rules.stddev, self.ror)
            bet = percent_to_bet*self.stack_size

            if bet <= rules.min_bet:
                return rules.min_bet
            if bet >= rules.max_bet:
                return rules.max_bet

            if bet < rules.min_bet:
                return rules.min_bet
            if bet > rules.max_bet:
                return rules.max_bet
            return bet

    # mutates the intended hand to split, and creates
    # two new hands of 1 card each.
    # These hands still need to have a card
    # dealt to them
    def split_hand(self, hand_to_split_index=None):
        if hand_to_split_index == None:
            hand_to_split_index = 0

        if not self.hands[hand_to_split_index].is_pair():
            raise CannotSplitHand(f"The hand {self.hands[hand_to_split_index]} is not a pair and therefore cannot be split")
        if self.times_split > 3:
            raise CannotSplitHand(f"Cannot split a hand more than 4 times")

        hand_to_split = self.hands[hand_to_split_index]
        card_to_split = hand_to_split.hand.pop()

        self.times_split += 1

        self.stack_size -= self.curr_bet

        # removes the card from one hand and places it
        # into a new hand
        self.hands.insert(hand_to_split_index+1, Hand([card_to_split]))

        self.which_hand_doubled.insert(hand_to_split_index+1, False) # new possible hand to double later

        return

    def add_hand(self, new_hand: Hand):
        self.hands.append(new_hand)

    def receive_card(self, card: Card, which_hand=None):
        if which_hand is None:
            self.hands[0].add_card(card)
        else:
            self.hands[which_hand].add_card(card)

    def reset_player(self, true_count: int, rules: RuleSet):
        """
        Clears the hands, and updates the player's
        game logic related instance variables
        """
        self.hands = [Hand(),]
        self.which_hand_doubled = [False,]
        self.took_insurance = False
        self.times_split = 0
        self.curr_bet = self.get_bet_size(true_count, rules)
        self.curr_hand = 0

    def give_money_to_player(self, amount):
        self.stack_size += amount

    def take_money_from_player(self, amount):
        self.stack_size -= amount

    def get_hand(self, index=None):
        if index:
            return self.hands[index]
        return self.hands[0]

    def get_hands(self):
        return self.hands

    def has_one_hand(self):
        return len(self.hands) == 1
