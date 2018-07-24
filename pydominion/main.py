#!/usr/bin/env python
# coding: utf-8

""" """

import argparse
import random
import sys
from collections import Counter

from agent import CLIAgent
from card import *
from defines import *


def parse_arguments():
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()
    return args


class Supply:
    def __init__(self):
        self.basic_cards = {"Copper": CopperCard(), "Silver": SilverCard(),
                            "Gold": GoldCard(), "Estate": EstateCard(),
                            "Duchy": DuchyCard(), "Province": ProvinceCard()}
        self.kingdom_cards = {"Smithy": SmithyCard()}
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

    def __init__(self, agent):
        self.phase = PhaseType.CLEANUP
        self.agent = agent
        self.deck = []
        self.playarea = []
        self.discard_pile = []
        self.hand = []
        self.action_pool = {}
        self.remain_action = 1

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
        self.hand.remove(card) # TODO: implement efficiently
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

    def buy(self, card):
        self.discard_pile.append(card)

    def cleanup(self):
        self.remain_action = 1
        self.discard_pile += self.hand
        self.discard_pile += self.playarea
        self.hand = []
        self.action_pool = {}
        self.playarea = []
        for i in range(5):
            self.draw()

    def __str__(self):
        out = ""
        out += "[D]" + "".join(str(c) for c in self.deck) + "\n"
        out += "[T]" + "".join(str(c) for c in self.discard_pile) + "\n"
        out += "[P]" + "".join(str(c) for c in self.playarea) + "\n"
        out += "[H]" + "".join(str(c) for c in self.hand) + "\n"
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
    """

    def __init__(self):
        self.player = Player(CLIAgent())
        self.player.init_deck()
        self.supply = Supply()

    def play(self):
        """ command line user interface """
        while not self.finish():
            self.player.phase = PhaseType.ACTION
            action = self.player.agent.select(self, self.player.action_pool)

            if action != '.':
                assert(action in self.player.action_pool)
                assert(len(self.player.action_pool[action]) > 0)
                self.player.action(self, self.player.action_pool[action].pop())
            print(self.player)
            self.player.phase = PhaseType.BUY
            card = self.player.agent.select(self, self.supply.cards)
            if card != ".":
                self.player.buy(self.supply.get(card))
            self.player.phase = PhaseType.CLEANUP
            self.player.cleanup()

    def finish(self):
        """ Returns True if the game satisfies one of end conditions
        """
        # WIP
        return False


def main():
    # simulator = Simulator()
    # simulator.simulate(10000)
    game = GameState()
    game.play()


if __name__ == '__main__':
    main()
