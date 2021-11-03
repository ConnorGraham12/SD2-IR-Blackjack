
from player import Player
from blackjack_hi_low import Table
from hand import Hand
from card import Card


player1 = Player(69, 3000, 50)

print(f"type(player1.betting_unit): {type(player1.betting_unit)}")
print(f"player1.betting_unit: {player1.betting_unit}")

print(f"type(player1.curr_bet): {type(player1.curr_bet)}")
print(f"player1.curr_bet: {player1.curr_bet}")

print(f"type(player1.get_what_to_bet(3)): {type(player1.get_what_to_bet(3))}")
print(f"player1.curr_bet: {player1.curr_bet}")
