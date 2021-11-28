import math

# refer to 'kelly_math' under 'whiteboards'
def calc_kelly_frac(ror):
    """Returns the fraction of the kellybet to place given a risk of ruin"""
    if ror == 0:
        ror = 0.0000001
    return -2/(math.log(ror))

def calc_full_kelly(advantage, sttdev):
    return advantage / sttdev**2

    # ror is the decimal value of risk of ruin
def kelly_fractional_bet(advantage, sttdev, ror):
    """returns a float representing the ammount of total bankroll which should be bet"""
    return calc_kelly_frac(ror) * calc_full_kelly(advantage, sttdev)
