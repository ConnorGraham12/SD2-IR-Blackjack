import math

# NOTE
#   The edge calculator is only accurate to one or two sig figs!

class RuleSet:
    def __init__(self,
                num_decks: int,
                penetration: float,
                min_bet: int,
                max_bet: int,

                insurance=False,
                late_surrender=False,
                double_after_split=False,
                stand_on_soft_17=False,
                resplit_aces=False,
                hit_split_aces=False,
                ):

        # needed for gameplay logic
        self.num_decks = num_decks
        self.penetration = penetration
        self.min_bet = min_bet
        self.max_bet = max_bet

        # maybe just always allow insurance for consistant EV calulations?
        self.insurance = insurance

        self.late_surrender = late_surrender
        self.double_after_split = double_after_split
        self.stand_on_soft_17 = stand_on_soft_17
        self.resplit_aces = resplit_aces
        self.hit_split_aces = hit_split_aces

        # needed to calculate kelly bets
        # Thank you Connor for the get_stats function
        tmp = RuleSet.get_stats(
            num_decks,
            insurance,
            late_surrender,
            double_after_split,
            stand_on_soft_17,
            resplit_aces,
            hit_split_aces
        )
        self.base_house_edge = tmp[0]/100 # need decimal form
        self.stddev = tmp[1]

    def __str__(self):
        retval = f"insurance: {self.insurance}\n"
        retval += f"late_surrender: {self.late_surrender}\n"
        retval += f"double_after_split: {self.double_after_split}\n"
        retval += f"stand_on_soft_17: {self.stand_on_soft_17}\n"
        retval += f"resplit_aces: {self.resplit_aces}\n\n"
        retval += f"hit_split_aces: {self.hit_split_aces}"

        retval += f"base_player_edge: {self.base_house_edge}\n"
        retval += f"variance: {self.stddev**2}"

        return retval

    # returns [houseEdge, stanDev]
    @staticmethod
    def get_stats(
            num_decks: int,
            insurance: bool,
            late_surrender: bool,
            double_after_split: bool,
            stand_on_soft_17: bool,
            resplit_aces: bool,
            hit_split_aces: bool,
            ):
        """Returns a list of floats representing house edge and standard deviation for this games set of rules"""

        #Variables
        decks = 0
        if num_decks == 4:
            decks = 2
        elif num_decks == 6:
            decks = 4
        elif num_decks == 8:
            decks = 5
        else:
            raise ValueError('Only supports 4, 6, and 8 decks')
        # Number of decks
        # 0 = 1 Deck(s)
        # 1 = 2 Deck(s)
        # 2 = 4 Deck(s)
        # 3 = 5 Deck(s)
        # 4 = 6 Deck(s)
        # 5 = 8 Deck(s)

        double = [1,0,0,0,double_after_split]
        # [0] Double on Any two cards
        # [1] Double on hard 9/11
        # [2] Double on hard 10/11
        # [3] Double on hard/soft 9/11
        # [4] Double after Split

        resplits = [0,1,0,0]
        # [0] No Resplits
        # [1] Respltis to 3 hands
        # [2] Resplit to 4 hands
        # [3] Respit aces

        bj = [1,0,0,0,0,0]
        #   Blackjack Pays 3:2
        #   Blackjack Pays 1:1
        #   Blackjack Pays 6:5
        #   Blackjack Pays 7:5
        #   Blackjack Pays 2:1
        #   Suited BJ Pays 2:1

        # Hit Split Aces
        if hit_split_aces:
            hitAces = 1
        else:
            hitAces = 0

        split4 = 0 # Cannot split 4s 5s & 10s

        # disgusting, I know. But it works okay
        noSplitAces = not resplit_aces # Cannot split Aces

        if stand_on_soft_17:
            h17 = [1,0]
        else:
            h17 = [0,1]
        # [0] Stand on soft 17
        # [1] Hit on soft 17

        peek = [1,0,0,0,0]
        # [0] Dealer Peeks For BJ
        # [1] Dealer Does Not Peek For BJ
        # [2] Dealer Peeks on Ace
        # [3] Dealer Peeks on Ten
        # [4] Playtech Peek (split bets lost)

        if late_surrender:
            surrender = [0,1,0,0]
        else:
            surrender = [1,0,0,0]
        # [0] No surrender
        # [1] Late (Standard) Surrender
        # [2] Early Surrender Against 10
        # [3] Full Early Surrender

        charlie = [1,0,0,0,0,0]
        # [0] No #-card Bonus
        # [1] 5-Card 21 Pays 2:1
        # [2] 5+-Card 21 Pays 2:1
        # [3] 5-Card Charlie
        # [4] 6-Card Charlie
        # [5] 7-Card Charlie

        shuffle = 0 #Shuffle After Each Hand
        cd = 0      #Use CD Exceptions
        sevens = 0  #777 Pays 3:1

        dv = {}
        #                  1       2      4       5       6       8      12        Decks
        dv["ddecks"] = [0.114, -0.237, -0.405, -0.438, -0.460, -0.488, -0.515]	# Default
        dv["h17"] = [-0.188, -0.201, -0.209, -0.211, -0.212, -0.213, -0.214]	# h17
        dv["nopeek"] = [-0.106, -0.106, -0.108, -0.109, -0.109, -0.109, -0.109]	# No Peek
        dv["apeek"] = [-0.097, -0.097, -0.099, -0.100, -0.100, -0.100, -0.100]	# Peek on Ace
        dv["tpeek"] = [-0.009, -0.009, -0.009, -0.009, -0.009, -0.009, -0.009]	# Peek on Ten
        dv["ppeek"] = [-0.027, -0.027, -0.027, -0.027, -0.027, -0.027, -0.027]	# Playtech Peek
        dv["d911"] = [-0.144, -0.111, -0.099, -0.097, -0.095, -0.093, -0.091]	# Double on 9-11
        dv["d911nodas"] = [-0.136, -0.105, -0.093, -0.091, -0.089, -0.087, -0.085]	# Double on 9-11, no DAS
        dv["d911h17"] = [-0.009, -0.009, -0.009, -0.009, -0.010, -0.010, -0.010]	# Double on 9-11, H17
        dv["ds911h17"] = [0.002, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]	# Double on soft 9-11, H17
        dv["d1011"] = [-0.287, -0.225, -0.198, -0.193, -0.189, -0.185, -0.181]	# Double on 10-11
        dv["d1011h17"] = [-0.009, -0.009, -0.009, -0.009, -0.010, -0.010, -0.010]	# Double on 9-11, H17
        dv["d1011nodas"] = [-0.268, -0.207, -0.181, -0.177, -0.173, -0.170, -0.167]	# Double on 10-11, no DAS
        dv["resplit3"] = [0.028, 0.039, 0.044, 0.045, 0.045, 0.046, 0.047]	# Resplit to 3 Hands, DAS
        dv["resplit4"] = [0.030, 0.045, 0.052, 0.053, 0.054, 0.055, 0.056]	# Resplit to 4 Hands, DAS
        dv["nodas"] = [-0.129, -0.125, -0.123, -0.122, -0.122, -0.121, -0.121]	# No Double After Split No Resplits
        dv["nodas3"] = [-0.109, -0.100, -0.094, -0.091, -0.092, -0.091, -0.091]	# No Double After Split Resplit to 3 Hands
        dv["nodas4"] = [-0.108, -0.098, -0.091, -0.088, -0.087, -0.086, -0.085]	# No Double After Split Resplit to 4 Hands
        dv["hitaces"] = [0.142, 0.168, 0.183, 0.185, 0.187, 0.190, 0.193]	# Draw to Split Aces
        dv["hitaces3"] = [-0.006, -0.007, -0.007, -0.007, -0.007, -0.007, -0.007]	# Draw to Split Aces, Resplit Aces
        dv["hitaces4"] = [-0.007, -0.008, -0.009, -0.009, -0.009, -0.009, -0.009]	# Draw to Split Aces, Resplit Aces
        dv["hitacesnodas"] = [0.130, 0.160, 0.175, 0.178, 0.181, 0.183, 0.185]	# Draw to Split Aces, No DAS
        dv["hitacesh17"] = [-0.001, -0.001, -0.002, -0.002, -0.002, -0.003, -0.003]	# Draw to Split Aces & H17
        dv["resplitanp3"] = [-0.003, -0.004, -0.005, -0.006, -0.007, -0.008, -0.009]	# Resplit Aces & No Peek
        dv["resplitanp4"] = [-0.003, -0.004, -0.005, -0.006, -0.007, -0.008, -0.009]	# Resplit Aces & No Peek
        dv["hitacesnp"] = [-0.004, -0.006, -0.008, -0.008, -0.008, -0.008, -0.008]	# Draw to Split Aces & No Peek
        dv["hitacesnsd"] = [-0.011, -0.008, -0.007, -0.007, -0.007, -0.007, -0.007]	# Draw to Split Aces & No Soft Double || No Double Spilt Aces
        dv["resplita3"] = [0.031, 0.047, 0.055, 0.057, 0.058, 0.059, 0.060]	# Resplit to 3 Hands, Aces
        dv["resplita4"] = [0.032, 0.053, 0.065, 0.067, 0.068, 0.070, 0.072]	# Resplit to 4 Hands, Aces
        dv["lates17"] = [0.022, 0.053, 0.069, 0.072, 0.075, 0.077, 0.079]	# Late Surrender S17
        dv["lateh17"] = [0.038, 0.066, 0.082, 0.086, 0.088, 0.091, 0.094]	# Late Surrender H17
        dv["earlys17"] = [0.626, 0.631, 0.634, 0.634, 0.634, 0.635, 0.635]	# Early Surrender S17
        dv["earlyh17"] = [0.700, 0.710, 0.715, 0.716, 0.717, 0.718, 0.719]	# Early Surrender H17
        dv["earlys10"] = [0.190, 0.220, 0.233, 0.234, 0.238, 0.238, 0.238]	# Early Surrender vs 10
        dv["charlie5"] = [1.171, 1.334, 1.416, 1.430, 1.444, 1.458, 1.452]	# 5 Card Charlie
        dv["charlie6"] = [0.125, 0.146, 0.156, 0.158, 0.160, 0.162, 0.164]	# 6 Card Charlie
        dv["charlie7"] = [0.007, 0.008, 0.009, 0.010, 0.010, 0.010, 0.010]	# 7 Card Charlie
        dv["card5"] = [0.162, 0.181, 0.193, 0.195, 0.197, 0.199, 0.201]	# 5 Card 21
        dv["card5p"] = [0.194, 0.221, 0.234, 0.236, 0.239, 0.241, 0.243]	# 5+ Card 21
        dv["sevens"] = [0.030, 0.049, 0.059, 0.061, 0.063, 0.064, 0.065]	# 777 pays 3:1
        dv["sbj21"] = [0.581, 0.572, 0.568, 0.567, 0.567, 0.566, 0.565]	# Suited blackjack pays 2:1
        dv["bj21"] = [2.325, 2.289, 2.272, 2.268, 2.266, 2.263, 2.260]	# blackjack pays 2:1
        dv["bj75"] = [-0.465, -0.458, -0.454, -0.454, -0.453, -0.453, -0.453]	# blackjack pays 7:5
        dv["bj65"] = [-1.395, -1.372, -1.364, -1.361, -1.360, -1.359, -1.359]	# blackjack pays 6:5
        dv["bj11"] = [-2.325, -2.289, -2.272, -2.268, -2.266, -2.263, -2.2630]	# blackjack pays 1:1
        dv["cds17"] = [0.039, 0.014, 0.005, 0.004, 0.003, 0.002, 0.001]	# CD Exceptions S17
        dv["cdh17"] = [0.036, 0.012, 0.005, 0.003, 0.003, 0.002, 0.001]	# CD Exceptions H17
        dv["shuffle"] = [-0.113, -0.063, -0.034, -0.028, -0.020, -0.014, -0.008]	# No Shuffle
        dv["split4h"] = [-0.008, -0.007, -0.006, -0.006, -0.005, -0.005, -0.005]	# Split 4, H17
        dv["split4s"] = [-0.006, -0.005, -0.004, -0.003, -0.003, -0.003, -0.003]	# Split 4, S17
        dv["splitA"] = [-0.139, -0.166, -0.177, -0.179, -0.181, -0.183, -0.185]	# Cannot Split Aces

        sum = dv["ddecks"][decks]

        if (h17[1] == 1):
            sum += dv["h17"][decks]

        if (peek[1] == 1):
            sum += dv["nopeek"][decks]
        elif (peek[2] == 1):
            sum += dv["apeek"][decks]
        elif (peek[3] == 1):
            sum += dv["tpeek"][decks]
        elif (peek[4] == 1):
            sum += dv["ppeek"][decks]

        if (double[1] == 1):
            if (double[4] == 1):
                sum += dv["d911"][decks]
            else:
                sum += dv["d911nodas"][decks]
            if (h17[1]):
                sum += dv["d911h17"][decks]

        elif (double[2] == 1):
            if (double[4] == 1):
                sum += dv["d1011"][decks]
            else:
                sum += dv["d1011nodas"][decks]
            if (h17[1] == 1):
                sum += dv["d1011h17"][decks]

        elif ((double[3] == 1) and (h17[1] == 1)):
            sum += dv["ds911h17"][decks]

        if ((resplits[1] == 1) and (double[4] == 1)):
            sum += dv["resplit3"][decks]
        elif ((resplits[2] == 1) and (double[4] == 1)):
            sum += dv["resplit4"][decks]
        elif ((resplits[0] == 1) and (double[4] == 0)):
            sum += dv["nodas"][decks]
        elif ((resplits[1] == 1) and (double[4] == 0)):
            sum += dv["nodas3"][decks]
        elif ((resplits[2] == 1) and (double[4] == 0)):
            sum += dv["nodas4"][decks]

        if ((hitAces == 1) and (noSplitAces == 0)):
            if (double[4] == 1):
                sum += dv["hitaces"][decks]
                if ((double[1] == 1) or (double[2] == 1)):
                    sum += dv["hitacesnsd"][decks]

            else:
                sum += dv["hitacesnodas"][decks]
            if ((peek[1] == 1) or (peek[2] == 1)):
                sum += dv["hitacesnp"][decks]
            if (h17[1] == 1):
                sum += dv["hitacesh17"][decks]

        if ((resplits[1] == 1) and (resplits[3] == 1)):
            sum += dv["resplita3"][decks]
            if ((hitAces == 1) and noSplitAces == 0):
                sum += dv["hitaces3"][decks]
            if ((peek[1] == 1) or (peek[2] == 1)):
                sum += dv["resplitanp3"][decks]

        elif ((resplits[2] == 1) and (resplits[3] == 1)):
            sum += dv["resplita4"][decks]
            if ((hitAces == 1) and (noSplitAces == 0)):
                sum += dv["hitaces4"][decks]
            if ((peek[1] == 1) or (peek[2] == 1)):
                sum += dv["resplitanp4"][decks]

        if ((h17[0] == 1) and (surrender[1] == 1)):
            sum += dv["lates17"][decks]
        elif ((h17[1] == 1) and (surrender[1] == 1)):
            sum += dv["lateh17"][decks]
        elif ((h17[0] == 1) and (surrender[3] == 1)):
            sum += dv["earlys17"][decks]
        elif ((h17[1] == 1) and (surrender[3] == 1)):
            sum += dv["earlyh17"][decks]
        elif (surrender[2] == 1):
            sum += dv["earlys10"][decks]

        if (charlie[1] == 1):
            sum += dv["card5"][decks]
        elif (charlie[2] == 1):
            sum += dv["card5p"][decks]
        elif (charlie[3] == 1):
            sum += dv["charlie5"][decks]
        elif (charlie[4] == 1):
            sum += dv["charlie6"][decks]
        elif (charlie[5] == 1):
            sum += dv["charlie7"][decks]

        if (bj[1] == 1):
            sum += dv["bj11"][decks]
        elif (bj[2] == 1):
            sum += dv["bj65"][decks]
        elif (bj[3] == 1):
            sum += dv["bj75"][decks]
        elif (bj[4] == 1):
            sum += dv["bj21"][decks]

        if (bj[5] == 1):
            if (bj[0] == 1):
                sum += dv["sbj21"][decks]
            elif (bj[1] == 1):
                sum += (dv["sbj21"][decks] * 2.0)
            elif (bj[2] == 1):
                sum += (dv["sbj21"][decks] * 1.6)
            elif (bj[3] == 1):
                sum += (dv["sbj21"][decks] * 1.2)

        if ((h17[0] == 1) and (cd == 1)):
            sum += dv["cds17"][decks]
        elif ((h17[1] == 1) and (cd == 1)):
            sum += dv["cdh17"][decks]

        if (shuffle == 0):
            sum += dv["shuffle"][decks]

        if ((h17[0] == 1) and (split4 == 1) and (double[4] == 1)):
            sum += dv["split4s"][decks]
        elif ((h17[1] == 1) and (split4 == 1) and (double[4] == 1)):
            sum += dv["split4h"][decks]

        if (noSplitAces == 1):
            sum += dv["splitA"][decks]

        if (sevens == 1):
            sum += dv["sevens"][decks]


        houseEdge = -sum

        dv2 = {}
        # 1         2       4       5       6       8      12 Dekcs
        dv2["ddecks"] = [1.151, 1.144, 1.140, 1.140, 1.140, 1.140, 1.140]	# Default
        dv2["h17"] = [0.001, 0.005, 0.006, 0.006, 0.006, 0.006, 0.006]	# h17
        dv2["nopeek"] = [-0.022, -0.022, -0.019, -0.019, -0.019, -0.019, -0.019]	# No Peek
        dv2["apeek"] = [-0.020, -0.020, -0.017, -0.017, -0.017, -0.017, -0.017]	# Ace Peek
        dv2["ppeek"] = [-0.003, -0.003, -0.003, -0.003, -0.003, -0.003, -0.003]	# Playtech Peek
        dv2["d911"] = [-0.031, -0.022, -0.022, -0.022, -0.022, -0.022, -0.022]	# Double on 9-11
        dv2["d1011"] = [-0.051, -0.042, -0.039, -0.039, -0.039, -0.039, -0.039]	# Double on 10-11
        dv2["resplit3"] = [0.003, 0.006, 0.007, 0.007, 0.007, 0.007, 0.007]	# Resplit to 3 Hands, DAS
        dv2["resplit4"] = [0.003, 0.006, 0.007, 0.007, 0.007, 0.007, 0.007]	# Resplit to 4 Hands, DAS
        dv2["nodas"] = [-0.013, -0.014, -0.016, -0.016, -0.016, -0.016, -0.016]	# No Double After Split No Resplits
        dv2["resplita3"] = [0.000, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]	# Resplit to 3 Hands, Aces
        dv2["resplita4"] = [0.000, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]	# Resplit to 4 Hands, Aces
        dv2["lates17"] = [-0.011, -0.012, -0.012, -0.012, -0.012, -0.012, -0.012]	# Late Surrender S17
        dv2["lateh17"] = [-0.014, -0.014, -0.015, -0.015, -0.015, -0.015, -0.015]	# Late Surrender H17
        dv2["earlys17"] = [-0.033, -0.033, -0.033, -0.033, -0.033, -0.033, -0.033]	# Early Surrender S17
        dv2["earlyh17"] = [-0.033, -0.033, -0.033, -0.033, -0.033, -0.033, -0.033]	# Early Surrender H17
        dv2["earlys10"] = [-0.018, -0.018, -0.021, -0.021, -0.021, -0.021, -0.021]	# Early Surrender vs 10
        dv2["bj21"] = [0.035, 0.034, 0.034, 0.034, 0.034, 0.034, 0.034]	# blackjack pays 2:1
        dv2["sbj21"] = [0.008, 0.008, 0.008, 0.008, 0.008, 0.008, 0.008]	# suited blackjack pays 2:1
        dv2["bj65"] = [-0.016, -0.016, -0.016, -0.016, -0.016, -0.016, -0.016]	# blackjack pays 6:5
        dv2["bj11"] = [-0.035, -0.034, -0.034, -0.034, -0.034, -0.034, -0.034]	# blackjack pays 1:1

        sum2 = dv2["ddecks"][decks]
        if (h17[1] == 1):
            sum2 += dv2["h17"][decks]

        if (peek[1] == 1):
            sum2 += dv2["nopeek"][decks]
        elif (peek[2] == 1):
            sum2 += dv2["apeek"][decks]
        elif (peek[4] == 1):
            sum2 += dv2["ppeek"][decks]

        if (double[1] == 1):
            sum2 += dv2["d911"][decks]
        elif (double[2] == 1):
            sum2 += dv2["d1011"][decks]

        if (resplits[1] == 1):
            sum2 += dv2["resplit3"][decks]
        elif (resplits[2] == 1):
            sum2 += dv2["resplit4"][decks]

        if (double[4] == 0):
            sum2 += dv2["nodas"][decks]

        if ((resplits[1] == 1) and (resplits[3] == 1)):
            sum2 += dv2["resplita3"][decks]
        elif ((resplits[2] == 1) and (resplits[3] == 1)):
            sum2 += dv2["resplita4"][decks]

        if ((h17[0] == 1) and (surrender[1] == 1)):
            sum2 += dv2["lates17"][decks]
        elif ((h17[1] == 1) and (surrender[1] == 1)):
            sum2 += dv2["lateh17"][decks]
        elif ((h17[0] == 1) and (surrender[3] == 1)):
            sum2 += dv2["earlys17"][decks]
        elif ((h17[1] == 1) and (surrender[3] == 1)):
            sum2 += dv2["earlyh17"][decks]
        elif (surrender[2] == 1):
            sum2 += dv2["earlys10"][decks]

        if (bj[1] == 1):
            sum2 += dv2["bj11"][decks]
        elif (bj[2] == 1):
            sum2 += dv2["bj65"][decks]
        elif (bj[3] == 1):
            sum2 += dv2["bj75"][decks]
        elif (bj[4] == 1):
            sum2 += dv2["bj21"][decks]

        if (bj[5] == 1):
            sum2 += (dv2["bj21"][decks] * 0.25)

        stanDev = sum2

        # dv3 = {}
        # # 1         2       4       5       6     8    12   Decks
        # dv3["ddecks"] = [1.135, 1.130, 1.128, 1.128, 1.128, 1.128, 1.128]	# Default
        # dv3["h17"] = [0.001, 0.003, 0.004, 0.004, 0.004, 0.004, 0.004]	# h17
        # dv3["nopeek"] = [-0.018, -0.018, -0.016, -0.016, -0.016, -0.016, -0.016]	# No Peek
        # dv3["apeek"] = [-0.017, -0.017, -0.015, -0.015, -0.015, -0.015, -0.015]	# Ace Peek
        # dv3["ppeek"] = [-0.002, -0.002, -0.002, -0.002, -0.002, -0.002, -0.002]	# Playtech Peek
        # dv3["d911"] = [-0.022, -0.018, -0.018, -0.018, -0.018, -0.018, -0.018]	# Double on 9-11
        # dv3["d1011"] = [-0.024, -0.020, -0.020, -0.020, -0.020, -0.020, -0.020]	# Double on 10-11
        # dv3["resplit3"] = [0.002, 0.004, 0.005, 0.005, 0.005, 0.005, 0.005]	# Resplit to 3 Hands, DAS
        # dv3["resplit4"] = [0.002, 0.004, 0.005, 0.005, 0.005, 0.0055, 0.005]	# Resplit to 4 Hands, DAS
        # dv3["nodas"] = [-0.009, -0.009, -0.010, -0.010, -0.010, -0.010, -0.010]	# No Double After Split No Resplits
        # dv3["resplita3"] = [0.000, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]	# Resplit to 3 Hands, Aces
        # dv3["resplita4"] = [0.000, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]	# Resplit to 4 Hands, Aces
        # sum3 = dv3["ddecks"][decks]
        # if (h17[1] == 1):
        #     sum3 += dv3["h17"][decks]
        #
        # if (peek[1] == 1):
        #     sum3 += dv3["nopeek"][decks]
        # elif (peek[2] == 1):
        #     sum3 += dv3["apeek"][decks]
        # elif (peek[4] == 1):
        #     sum3 += dv3["ppeek"][decks]
        #
        # if (double[1] == 1 or double[3] == 1):
        #     sum3 += dv3["d911"][decks]
        # elif (double[2] == 1):
        #     sum3 += dv3["d1011"][decks]
        #
        # if (resplits[1] == 1):
        #     sum3 += dv3["resplit3"][decks]
        # elif (resplits[2] == 1):
        #     sum3 += dv3["resplit4"][decks]
        #
        # if (double[4] == 0):
        #     sum3 += dv3["nodas"][decks]
        #
        # if ((resplits[1] == 1) and (resplits[3])):
        #     sum3 += dv3["resplita3"][decks]
        # elif ((resplits[2] == 1) and (resplits[3])):
        #     sum3 += dv3["resplita4"][decks]
        #
        # ratio = sum3
        # ratio2 = math.sqrt(ratio)
        # houseEdge2 = round((-sum / ratio), 3)
        # stanDev2 = round((sum2 / ratio2), 2)

        # print(houseEdgePerHand, houseEdge2PerWager, stanDevPerHand, stanDev2PerWager)
        # Whatever that means

        return [houseEdge, stanDev]
