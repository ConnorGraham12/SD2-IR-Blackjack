from Resources.simulator.shoe import Shoe
from Resources.simulator.hand import Hand
from Resources.simulator.card import Card
from Resources.simulator.player import Player
from Resources.simulator.dealer import Dealer
from math import floor
import matplotlib
import numpy
import Resources.simulator.basic_strategy as bs
import Resources.simulator.count_map as cm

MIN_NUM_BETTING_UNITS_ALLOWED = 4
MAX_NUM_OF_SPLITS_ALLOWED = 4
LEAVE_THE_TABLE_ON_THIS_COUNT_TRUE_COUNT = -2

#####################
# TODO: REWRITE THIS ENTIRE FILE IT SUCKS!!!
#       Next time write unit tests while building the app
#       then, it might actually work...
#
# - Make it so the dealer hits on a soft 17 to better match vegas rules
#
# - Allow doubledown after split
#   This would me completely changing how payments works.
#   Might need to create a list of player bets wrt player hands
#
# - Players currently bet their base betting_unit instead of table minimum at true count of 1 and below,
#   so we need an option to force betting the table minimum instead of base betting unit.
#
# - Add option to leave the table when the true count reaches a certain optinal number
#   Just create a new shoe in this case
#   implement surrendering
#
#
#####################

####################################################################
# DO NOT CHANGE THESE VALUES YET
# they do not currently work if you change them
# need to create a new strategy chart and edit play_turn() to implement these
ALLOW_DOUBLE_AFTER_SPLIT = False
ALLOW_SURRENDER = False
####################################################################

FORCE_ONE_CARD_ON_SPLIT_ACES = True


class BankruptPlayer(Exception):
    pass

class NoPlayersError(Exception):
    pass

