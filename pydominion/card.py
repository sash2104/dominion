from pydominion.defines import *


class Card:
    def __init__(self):
        self.name = "."
        self.coin = 0
        self.card_types = set([CardType.NULL])
        self.init()

    def init(self):
        pass

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

    def get_coins(self, state):
        """ Return coins of the card when it has played in buy phase
        Parameters
        ----------
        state: GameState
            current game state
        """
        return self.coin


class CopperCard(Card):
    def init(self):
        self.name = "Copper"
        self.coin = 1
        self.card_types = set([CardType.TREASURE])


class SilverCard(Card):
    def init(self):
        self.name = "Silver"
        self.coin = 2
        self.card_types = set([CardType.TREASURE])


class GoldCard(Card):
    def init(self):
        self.name = "Gold"
        self.coin = 3
        self.card_types = set([CardType.TREASURE])


class EstateCard(Card):
    def init(self):
        self.name = "Estate"
        self.card_types = set([CardType.TREASURE])


class DuchyCard(Card):
    def init(self):
        self.name = "Duchy"
        self.card_types = set([CardType.TREASURE])


class ProvinceCard(Card):
    def init(self):
        self.name = "Province"
        self.card_types = set([CardType.TREASURE])


class MiserCard(Card):
    def init(self):
        self.name = "Miser"
        self.card_types = set([CardType.ACTION])

    def action(self, state):
        player = state.turn_player
        options = [
            "Put a Copper from your hand onto your Tavern mat",
            "+$1 per Copper on your Tavern mat"]
        option = player.agent.select(state, "Miser", options)
        if option == options[0]:
            # Put a Copper from the player's hand onto her Tavern mat
            for card in player.hand:
                print(card.name, card.__class__)
                if card.name == "Copper":
                    # copper
                    player.hand.remove(card)
                    player.tavern_mat.append(card)
                    player.num_copper_on_tavern_mat += 1
                    break
        else:
            # +$1 per Copper on the player's Tavern mat
            player.coin += player.num_copper_on_tavern_mat


class SmithyCard(Card):
    def init(self):
        self.name = "Smithy"
        self.plus_draw = 3
        self.card_types = set([CardType.ACTION])

    def action(self, state):
        common_basic_action(self, state.turn_player)


def common_basic_action(card, player):
    for _ in range(card.plus_draw):
        player.draw()
