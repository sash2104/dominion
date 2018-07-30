import random

from pydominion.card import *
from pydominion.defines import *
from pydominion.agent import *
from pydominion.utils import log


class BuyOption(Option):
    def init(self):
        self.type = OptionType.BUY
        # Information of a card to buy must be in self.info
        assert("card" in self.info)
        self.description = self.info["card"].name

    def apply(self, state):
        self._buy_a_card(state)

    def _buy_a_card(self, state):
        state.turn_player.discard_pile.append(self.info["card"])


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
        options = [BuyOption(card=card)
                   for card in state.supply.cards.values()]
        options.append(Option())
        option = self.agent.select(state, "Buy", options)
        option.apply(state)

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
