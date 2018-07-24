import sys

from defines import *


class Option(object):
    """ Base Option Class
    """

    def __init__(self, **kwargs):
        self.info = kwargs
        self.type = OptionType.NULL
        self.init()

    def init(self):
        pass


class BuyOption(Option):
    def init(self):
        self.type = OptionType.BUY
        # Information of a card to buy must be in self.info
        assert("card" in self.info)


class Agent(object):
    """ Base Agent Class
    """

    def __init__(self):
        pass

    def select(self, state, options):
        """ Select an option from given options
        Parameters
        ----------
        state: GameState
            Current game state
        options: list of Option
            Valid options

        Returns
        -------
        option: Option
            The selected option
        """
        raise NotImplementedError


class CLIAgent(Agent):
    """ A Command Line Interface agent, which takes input from the command line.
    """

    def select(self, state, options):
        print(state.player)
        print("Now {phase} phase. Choose your {phase} {options}.).".format(
            phase=state.player.phase.name, options=options))
        option = sys.stdin.readline().rstrip()
        return option
