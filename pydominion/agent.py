import click
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
        print(state.player)
        click.echo(
            "Select {} options (q to quit, . for null):".format(option_name))
        for i, option in enumerate(options):
            click.echo("{}: {}".format(i, option))

        c = click.getchar()
        if c == 'q':
            click.echo("Goodbye.")
            sys.exit()
        if c.isdigit():
            option_id = int(c)
            assert(option_id < len(options),
                   "Index must be lower than the number of options")
            return options[option_id]
        return c
