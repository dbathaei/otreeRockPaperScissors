from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'RPS_Goodlooking'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = random.randint(10,24)
    PAYOFF_WIN = 1
    PAYOFF_DRAW = 0
    PAYOFF_LOSE = -1

    FINAL_DECISION_VALUE = random.randint(1,2)
    CHOICES = [
                ["Rock", "Rock"],
                ["Paper", "Paper"],
                ["Scissor", "Scissor"]
            ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.StringField(
            label = "Rock? Paper? or Scissors? Hmm? Say it. Which one? Hmm?",
            widget = widgets.RadioSelectHorizontal,
            choices = C.CHOICES
        )


# PAGES
class MyPage(Page):
    timeout_seconds = 10
    form_model = "player"
    form_fields = ["choice"]
    
    @staticmethod #Method to set choice if player doesn't pick.
    def before_next_page(player: Player, timeout_happened):
        if timeout_happened:
            player.choice = random.choice(C.CHOICES)[0]

class ResultsWaitPage(WaitPage):
    @staticmethod #Method to distribute payoffs
    def after_all_players_arrive(group: Group):
        player_list = group.get_players()
        p1 = player_list[0]
        p2 = player_list[1]

        if p1.choice == p2.choice:
            p1.payoff += C.PAYOFF_DRAW
            p2.payoff += C.PAYOFF_DRAW
        elif p1.choice == "Rock":
            if p2.choice == "Scissor":
                p1.payoff += C.PAYOFF_WIN
                p2.payoff += C.PAYOFF_LOSE
            else:
                p1.payoff += C.PAYOFF_LOSE
                p2.payoff += C.PAYOFF_WIN
        elif p1.choice == "Scissor":
            if p2.choice == "Rock":
                p1.payoff += C.PAYOFF_LOSE
                p2.payoff += C.PAYOFF_WIN
            else:
                p1.payoff += C.PAYOFF_WIN
                p2.payoff += C.PAYOFF_LOSE
        else:
            if p2.choice == "Rock":
                p1.payoff += C.PAYOFF_WIN
                p2.payoff += C.PAYOFF_LOSE
            else:
                p1.payoff += C.PAYOFF_LOSE
                p2.payoff += C.PAYOFF_WIN


class Results(Page):
    timeout_seconds = 10

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == C.NUM_ROUNDS:
            if C.FINAL_DECISION_VALUE == 1:
                if player.id_in_group == 1:
                    player.payoff = 100
                else:
                    player.payoff = 0
            else:
                if player.id_in_group == 2:
                    player.payoff = 100
                else:
                    player.payoff = 0
        else:
            pass


class LastRoundPage(Page):

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == C.NUM_ROUNDS:
            return True
        else:
            return False


page_sequence = [MyPage, ResultsWaitPage, Results, LastRoundPage]
