#!/usr/bin/env python
# coding: utf-8

""" """

import sys

from pydominion.agent import CLIAgent
from pydominion.player import Player
from pydominion.state import GameState
from pydominion.supply import Supply


def main():
    logger = sys.stderr
    players = [Player(CLIAgent(), logger)]
    game = GameState(players, logger)
    game.play()


if __name__ == '__main__':
    main()
