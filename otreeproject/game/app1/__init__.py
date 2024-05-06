from otree.api import *
import random

from otree.models import player

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'app1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 8



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.LongStringField()
    money = models.FloatField()
    a1_number = models.PositiveIntegerField(default=0, max=5, label="Стоимость для Вас 100")
    a2_number = models.PositiveIntegerField(default=0, max=5, label="Стоимость для Вас 200")
    a3_number = models.PositiveIntegerField(default=0, max=5, label="Стоимость для Вас 250")
    a4_number = models.PositiveIntegerField(default=0, max=5, label="Стоимость для Вас 400")
    a5_number = models.PositiveIntegerField(default=0, max=5, label="Стоимость для Вас 450")
    total_profit = models.IntegerField()
    profit = models.IntegerField()
    a1_price = models.FloatField()
    a2_price = models.FloatField()
    a3_price = models.FloatField()
    a4_price = models.FloatField()
    a5_price = models.FloatField()
    wrong = models.BooleanField
    c1 = models.FloatField()
    c2 = models.FloatField()
    c3 = models.FloatField()
    c4 = models.FloatField()
    c5 = models.FloatField()
    b1 = models.IntegerField()
    b2 = models.IntegerField()
    b3 = models.IntegerField()
    b4 = models.IntegerField()
    b5 = models.IntegerField()






A = [10, 20, 30, 40, 50]
B = [0, 0, 0, 0, 0]
C_ = [0, 0, 0, 0, 0]
Costs = [100, 200, 250, 400, 450]



# PAGES
class zero_page(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    form_model = 'player'
    form_fields = ['name']
    player.money = 200


total_profit = 0
class first_round(Page):
    form_model = 'player'
    form_fields = ['a1_number', 'a2_number', 'a3_number', 'a4_number', 'a5_number']





    @staticmethod
    def vars_for_template(player):
        if player.round_number == 1:
            player.money = 1000
            player.b1 = 0
            player.b2 = 0
            player.b3 = 0
            player.b4 = 0
            player.b5 = 0
        else:
            prev_player = player.in_round(player.round_number - 1)
            player.money = prev_player.money
            player.b1 = prev_player.b1
            player.b2 = prev_player.b2
            player.b3 = prev_player.b3
            player.b4 = prev_player.b4
            player.b5 = prev_player.b5
        player.a1_price = max(round(A[0], 1), 0)
        player.a2_price = max(round(A[1], 1), 0)
        player.a3_price = max(round(A[2], 1), 0)
        player.a4_price = max(round(A[3], 1), 0)
        player.a5_price = max(round(A[4], 1), 0)


        return {
                'цена на а1:': player.a1_price,
                'цена на а2:': player.a2_price,
                'цена на а3:': player.a3_price,
                'цена на а4:': player.a4_price,
                'цена на а5:': player.a5_price,
                'player.money_for_round': player.money,
                'player.status': player.wrong
                }






class Profit(Page):
    @staticmethod
    def vars_for_template(player):
        player.wrong = False
        check = player.a1_number * player.a1_price + player.a2_number * player.a2_price + player.a3_number * player.a3_price + player.a4_number * player.a4_price + player.a5_number * player.a5_price
        if player.money < check:
            player.wrong = True
            check = 0
        player.profit = 0
        if player.wrong:
            n = 0
        else:
            n = player.a1_number * Costs[0] + player.a2_number * Costs[1] + player.a3_number * Costs[2] + player.a4_number * Costs[3] + player.a5_number * Costs[4]
        player.money = player.money - check
        player.profit += n
        player_list = player.in_previous_rounds()
        player.total_profit = n
        for player_ in player_list:
            player.total_profit += player_.profit
        return {
            'profit': player.profit
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        B = [0, 0, 0, 0, 0]
        if player.wrong is not True:
            B[0] += player.a1_number
            B[1] += player.a2_number
            B[2] += player.a3_number
            B[3] += player.a4_number
            B[4] += player.a5_number
        for guys in player.get_others_in_group():
            B[0] += guys.a1_number
            B[1] += guys.a2_number
            B[2] += guys.a3_number
            B[3] += guys.a4_number
            B[4] += guys.a5_number
        player.b1 = B[0]
        player.b2 = B[1]
        player.b3 = B[2]
        player.b4 = B[3]
        player.b5 = B[4]


        people = len(player.get_others_in_group()) + 1

        if player.round_number == 1:
            player.c1 = 0
            player.c2 = 0
            player.c3 = 0
            player.c4 = 0
            player.c5 = 0
        else:
            prev_player = player.in_round(player.round_number - 1)
            C_[0] = prev_player.c1
            C_[1] = prev_player.c2
            C_[2] = prev_player.c3
            C_[3] = prev_player.c4
            C_[4] = prev_player.c5



        player.c1 = B[0] * people - C_[0]
        player.c2 = B[1] * people - C_[1]
        player.c3 = B[2] * people - C_[2]
        player.c4 = B[3] * people - C_[3]
        player.c5 = B[4] * people - C_[4]


        A[0] = player.a1_price * (1 + player.c1/100)
        A[1] = player.a2_price * (1 + player.c2/100)
        A[2] = player.a3_price * (1 + player.c3/100)
        A[3] = player.a4_price * (1 + player.c4/100)
        A[4] = player.a5_price * (1 + player.c5/100)










class WaitingPage(WaitPage):
    pass

class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player):
        return {
            'profit': player.total_profit
        }





page_sequence = [zero_page, WaitingPage, first_round, WaitingPage, Profit, WaitingPage, Results]
