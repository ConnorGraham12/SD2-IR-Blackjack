from blackjack_hi_low import Table
from player import Player
from dealer import Dealer
from card import Card
from hand import Hand
import matplotlib
import matplotlib.pyplot
import numpy

def profit_percent(begin_ammount, end_ammount):
    return ((end_ammount - begin_ammount) / begin_ammount) * 100

def get_player_average_bankroll(player_list):
    avg = 0
    total = 0
    num_players = 0
    for player in player_list:
        if player:
            total += player.stack_size
            num_players += 1

    return total / len(player_list)

def num_players_in_game(game):
    total = 0
    for player in game.player_list:
        if player:
            total +=1
    total += len(game.bankrupt_players)
    return total



num_decks = 8
deck_pen = 0.75
min_bet = 10
max_bet = 1000

total_rounds_played = 15000
start_stack_size = 50000
betting_units = 200
num_bins = 500

game = Table(num_decks, deck_pen, min_bet, max_bet)
player_list = []

player_list.append(Player(0, start_stack_size, betting_units, '1-12'))
player_list[0].take_seat(0, game)


# ONLY WORKS WHEN 1 PLAYER IS SITTING AND MUST BE IN SEAT INDEX ZERO!!!
# (hotfix for demo)
bankroll_over_time = game.play_n_rounds(total_rounds_played, num_bins)
rounds = numpy.linspace(0, total_rounds_played, retstep=True, num=num_bins, dtype=int, axis=0)
print("bak_roll = " + str((bankroll_over_time)))
# print("rounds[0]_len = " + str((rounds[0])))
matplotlib.pyplot.scatter(rounds[0], bankroll_over_time)
matplotlib.pyplot.xlabel("rounds")
matplotlib.pyplot.ylabel("bankroll")
matplotlib.pyplot.show(block=True)
print(game)

avg_end_stack = get_player_average_bankroll(player_list)


print(f"\nTotal rounds played: {total_rounds_played}")
print(f"Total hands played: {game.num_hands_played}\n")

print(f"Average stack is ${round(avg_end_stack)}\n")
print(f"Which leads to an average change of {round(profit_percent(start_stack_size, avg_end_stack), 2)}%")
# this number is only correct is nobody bankrupts
num_players_in_game = num_players_in_game(game)
print(f"Profit in dollars per hand: {(avg_end_stack*num_players_in_game - start_stack_size*num_players_in_game) / (game.num_hands_played/num_players_in_game)}")
