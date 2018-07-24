from enum import Enum


class CardType(Enum):
    ACTION, TREASURE, VICTORY, CURSE, REACTION, ATTACK, NULL = range(7)


class PhaseType(Enum):
    ACTION, BUY, CLEANUP, NIGHT, NULL = range(5)


class OptionType(Enum):
    NULL, ACTION, BUY, DRAW = range(4)
