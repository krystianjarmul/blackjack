import enum
import random
from dataclasses import dataclass
from typing import Set, List, Optional

from src.config import logger


class Mode(enum.Enum):
    AUTO = 0
    MANUAL = 1


@dataclass(frozen=True)
class Card:
    suit: str
    rank: str


class Player:

    def __init__(self, name: str):
        self.name = name
        self.score: int = 0
        self.cards: List[Card] = []
        self.plays = True

    def hit(self, card: Card):
        logger.info('HIT! "%s %s".', card.rank, card.suit)
        self.cards.append(card)
        self._update_scores()

    def _update_scores(self):
        self.score = sum([self._parse_card_rank(c.rank) for c in self.cards])

    def stand(self):
        self.plays = False

    @staticmethod
    def _parse_card_rank(rank: str):
        if rank in ['J', 'D', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)


class Game:

    def __init__(self):
        self._players_number: int = 0
        self._players: List[Player] = []
        self.deck: Optional[Deck] = None
        self.mode: Mode = Mode.AUTO

    def set_players_number(self, players_number: int):
        self._players_number = players_number

    def set_player(self, player: Player):
        self._players.append(player)

    @property
    def players_number(self):
        return self._players_number

    @property
    def players(self):
        return self._players

    def set_mode(self, mode: Mode):
        logger.info('Game mode has been changed to %s.', mode.name)
        self.mode = mode

    def start(self):
        logger.info('The blackjack game has been started.')
        self.deck = Deck()
        self.deck.shuffle()

    def is_over(self) -> bool:
        too_big_score = any([True for plr in self._players if plr.score > 21])
        all_players_folded = not any(plr.plays for plr in self._players)
        return too_big_score or all_players_folded

    def _all_players_folded(self) -> bool:
        return not all([plr.plays for plr in self._players])

    @staticmethod
    def get_win_score(scores: List[int]) -> int:
        scores = scores.copy()
        while True:
            score = max(scores)
            if score > 21:
                scores.remove(score)
            else:
                break
        return score

    def is_last_round(self):
        all_players_folded = not any(plr.plays for plr in self._players)
        one_player_left = [plr.plays for plr in self._players].count(True) == 1
        return one_player_left or all_players_folded


class Deck:

    def __init__(self):
        self._suits: Set[str] = {'Clubs', 'Diamonds', 'Hearts', 'Spades'}
        self._ranks: Set[str] = {
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'D', 'K', 'A'
        }
        self.cards = self._get_cards()

    def _get_cards(self) -> List[Card]:
        return [Card(s, r) for s in self._suits for r in self._ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        return self.cards.pop(0)
