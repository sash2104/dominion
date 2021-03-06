from pydominion.agent import *
from pydominion.defines import *
from pydominion.supply import Supply
from pydominion.utils import log


class ActionOption(Option):
    def init(self):
        self.type = OptionType.ACTION
        # Information of a card to play must be in self.info
        assert("card" in self.info)
        self.description = self.info["card"].name

    def apply(self, state):
        self._choose_an_action(state)

    def _choose_an_action(self, state):
        card = self.info["card"]
        state.turn_player.action(state, card)


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

    def __init__(self, players, logger):
        """
        Attributes
        ----------
        players: list of Player
            the players who play this game
        logger: file_like
            logger must have a `write` method such as sys.stdout or file
        """
        self.supply = Supply()
        self.logger = logger
        self.players = players
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
                while self.turn_player.remain_action > 0:
                    if len(self.turn_player.action_pool) == 0:
                        break
                    # TODO: support multiple actions in a turn
                    options = [ActionOption(card=cards[0])
                               for cards in self.turn_player.action_pool.values()]
                    options.append(Option())
                    option = self.turn_player.agent.select(
                        self, "Action", options)
                    if option.type == OptionType.NULL:
                        """ if turn player chooses nothing to do, finish action phase """
                        break
                    option.apply(self)
                self.turn_player.update_phase(PhaseType.BUY)
                self.turn_player.buy(self)
                self.turn_player.update_phase(PhaseType.CLEANUP)
                self.turn_player.cleanup()

    def finish(self):
        """ Returns True if the game satisfies one of end conditions
        """
        # WIP
        return False
