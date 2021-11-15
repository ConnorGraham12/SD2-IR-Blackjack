from Resources.simulator.hand import Hand
import Resources.simulator.basic_strategy

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

class Player():
    def __init__(self, _id, stack_size, betting_unit_in_dollars, bet_spread_type=None):
        self._id = _id
        self.stack_size = stack_size # in dollars
        self.hands = [Hand(),]
        self.betting_unit = betting_unit_in_dollars
        self.curr_bet = betting_unit_in_dollars
        self.times_split = 0
        self.doubled_this_round = False
        self.num_hands_played = 0

        # defaults to a '1-8' bet spread
        if bet_spread_type == None or bet_spread_type == '1-8':
            self.bet_spread_type = '1-8'
        elif bet_spread_type == 'flat_bet':
            self.bet_spread_type = bet_spread_type
        elif bet_spread_type == '1-12':
            self.bet_spread_type = bet_spread_type
        else:
            raise UnimplementedBetSpread(f"Sorry, we haven't implemented this bet spread yet, you gave '{bet_spread_type}' for player {self._id}")

    def __str__(self):
        return f"player_id:{self._id}, stack_size:{self.stack_size}, hand(s):{self.hands}, num_splits:{self.times_split }, betting_unit:{self.betting_unit}, curr_bet:{self.curr_bet}, bet_spread_type:'{self.bet_spread_type}, total hands played: {self.num_hands_played}'"

    def __repr__(self):
        return f"<{str(self)}>"

    def __eq__(self, other):
        if isinstance(other, Player):
            return self._id == other._id
        return False

    # removes the hand_to_split and creates two new hands each of length 1
    # also removes the curr_bet from players stack
    def split_hand(self, hand_to_split_index):
        hand_to_split = self.hands[hand_to_split_index]

        if not hand_to_split.is_pair():
            raise CannotSplitHand(f"The hand {hand_to_split} is not a pair and therefore cannot be split")
        if self.times_split > 3:
            raise CannotSplitHand(f"Cannot split a hand more than 4 times")
        self.times_split += 1

        # needs to take money from player, not pay them
        self.take_money_from_player(self.curr_bet)

        card1 = hand_to_split.hand[0]
        card2 = hand_to_split.hand[1]
        self.remove_hand(hand_to_split)

        self.add_hand(Hand([card1]))
        self.add_hand(Hand([card1]))

    def add_hand(self, new_hand):
        self.hands.append(new_hand)

    def remove_hand(self, hand_to_remove):
        self.hands.remove(hand_to_remove)

    def receive_card(self, card, which_hand=None):
        if which_hand is None:
            self.hands[0].add_card(card)
        else:
            self.hands[which_hand].add_card(card)

    def clear_hands(self):
        self.hands = [Hand(),]
        self.doubled_this_round = False
        self.times_split = 0

    # horrible name, pay who?
    def give_money_to_player(self, ammount):
        self.stack_size += ammount

    def take_money_from_player(self, ammount):
        self.stack_size -= ammount

    def get_hand(self, index):
        return self.hands[index]

    def get_hands(self):
        return self.hands

    def place_bet(self, true_count):
        self.curr_bet = self.get_what_to_bet(true_count)
        self.take_money_from_player(self.curr_bet)

    # overwrites player index, be careful
    def take_seat(self, index, table):
        if index < 0 or index > 6:
            raise InvalidSeat(f" please insert a seat position between 0 and 6, you gave: {index}")
        table.player_list[index] = self

    def has_one_hand(self):
        return len(self.hands) == 1

    def get_what_to_bet(self, true_count):
        if self.bet_spread_type == '1-8':
            if true_count < 2:
                return self.betting_unit
            if true_count < 3:
                return 2*self.betting_unit
            if true_count < 4:
                return 3*self.betting_unit
            return 4*self.betting_unit
        if self.bet_spread_type == 'flat_bet':
            return self.betting_unit
        if self.bet_spread_type == '1-12':
            if true_count < 2:
                return self.betting_unit
            if true_count < 3:
                return 3*self.betting_unit
            if true_count < 4:
                return 6*self.betting_unit
            if true_count < 5:
                return 9*self.betting_unit
            return 12*self.betting_unit
