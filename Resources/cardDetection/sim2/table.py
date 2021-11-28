import Resources.cardDetection.sim2.count_map as cm
import Resources.cardDetection.sim2.basic_strategy as bs
from Resources.cardDetection.sim2.shoe import Shoe
from Resources.cardDetection.sim2.hand import Hand
from Resources.cardDetection.sim2.card import Card
from Resources.cardDetection.sim2.player import Player
from Resources.cardDetection.sim2.dealer import Dealer
from Resources.cardDetection.sim2.rule_set import RuleSet
from math import floor

class GameLogicError(Exception):
    pass

class Table:
    def __init__(self, _id: int, rules: RuleSet):
        self._id = _id
        self.shoe = Shoe(rules.num_decks, rules.penetration)
        self.rules = rules

        self.player_list = [None] * 7
        self.bankrupt_players = []
        self.dealer = Dealer()
        self.num_hands_played = 0

        self.running_count = 0
        self.true_count = 0

        self.count_map = cm.get_hi_low_map()

        if self.rules.stand_on_soft_17:
            self.strategy = bs.get_bs_stand_soft_17()
        else:
            self.strategy = bs.get_bs_hit_soft_17()

    def __str__(self):
        string = "Game state\n"

        string += f"min bet is {self.rules.min_bet}\n"
        string += f"max bet is {self.rules.max_bet}\n"
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


        string += f"shoe size: {self.rules.num_decks}\n"
        string += f"deck penetration: {self.rules.penetration}\n"
        string += f"cards left in shoe: {len(self.shoe.deck)}\n"
        string += f"decks left: {round(self.shoe.get_decks_left(), 2)}"

        return string

    # Should rewrite to default to just appending to the list
    # if index is not specified, and throw an error if len is > 7
    def add_player(self, seat_index: int, player: Player):
        """Overwrites a player to the seat index"""
        if isinstance(self.player_list[seat_index], Player):
            raise IndexError(f"A player is already sitting at index {seat_index}!")

        self.player_list[seat_index] = player

    def remove_player(self, seat_index: int):
        """Removes player the list of players at the given index"""
        if not isinstance(self.player_list[seat_index], Player):
            raise IndexError(f"There is no player at index {seat_index} to remove.")
        self.player_list[seat_index] = None

    def deal_card(self, player_or_dealer_object, which_hand=None):
        """
        Give the corresponding player_or_dealer_object a new card.
        which_hand is for the index of the player hand to deal to during a split
        which_hand defaults to None (For when player has 1 hand)
        Automatically updates the running and true count
        """
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

    def reset_table(self):
        """
        Removes all the cards from the player and dealer hands and
        resets all instance variables relating to gameplay logic
        for every player object. (such as curr_bet, times_split, etc..)
        """
        if self.shoe.cut_card_reached:
            self.shoe = Shoe(self.rules.num_decks, self.rules.penetration)
            self.true_count = 0
            self.running_count = 0

        self.dealer.clear_hand()
        for player in self.player_list:
            if player:
                player.reset_player(self.true_count, self.rules)

    def deal_initial_round(self):
        """Deals out the inital 2 cards to each player and dealer"""
        # deal out intial 2 cards
        for i in range(2):
            for player in self.player_list:
                if player:
                    self.deal_card(player)
            self.deal_card(self.dealer)

    def add_to_bankrupt_players(self, bankrupt_player: Player):
        """Removes player from table and adds them to the bankrupt players list"""
        self.bankrupt_players.append(bankrupt_player)

        for i in range (7):
            if self.player_list[i] == bankrupt_player:
                self.player_list[i] = None

    def all_players_make_inital_bet(self):
        """Takes the current bet out of every players stack_size"""
        # players make their bets
        for player in self.player_list:
            if player:
                # player basically bankrupts
                if player.stack_size <= 2*player.curr_bet:
                    self.add_to_bankrupt_players(player)
                else:
                    player.stack_size -= player.curr_bet

    def insurance(self):
        """
        Checks if the dealer's upcard is an Ace, and if it is, makes all players
        who are using deviations pay the insurance bet if the true count is
        3 or higher. (Only time it's profitable to take insurance)
        """
        if self.dealer.get_up_card().is_ace():
            if self.rules.insurance: #insurance is allowed
                for player in self.player_list:
                    if player:
                        if player.uses_deviations:
                            if self.true_count >=3:
                                player.stack_size -= 0.5*player.curr_bet
                                player.took_insurance = True

    # Assumes you are able to hit
    def hit(self, player_or_dealer_object, hand_index=None):
        """
        Simulates a player who hits.
        Hand_index defaults to the first hand unless specified
        """
        self.deal_card(player_or_dealer_object, hand_index)
        return

    # Assumes you are able to stand
    def stand(self):
        """Simulates a player who stands."""
        # lol
        return

    # Assumes you are able to double
    def double(self, player: Player, hand_index=None):
        """
        Simulates a player who doubles.
        Hand_index defaults to the first hand unless specified
        """
        player.stack_size -= player.curr_bet # places another bet

        if hand_index == None:
            hand_index = 0

        self.deal_card(player, hand_index)
        player.which_hand_doubled[hand_index] = True
        # everytime a player splits, an index is added to the
        # which hand doubled index, to prevent an out of bounds error

        return

    # Assumes you are able to split
    def split(self, player: Player, hand_index=None):
        """
        Splits hand at index into 2 new hands, and deals a card to each.
        Also takes another bet from the player
        """
        if hand_index == None:
            hand_index = 0

        player.split_hand(hand_index) # this already takes money away (bad design)
        self.deal_card(player, hand_index)
        self.deal_card(player, hand_index+1) # currently split hand is in the next index

    # Assumes you are able to
    # Players can only surrender their first hand.
    # Players cannot surrender after a split
    def surrender(self, player: Player):
        """Simulates a player who surrenders. Does not give any money."""
        player.surrendered = True
        return

    def payout(self):
        # all possible payouts:

        # took insurance and won
        # which hand doubled and won
        # surrendered (CANNOT surrender a split hand)
        # flat out won
        # surr

        pass

    def play_n_rounds(self, n: int):
        """Returns a dataframe detailing each player's bankroll per hand played"""

        for round in range(n):

            self.reset_table() # player current bet is updated here
            self.all_players_make_inital_bet()
            self.deal_initial_round()
            self.insurance()

            for player in self.player_list:
                if player:
                    self.play_turn(player) # action = player.get_action()

            # must do seperately so dealer finishes turn
            for player in self.player_list:
                self.payout(player) # This is the ONLY place where money will be given to player


    # STILL IMPLEMENTING
    # DOES NOT WORK!! DO NOT CALL
    def play_turn(self, player, hand_index=None):
        """
        Player should already have 2 cards in their hands[0] before calling this

        Updates the game state by setting all player object states accordingly,
        and ONLY subtracts from the players bankroll. Should a player bankrupt,
        They will be removed from the table and added to the bankrupt player list
        """
        player.num_hands_played+=1
        # GARUNTEES a valid action always returns a valid action.
        action = self.get_player_action(player, hand_index) # hand_index is None unless its a split

        if action == 'STAND':
            player.curr_hand += 1
            return

        if action == 'HIT':
            self.hit(player, hand_index)
            return

        if action == 'DOUBLE':
            self.double(player, hand_index)
            player.curr_hand += 1
            return

        if action == 'SURRENDER':
            self.surrender(player)
            player.curr_hand += 1
            return

        if action == 'SPLIT':
            if hand_index == None:
                hand_index = 0

            self.split(player, hand_index)

            # imagine the scenerio [<Hand [6s, 6d]>, <Hand [6s, 8d]>]
            # becoming [<Hand [6s, 7d]>, <Hand [6s, kd]>, <Hand [6s, 8s]>]
            self.play_turn(player, player.curr_hand)
            # something is probably wrong here
            self.play_turn(player, player.curr_hand) # Accounts for the index after nested recursive splits.

            return

        raise GameLogicError(f'This line should never be reached! oopsies... Printing game state: {self}')


    # actions_queue is a priority queue of all optimal actions for the player
    # This function does not take Insurance into account. Insurance is a side bet
    # and should be handled on it's own

    # Returns [] if no action
    # otherwise the returned action list can contain following strings:
    # HIT
    # STAND
    # DOUBLE
    # SPLIT
    # SURRENDER
    # SPLIT_DAS (SPLIT but ONLY if double_after_split is allowed)

    # STILL IMPLEMENTING
    def validate_actions(self, optimal_actions, player, hand_index=None):
        """
        Removes all invalid actions in the actions_queue based
        on rules and game state

        The head of the actions_queue, after being passed into this function,
        will be the optimal play allowable.
        This method considers all the allowable toggles in the rule_set along
        with the current state of the player's hand
        """

        invalid_actions = []
        hand = player.get_hand(hand_index) # needed for ace things

        # all hands
        if not self.rules.late_surrender:
            invalid_actions.append('SURRENDER')

        if not self.rules.double_after_split:
            invalid_actions.append('SPLIT_DAS')

        # currently split hands
        if hand_index != None: # required for when hand_index=0 since 0 is falsy

            # can never surrender on a split hand
            invalid_actions.append('SURRENDER')

            # cant split anymore
            if player.times_split >= 3:
                invalid_actions.append('SPLIT')
                invalid_actions.append('SPLIT_DAS')

            if not self.rules.double_after_split:
                invalid_actions.append('DOUBLE')

            # occurs on a split ace (CANNOT simply ask if hand contains an ace)
            if hand.hand[0].card_face == 'A':
                invalid_actions.append('DOUBLE') # can never double a split ace

                # cant hit split aces
                if not self.rules.hit_split_aces:
                    invalid_actions.append('HIT')

                # cant resplit aces
                if not self.rules.resplit_aces:
                    invalid_actions.append('SPLIT')

        # removes everything in invaid_actions from optimal actions
        for invalid_action in invalid_actions:
            while (invalid_action in optimal_actions):
                optimal_actions.remove(invalid_action)

        # happens when both surrender and split are filtered out from pairs
        # pairs can be aces.
        # can no longer: split,
        if optimal_actions == []:
            hand_type, hand_value = hand.get_hand_value()

            # Edge case. Soft 12 that cant split, double, or surrender.
            # We only want to know if we should hit or stand at this point.
            if hand.hand[0].card_face == 'A':
                if self.rules.hit_split_aces:
                    return ['HIT']
                return ['STAND']

            # all other pairs are beyond this point
            # therefore, treat as hard hands and refilter
            hand_type, hand_value = hand.get_hand_value()
            if hand_value == 'K' or  hand_value == 'Q' or  hand_value == 'J':
                 hand_value = '10'
            hand_type = 'hard'
            hand_value = str(2*int(hand_value))
            new_optimal_actions = self.strategy[hand_type][(hand_value, self.dealer.get_up_card().card_face)]

            new_invalid_actions = []
            if not self.rules.double_after_split:
                new_invalid_actions.append('DOUBLE')
            if not self.rules.late_surrender:
                new_invalid_actions.append('SURRENDER')

            # removes everything in new_invalid_actions from new_optimal_actions
            for new_invalid_action in new_invalid_actions:
                while (new_invalid_action in new_optimal_actions):
                    new_optimal_actions.remove(new_invalid_action)
            return new_optimal_actions

        if optimal_actions == []:
            raise GameLogicError(f'validate_actions method incorrectly filtered out current hand. Hand: {hand}, player: {player}')

        if optimal_actions[0] == 'SPLIT_DAS': # split if double after split allowed
            return ['SPLIT']

        return optimal_actions

        # Implementation notes:
            #
            # Actions that can NEVER happen (always filter out):
            #
            # Double a split ace
                # No casino allows this. Should they allow it, players could
                # generate enough EV to be profitable using only basic strategy.
                # If a casino did allow it, there would be other rules that would
                # off-set this difference in EV like Blackjack pays 6:5
            # Split more than 3 times
                # I'm hard coding this one in. Could change this later, but
                # would have to update edge calc and add more things to GUI
            # Player can never surrender a split hand

            # Toggleable actions to filter out with respect to the game's rules:
            #
            # Late surrender is allowed or not
            # Double after split is allowed or not
            # stand_on_soft_17 vs hit_on_soft_17 (if the object is a dealer)
            # Resplitting aces is allowed or not
            # Hitting a split ace is allowed or not


    def get_dealer_action(self):
        """returns string representing the next action of the dealer"""

        hand_type, hand_value = self.dealer.hand.get_hand_value()

        hand_value = int(hand_value)

        if hand_type == 'pair':
            hand_value = 2*hand_value

        if hand_value < 17:
            return 'HIT'

        if hand_value > 17:
            return 'STAND'

        # 17 cant be a pair
        if hand_value == 17:
            if hand_type == 'hard':
                return 'STAND'
            if self.rules.stand_on_soft_17:
                return 'STAND'
            return 'HIT'
        raise GameLogicError(f'Dealer action incorrectly determined: printing game state: {self}')

    # All possible returned strings:
        # HIT
        # STAND
        # DOUBLE
        # SURRENDER
        # SPLIT
    def get_player_action(self, player, hand_index=None): # hand_index is no longer none on splits
        """
        Returns the optimal action this player should make.
        The action is GUARANTEED to be valid.

        hand_index represents the hand currently being played.
        """

        hand = player.get_hand(hand_index)
        hand_type, hand_value = hand.get_hand_value()

        optimal_actions = self.strategy[hand_type][(hand_value, self.dealer.get_up_card().card_face)]
        # optimal_actions.insert(0, self.deviations())
        best_actions = self.validate_actions(optimal_actions, player, hand_index)

        return best_actions[0]
