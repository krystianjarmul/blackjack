import enum
import logging
import random
from dataclasses import dataclass
from typing import Set, List, Optional

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s')
logger.setLevel(logging.INFO)


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

    def take_card(self, card: Card):
        self.cards.append(card)
        self._update_scores()

    def _update_scores(self):
        self.score = sum([self._parse_card_rank(c.rank) for c in self.cards])

    def fold(self):
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

    def enter_players_name(self):
        for pn in range(self._players_number):
            player_name = input("Enter player's name: ")
            self.set_player(Player(player_name))
            logging.info('Player %s was added.', player_name)

    @property
    def players_number(self):
        return self._players_number

    @property
    def players(self):
        return self._players

    def set_mode(self, mode: Mode):
        logging.info('Game mode has been changed to %s.', mode.name)
        self.mode = mode

    def start_game(self):
        logging.info('The blackjack game has been started.')
        self.deck = Deck()
        self.deck.shuffle()
        self.set_players_number(2)
        self.enter_players_name()

    def run(self):
        self.start_game()
        self.choose_mode()

        if self.mode.name == 'AUTO':
            self._auto_mode()
        else:
            self._manual_mode()

    def _auto_mode(self):
        while True:
            for player in self._players:
                logging.info('Currently playing: %s.', player.name)
                card = self.deck.draw_card()
                player.take_card(card)
                logging.info('"%s %s" has been drawn.', card.rank, card.suit)
                logging.info("%s's scores: %s.", player.name, player.score)

                if player.score > 21:
                    logging.info('%s[%s] lost.', player.name, player.score)
                    break

            if self.is_game_over():
                logging.info('The game is over.')
                break

    def _manual_mode(self):
        while True:
            for player in self._players:
                if not player.plays:
                    continue
                logging.info('Currently playing: %s.', player.name)

                if player.score:
                    opt = self.input('Do you fold? 0 [no] | 1 [yes] ')
                    if opt:
                        logging.info('%s folded. The last draw.', player.name)
                        player.fold()
                        continue

                card = self.deck.draw_card()
                player.take_card(card)
                logging.info('"%s %s" has been drawn.', card.rank, card.suit)
                logging.info("%s's scores: %s.", player.name, player.score)

                if player.score > 21 or self._is_last_round():
                    break

            if self.is_game_over():
                players = [plr.name for plr in self._players]
                scores = [plr.score for plr in self._players]

                win_score = self._get_win_score(scores)
                winner = players[scores.index(win_score)]

                logging.info('The winner is %s[%s].', winner, win_score)
                logging.info('The game is over.')
                break

    def _one_player_left(self):
        return not any(plr.plays for plr in self._players)

    def choose_mode(self):
        mode = self.input('Choose game mode: 0 [auto] | 1 [manual] ')
        if mode:
            self.set_mode(Mode.MANUAL)
        else:
            self.set_mode(Mode.AUTO)

    def is_game_over(self) -> bool:
        #  TODO Refactor this method
        return bool(list(filter(lambda x: x.score > 21, self._players))) or \
               bool(list(filter(lambda x: not x.plays, self._players)))

    def _all_players_folded(self) -> bool:
        return not all([plr.plays for plr in self._players])

    @staticmethod
    def input(q: str) -> int:
        while True:
            try:
                ans = int(input(q))
                break
            except ValueError:
                logging.error('Invalid answer. Choose between 0 and 1.')

        return ans

    @staticmethod
    def _get_win_score(scores: List[int]) -> int:
        scores = scores.copy()
        while True:
            score = max(scores)
            if score > 21:
                scores.remove(score)
            else:
                break
        return score

    def _is_last_round(self):
        all_players_folded = not any(plr.plays for plr in self._players)
        one_player_left = not all([plr.plays for plr in self._players])
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


if __name__ == '__main__':
    Game().run()
