#!/usr/bin/env python
# coding: utf-8

""" """

import random
import sys
from collections import Counter

from pydominion.agent import CLIAgent
from pydominion.card import *
from pydominion.defines import *


def log(logger, brief, message):
    """ Logging function
    Parameters
    ----------
    brief: str
        Brief message for log
    message: str
        A message to log
    """
    logger.write("[{}] {}\n".format(brief, message))


class Supply:
    def __init__(self):
        self.basic_cards = {"Copper": CopperCard(), "Silver": SilverCard(),
                            "Gold": GoldCard(), "Estate": EstateCard(),
                            "Duchy": DuchyCard(), "Province": ProvinceCard()}
        self.kingdom_cards = {"Smithy": SmithyCard(), "Miser": MiserCard()}
        self.cards = {".": Card()}  # dummy card

        # initialize supply piles
        # WIP: check and add extra cards such as Colony
        self.cards.update(self.basic_cards)
        self.cards.update(self.kingdom_cards)
        print(self.cards)

    def get(self, card_name):
        """ WIP: count down a card
        Returns
        -------
        card: Card
            A card to be bought or gained
        """
        assert(card_name in self.cards)
        return self.cards[card_name]


class Player:
    """
    Attributes
    ----------
    action_pool: dict of {str: list of Card}
        key is card name, value is the Cards of the card name
    """

    def __init__(self, agent, logger):
        self.phase = PhaseType.CLEANUP
        self.agent = agent
        self.deck = []
        self.playarea = []
        self.discard_pile = []
        self.hand = []
        self.tavern_mat = []
        self.action_pool = {}
        self.remain_action = 1
        self.coin = 0
        self.logger = logger

        """ Information related to a card """
        self.num_copper_on_tavern_mat = 0  # Miser

    def init_deck(self):
        for _ in range(7):
            self.discard_pile.append(CopperCard())
        for _ in range(3):
            self.discard_pile.append(EstateCard())
        self.cleanup()

    def action(self, state, card):
        """
        Parameters
        ----------
        state: GameState
            Current game state
        card: Card
            A card to play
        """
        if self.remain_action < 1:
            print("No action remains")
            return

        """ Move the card from hand to playarea """
        """ NOTE: when this function is called, the card is removed from action_pool """
        self.hand.remove(card)  # TODO: implement efficiently
        self.playarea.append(card)
        card.action(state)
        self.remain_action -= 1
        assert(self.remain_action >= 0)

    def draw(self):
        if len(self.deck) == 0:
            self.deck = self.discard_pile
            random.shuffle(self.deck)
            self.discard_pile = []
        top = self.deck.pop()
        if CardType.ACTION in top.card_types:
            self.action_pool.setdefault(top.name, [])
            self.action_pool[top.name].append(top)
        self.hand.append(top)

    def buy(self, state):
        """
        Parameters
        ----------
        state: GameState
            Current game state
        """
        for card in self.hand:
            if CardType.TREASURE in card.card_types:
                """ TODO:
                    enable to choose NOT play a treasure card
                    this is critical to buy some cards like Grand Market or Mint
                """
                self.coin += card.get_coins(state)
        option = self.agent.select(state, "Buy", list(state.supply.cards.keys()))
        if option != ".":
            card = state.supply.get(option)
            self.discard_pile.append(card)

    def cleanup(self):
        self.coin = 0
        self.remain_action = 1
        self.discard_pile += self.hand
        self.discard_pile += self.playarea
        self.hand = []
        self.action_pool = {}
        self.playarea = []
        for i in range(5):
            self.draw()

    def update_phase(self, phase):
        """
        Parameters
        ----------
        phase: PhaseType
            Target phase
        """
        self.phase = phase
        log(self.logger, "info", "Now {} phase.".format(phase.name))

    def __str__(self):
        out = ""
        out += " [basic   ]\tcoin({}) action({})\n".format(self.coin,
                                                           self.remain_action)
        out += " [deck    ]\t" + " ".join(str(c) for c in self.deck) + "\n"
        out += " [discard ]\t" + " ".join(str(c)
                                          for c in self.discard_pile) + "\n"
        out += " [hand    ]\t" + " ".join(str(c) for c in self.hand) + "\n"
        out += " [playarea]\t" + " ".join(str(c) for c in self.playarea) + "\n"
        if len(self.tavern_mat) > 0:
            out += " [tavern  ]\t" + " ".join(str(c)
                                              for c in self.tavern_mat) + "\n"
        return out

    def hand_str(self):
        return "".join(sorted(str(c) for c in self.hand))


class Simulator:
    def __init__(self):
        self.result = Counter()

    def simulate(self, n):
        for _ in range(n):
            player = Player()
            player.init_deck()
            self.result[player.hand_str()] += 1
        for elem in self.result.most_common():
            hand = elem[0]
            count = elem[1]
            print(1.0 * count / n, hand)


class GameState(object):
    """ Stores information which is used when an agent needs to make a decision
    Attributes
    ----------
    players: list of Player
        the players who play this game
    turn_player: Player
        the player who takes the turn
    logger: file_like
        logger must have a `write` method such as sys.stdout or file
    """

    def __init__(self, logger):
        self.supply = Supply()
        self.logger = logger
        self.players = [Player(CLIAgent(), logger)]
        for player in self.players:
            player.init_deck()
        self.turn = 0
        assert(len(self.players) > 0)
        self.turn_player = self.players[0]

    def update_turn(self):
        self.turn += 1
        log(self.logger, "info", "Turn {}".format(self.turn))

    def play(self):
        """ command line user interface """
        while not self.finish():
            self.update_turn()
            for player_id, player in enumerate(self.players):
                self.turn_player = player
                log(self.logger, "info", "Player {}".format(player_id))
                self.turn_player.update_phase(PhaseType.ACTION)
                if len(self.turn_player.action_pool) > 0:
                    # TODO: support multiple actions in a turn
                    action = self.turn_player.agent.select(
                        self, "Action", list(self.turn_player.action_pool.keys()))

                    if action != '.':
                        assert(action in self.turn_player.action_pool)
                        assert(len(self.turn_player.action_pool[action]) > 0)
                        self.turn_player.action(
                            self, self.turn_player.action_pool[action].pop())
                self.turn_player.update_phase(PhaseType.BUY)
                self.turn_player.buy(self)
                self.turn_player.update_phase(PhaseType.CLEANUP)
                self.turn_player.cleanup()

    def finish(self):
        """ Returns True if the game satisfies one of end conditions
        """
        # WIP
        return False


def main():
    # simulator = Simulator()
    # simulator.simulate(10000)
    game = GameState(sys.stderr)
    game.play()


if __name__ == '__main__':
    main()
