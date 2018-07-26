from pydominion.card import *

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

    def get(self, card_name):
        """ WIP: count down a card
        Returns
        -------
        card: Card
            A card to be bought or gained
        """
        assert(card_name in self.cards)
        return self.cards[card_name]
