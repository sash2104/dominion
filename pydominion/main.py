#!/usr/bin/env python
# coding: utf-8

""" """

import argparse
import random
import sys
from collections import Counter

from agent import CLIAgent
from defines import *


def parse_arguments():
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-i', '--input_file', required=True)
    parser.add_argument('-o', '--output_file', required=True)
    args = parser.parse_args()
    return args


class Card:
    def __init__(self):
        self.name = "."
        self.coin = 0
        self.card_types = set([CardType.NULL])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def action(self, game):
        """
        Parameters
        ----------
        game: Game
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

    def action(self, game):
        common_basic_action(self, game.player)


def common_basic_action(card, player):
    for _ in range(card.plus_draw):
        player.draw()


actions = {"1": CopperCard(), "2": SilverCard(), "3": GoldCard(), "S": SmithyCard(
), "E": EstateCard(), "D": DuchyCard(), "P": ProvinceCard(), ".": Card()}


class Player:
    def __init__(self, agent):
        self.phase = PhaseType.CLEANUP
        self.agent = agent
        self.deck = []
        self.playarea = []
        self.trash = []
        self.hand = []
        self.action_pool = []
        self.remain_action = 1

    def init_deck(self):
        for _ in range(7):
            self.deck.append(CopperCard())
        for _ in range(3):
            self.deck.append(EstateCard())
        random.shuffle(self.deck)
        self.cleanup()

    def action(self, card):
        if self.remain_action < 1:
            print("No action remains")
            return
        # TODO handからplayareaに移す処理
        card.action()
        self.remain_action -= 1
        assert(self.remain_action >= 0)

    def draw(self):
        if len(self.deck) == 0:
            self.deck = self.trash
            random.shuffle(self.deck)
            self.trash = []
        top = self.deck.pop()
        if CardType.ACTION in top.card_types:
            self.action_pool.append(top)
        self.hand.append(top)

    def buy(self, card):
        self.trash.append(card)

    def cleanup(self):
        self.remain_action = 1
        self.trash += self.hand
        self.hand = []
        self.action_pool = []
        self.playarea = []
        for i in range(5):
            self.draw()

    def __str__(self):
        out = ""
        out += "[D]" + "".join(str(c) for c in self.deck) + "\n"
        out += "[T]" + "".join(str(c) for c in self.trash) + "\n"
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


class State(object):
    """ Stores information which is used when an agent needs to make a decision
    """

    def __init__(self, player):
        self.player = player


class Game:
    def __init__(self):
        self.player = Player(CLIAgent())
        self.player.init_deck()

    def play(self):
        """ command line user interface """
        while not self.finish():
            self.player.phase = PhaseType.ACTION
            state = State(self.player)
            action = self.player.agent.select(state, self.player.action_pool)
            if action not in actions:
                # TODO: throw an exception
                print("Invalid action")
                return
            if action != ".":
                actions[action].action(self)
            print(self.player)
            self.player.phase = PhaseType.BUY
            state = State(self.player)
            action = self.player.agent.select(state, actions)
            if action not in actions:
                # TODO: throw an exception
                print("Invalid buy")
                return
            if action != ".":
                self.player.buy(actions[action])
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
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
