from defines import *


class Card:
    def __init__(self):
        self.name = "."
        self.coin = 0
        self.card_types = set([CardType.NULL])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def action(self, state):
        """
        Parameters
        ----------
        state: GameState
            current game state
        """
        pass


class CopperCard(Card):
    def __init__(self):
        self.name = "1"
        self.coin = 1
        self.card_types = set([CardType.TREASURE])


class SilverCard(Card):
    def __init__(self):
        self.name = "2"
        self.coin = 2
        self.card_types = set([CardType.TREASURE])


class GoldCard(Card):
    def __init__(self):
        self.name = "3"
        self.coin = 3
        self.card_types = set([CardType.TREASURE])


class EstateCard(Card):
    def __init__(self):
        self.name = "E"
        self.coin = 0
        self.card_types = set([CardType.TREASURE])


class DuchyCard(Card):
    def __init__(self):
        self.name = "D"
        self.coin = 0
        self.card_types = set([CardType.TREASURE])


class ProvinceCard(Card):
    def __init__(self):
        self.name = "P"
        self.coin = 0
        self.card_types = set([CardType.TREASURE])


class SmithyCard(Card):
    def __init__(self):
        self.name = "S"
        self.coin = 0
        self.plus_draw = 3
        self.card_types = set([CardType.ACTION])

    def action(self, state):
        common_basic_action(self, state.player)


def common_basic_action(card, player):
    for _ in range(card.plus_draw):
        player.draw()