# we're forcing players to only bet on one spot
class Table:
    def __init__(self, num_decks, deck_pen, min_bet, max_bet):
        self.num_decks = num_decks
        self.deck_pen = deck_pen
        self.shoe = Shoe(num_decks, deck_pen)

        self.player_list = [None] * 7
        self.bankrupt_players = []
        self.dealer = Dealer()
        self.num_hands_played = 0

        self.running_count = 0
        self.true_count = 0
        self.strategy = bs.get_basic_strategy()
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.count_map = cm.get_hi_low_map()

    def __str__(self):
        string = "Game state\n"

        string += f"min bet is {self.min_bet}\n"
        string += f"max bet is {self.max_bet}\n"
        string += "\n"

        string += f"Running count: {self.running_count}\n"
        string += f"True count: {self.true_count}\n"
        string += "\n"

        string += f"Dealer's upcard: {self.dealer.get_up_card()}\n"
        string += "\n"

        string += f"Players list: \n"
        for player in self.player_list:
            if player:
                string += f"\tSeat {self.player_list.index(player)}\t{player}\n"
        string += "\n\n"

        if len(self.bankrupt_players) != 0:
            string += f"Bankrupt players:\n"
        for player in self.bankrupt_players:
            string += f"\t{player}\n"


        string += f"shoe size: {self.num_decks}\n"
        string += f"deck penetration: {self.deck_pen}\n"
        string += f"cards left in shoe: {len(self.shoe.deck)}\n"
        string += f"decks left: {round(self.shoe.get_decks_left(), 2)}"

        return string


    # returns a card popped off the shoe and updates the count accordingly
    # which_hand is for the index of the player hand to deal to during a split hand
    # if which_hand is None, player has 1 hand
    def deal_card(self, player_or_dealer_object, which_hand=None):
        curr_card = self.shoe.deal_one()
        self.running_count += self.count_map[curr_card.card_face]
        self.true_count = floor(self.running_count / self.shoe.get_decks_left())

        if isinstance(player_or_dealer_object, Player):
            if which_hand is None:
                player_or_dealer_object.receive_card(curr_card)
            else:
                player_or_dealer_object.receive_card(curr_card, which_hand)

        if isinstance(player_or_dealer_object, Dealer):
            player_or_dealer_object.receive_card(curr_card)

    # assuming all players are card counters
    def set_all_player_bets(self):
        for player in self.player_list:
            if player:
                if player.stack_size < MIN_NUM_BETTING_UNITS_ALLOWED*player.betting_unit:
                    # remove bankrupt player
                    i = 0
                    for possibly_bankrupt_player in self.player_list:
                        if possibly_bankrupt_player == player:
                            self.bankrupt_players.append(player)
                            self.player_list[i] = None
                        i+=1
                    # raise BankruptPlayer(f'Player {player._id} has less than {MIN_NUM_BETTING_UNITS_ALLOWED} betting units left')
                player.place_bet(self.true_count)

    def play_all_player_turns(self):
        for player in self.player_list:
            if player:
                self.play_turn(player)

    def play_n_rounds(self, n, num_bank_bins):
        # Example
        # 500,000 rounds % 500 => plot bankroll every 500 rounds
        # which totals 1000 points to plot
        bank_over_time = numpy.zeros(num_bank_bins, dtype=int)
        bin_size = n/num_bank_bins
        j=0
        for i in range(n):
            if i%bin_size == 0:
                bank_over_time[j] = self.player_list[0].stack_size
                j+=1
                # print("at j=" +str(j) +"  stack="+str(self.player_list[0].stack_size))
            self.play_round()

        return bank_over_time

    # this needs to play_all_player_turns and play_dealer_turn cannot
    # be different functions if we want to allow for people to take insurance
    # after the dealer checks for blackjack
    # honestly, need to rewrite this whole thing from stratch
    def play_round(self):
        if self.has_no_players():
            raise NoPlayersError("No players have sat at the table")

        self.set_all_player_bets()
        self.deal_inital_round()
        self.play_all_player_turns()
        self.play_dealer_turn()


        # deals with paying based on player hands
        # dont forget, split aces are not considered blackjack, first check for players outside of index > 6
        self.pay_out_players()

    def has_no_players(self):
        for player in self.player_list:
            if player:
                return False
            return True


    def play_dealer_turn(self):
        _, hand_value = self.dealer.get_hand().get_hand_value()

        # must account for pair of aces which is a soft 12
        while hand_value == 'A' or int(hand_value) < 17:
            self.deal_card(self.dealer)
            _, hand_value = self.dealer.get_hand().get_hand_value()

        # print(f"dealers hand: {hand_value}")

    def pay_out_players(self):
        for player in self.player_list:
            if player:
                if player.doubled_this_round:
                    hand_outcome = player.get_hand(0).get_hand_result(self.dealer.get_hand())

                    # (recall we subtracted 2*player.curr_bet at this point)
                    if hand_outcome == 'win':
                        player.give_money_to_player(4*player.curr_bet)

                    if hand_outcome == 'push':
                        player.give_money_to_player(2*player.curr_bet)

                elif player.has_one_hand():
                    hand_outcome = player.get_hand(0).get_hand_result(self.dealer.get_hand())
                    if hand_outcome == 'blackjack':
                        # pays out 3 to 2
                        player.give_money_to_player(2.5 * player.curr_bet)
                        continue
                    if hand_outcome == 'win':
                        player.give_money_to_player(2 * player.curr_bet)
                        continue
                    # the player already paid their bet, so they dont get anything back
                    if hand_outcome == 'lose':
                        continue
                    if hand_outcome == 'push':
                        player.give_money_to_player(player.curr_bet)
                        continue
                # split hands
                # each hand already paid money
                else:
                    i = 0
                    for hand in player.hands:
                        hand_outcome = player.get_hand(i).get_hand_result(self.dealer.get_hand())

                        if hand_outcome == 'win':
                            player.give_money_to_player(2 * player.curr_bet)
                            continue
                        # remember, they already paid money, so they just dont get any back
                        if hand_outcome == 'lose':
                            continue
                        if hand_outcome == 'push':
                            player.give_money_to_player(player.curr_bet)
                            continue
                        i +=1

    def deal_inital_round(self):
        self.clear_table()
        for i in range(2):
            for player in self.player_list:
                if player is None:
                    continue
                self.deal_card(player)
            self.deal_card(self.dealer)

    def clear_table(self):
        self.dealer.clear_hand()
        for player in self.player_list:
            if player:
                player.clear_hands()

        if self.shoe.cut_card_reached or self.true_count <= LEAVE_THE_TABLE_ON_THIS_COUNT_TRUE_COUNT:
            self.replace_shoe(self.num_decks, self.deck_pen)
            self.true_count = 0
            self.running_count = 0


    def replace_shoe(self, num_decks, deck_pen):
        self.num_decks = num_decks
        self.deck_pen = deck_pen
        self.shoe = Shoe(num_decks, deck_pen)


    # this function will transform the player's list of hands into what it
    # should be based on how they should play the hand based on the strategy chart
    #
    # note: the current hand stops playing once either a value of 21 or greater is reached
    #       or a 'stand' action occurs.
    #       money is also taken from player stacks wrt doubles and splits as they occur
    #
    # players are NOT PAID MONEY in this function
    # money is ONLY TAKEN from players for ease of accounting for blackjack payouts
    # since 3:2 payout is only for a 'natural blackjack' player stacks are updated
    # accordingly during the pay_out_players() event
    #
    # possible error: If a player runs out of money, this will not work correctly
    # Therefore, a BankruptPlayer error is thrown when any player's stack is too small
    def play_turn(self, player, current_hand_index=None):

        # when player currently has no split hands
        if current_hand_index is None:
            self.num_hands_played += 1
            player.num_hands_played += 1



            hand_type, hand_value = player.get_hand(0).get_hand_value()

            # only occurs when dealt aces initally, and it also overwritten but whatever
            if hand_value == 'A':
                action = 'SPLIT'
            elif int(hand_value) >= 21:
                return

            action = self.strategy[hand_type][(hand_value, self.dealer.get_up_card().card_face)]

            # print(f"Running count is: {self.running_count},\tTrue count is: {self.true_count},\tPlayer:{player._id} has a {hand_type} {hand_value} with a dealer upcard of {self.dealer.get_up_card()} and should {action}")


            if action == 'SPLIT':
                # removes the current single hand, and creates two hands each with one card
                # also adds 1 to player.num_splits
                player.split_hand(0)

                # deal a new card into each new hand
                self.deal_card(player, 0)
                self.deal_card(player, 1)

                # plays the turn for each hand with player.num_splits updated
                self.play_turn(player, 0)
                self.play_turn(player, 1)

                return

            # This can never be a split card
            # When can't we double? When we've split.
            # therefore, we can always double in this case
            # player gets 1 card and returns
            # raises double flag for pay event
            if action == 'DOUBLE':
                player.doubled_this_round = True
                player.take_money_from_player(player.curr_bet)
                self.deal_card(player)
                return

            # note: after hitting, we dont have to worry about splits or doubles anymore
            if action == 'HIT':
                self.deal_card(player)
                self.play_turn(player)

                return

            if action == 'STAND':
                return

        # count this split hand too
        self.num_hands_played += 1
        player.num_hands_played += 1

        # Only get here if player has split hands
        # we can now access current_hand_index
        # player can no longer double after split
        # player can only resplit 3 times total
        # otherwise hit or stand
        hand_type, hand_value = player.get_hand(current_hand_index).get_hand_value()

        if hand_value == 'A':
            action = 'SPLIT'
        elif int(hand_value) >= 21:
            return

        action = self.strategy[hand_type][(hand_value, self.dealer.get_up_card().card_face)]

        # can only split 3 total times
        # happens when player splits again
        if action == 'SPLIT':
            if player.times_split >= 3:
                hand_type = 'hard'
                hand_value = player.get_hand(current_hand_index).get_pairs_hard_hand_value()
                action = self.strategy[hand_type][(str(hand_value), self.dealer.get_up_card().card_face)]
            # the rare soft 12
            # This allows for playing an ace after it's split, so this is a bug i think?
            # lets force a stand here
            elif hand_value == 'A':
                hand_type = 'soft'
                hand_value = '12'
                action = 'STAND'
            else:
                player.split_hand(current_hand_index)
                self.deal_card(player, current_hand_index)
                self.deal_card(player, current_hand_index + 1)
                self.play_turn(player, current_hand_index)
                self.play_turn(player, current_hand_index + 1)

                return

        # print(f"Running count is: {self.running_count},\tTrue count is: {self.true_count},\tPlayer:{player._id} has a {hand_type} {hand_value} with a dealer upcard of {self.dealer.get_up_card()} and should {action}")

        # no double after split
        if action == 'DOUBLE':
            # hard coded basic strategy stuff here for double after split things
            # only time we even consider a double so high here is on a soft hand, so hit instead
            if hand_type == 'soft':
                if int(hand_value) >= 18:
                    action = 'STAND'
                else:
                    action = 'HIT'
            else:
                action = 'HIT'

        if action == 'HIT':
            self.deal_card(player, current_hand_index)
            self.play_turn(player, current_hand_index)

            return

        if action == 'STAND':
            return

        # raise GameLogicError('This error should never be reached. If it is, then oopsies...')
