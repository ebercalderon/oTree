import random
from otree.api import *

doc = """
Juego de donación de órganos
"""

class C(BaseConstants):
    NAME_IN_URL = 'organ_donation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 20
    CHANGE_COST = cu(0.75)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    donaciones = models.IntegerField(initial=0)


class Player(BasePlayer):
    caso = models.CharField()
    round_number = models.IntegerField(initial=0)
    periodos_en_lista = models.IntegerField(initial=0)
    organo_a_funcional = models.BooleanField(initial=True)
    organo_b_funcional = models.BooleanField(initial=True)
    es_donante = models.BooleanField(initial=False)
    donacion_previa = models.BooleanField(initial=False)
    en_lista_espera = models.BooleanField(initial=False)
    fuera_de_juego = models.BooleanField(initial=False)


# FUNCTIONS

def ElegirDonar(p: Player):
    g = p.group
    if p.es_donante:
        g.donaciones += 1
        if p.round_number <= 10:
            p.payoff -= C.CHANGE_COST


def SimularCaso(p: Player):
    g = p.group
    caso = random.choices(['A', 'B', 'C'], [0.10, 0.20, 0.70])[0]
    p.caso = caso

    if caso == 'A':
        p.organo_a_funcional = False
        p.fuera_de_juego = True
    elif caso == 'B':
        if p.donacion_previa:
            p.fuera_de_juego = True
        else:
            p.organo_b_funcional = False
            p.en_lista_espera = True
    else:
        #p.organo_a_funcional = True
        #p.organo_b_funcional = True
        p.payoff += 3


def EvaluarLista(p: Player):
    g = p.group

    if g.donaciones > 0:
        g.donaciones -= 1
        p.donacion_previa = True
        p.periodos_en_lista = 0

    if p.periodos_en_lista >= 5:
        p.fuera_de_juego = True
    
    p.periodos_en_lista += 1


# PAGES

class Donacion(Page):
    timeout_seconds = 15
    form_model = 'player'
    form_fields = ['es_donante']

    @staticmethod
    def is_displayed(p: Player):
        return p.round_number == 1

    @staticmethod
    def before_next_page(p: Player, timeout_happened):
        ElegirDonar(p)


class Simulacion(Page):
    timeout_seconds = 5

    @staticmethod
    def is_displayed(p: Player):
        return not p.en_lista_espera and not p.fuera_de_juego
    
    @staticmethod
    def before_next_page(p: Player, timeout_happened):
        SimularCaso(p)


class ListaEspera(Page):
    timeout_seconds = 5

    @staticmethod
    def is_displayed(p: Player):
        return p.en_lista_espera and not p.fuera_de_juego
    
    @staticmethod
    def before_next_page(p: Player, timeout_happened):
        EvaluarLista(p)


class Espera(WaitPage):
    pass


class FinRonda(Page):
    timeout_seconds = 5

    @staticmethod
    def is_displayed(p: Player):
        return p.fuera_de_juego


page_sequence = [
    Donacion,
    Espera,
    Simulacion,
    ListaEspera,
    FinRonda
]
