import sys

from pydominion.defines import *


class Option(object):
    """ Base Option Class
    """

    def __init__(self, description, **kwargs):
        self.description = description
        self.info = kwargs
        self.type = OptionType.NULL
        self.init()

    def init(self):
        pass

    def apply(self, state):
        """ apply the option to given state """
        pass


class Agent(object):
    """ Base Agent Class
    """

    def __init__(self):
        pass

    def select(self, state, option_name, options):
        """ Select an option from given options
        Parameters
        ----------
        state: GameState
            Current game state
        option_name: str
            An explanation for the options
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

    def select(self, state, option_name, options):
        # TODO: make options to list of Options, not list of str
        # TODO: make return variable to Option, not str
        print(state.turn_player)
        print("Select {} options (q to quit):".format(option_name))
        for i, option in enumerate(options):
            print("{}: {}".format(i, option.description))

        c = sys.stdin.readline().rstrip()
        if c == 'q':
            print("Goodbye.")
            sys.exit()
        if c.isdigit():
            option_id = int(c)
            assert option_id < len(
                options), "Index must be lower than the number of options"
            return options[option_id]
        return c
