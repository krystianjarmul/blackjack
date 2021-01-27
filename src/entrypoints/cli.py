from src.blackjack.game import Game, Mode, Player
from src.config import logger


class BlackJackCLI:
    def __init__(self):
        self.game = Game()

    def auto_mode(self):
        while True:
            for player in self.game.players:
                logger.info('Currently playing: %s.', player.name)
                card = self.game.deck.draw_card()
                player.take_card(card)
                logger.info('"%s %s" has been drawn.', card.rank, card.suit)
                logger.info("%s's scores: %s.", player.name, player.score)

                if player.score > 21:
                    logger.info('%s[%s] lost.', player.name, player.score)
                    break

            if self.game.is_over():
                logger.info('The game is over.')
                break

    def run(self):
        self.game.start()
        self.enter_players_number()
        self.enter_players_name()
        self.choose_mode()
        if self.game.mode.name == 'AUTO':
            self.auto_mode()
        else:
            self.manual_mode()

    def choose_mode(self):
        mode = self.input('Choose game mode: 0 [auto] | 1 [manual] ')
        if mode:
            self.game.set_mode(Mode.MANUAL)
        else:
            self.game.set_mode(Mode.AUTO)

    def manual_mode(self):
        while True:
            for player in self.game.players:
                if not player.plays:
                    continue
                logger.info(
                    'Currently playing: %s[%s].', player.name, player.score
                )

                if player.score:
                    opt = self.input('Do you fold? 0 [no] | 1 [yes] ')
                    if opt:
                        logger.info('%s folded. The last draw.', player.name)
                        player.fold()
                        continue

                card = self.game.deck.draw_card()
                player.take_card(card)
                logger.info('"%s %s" has been drawn.', card.rank, card.suit)
                logger.info("%s's scores: %s.", player.name, player.score)

                if player.score > 21 or self.game.is_last_round():
                    break

            if self.game.is_over():
                players = [plr.name for plr in self.game.players]
                scores = [plr.score for plr in self.game.players]

                win_score = self.game.get_win_score(scores)
                winner = players[scores.index(win_score)]

                logger.info('The winner is %s[%s].', winner, win_score)
                logger.info('The game is over.')
                break

    def enter_players_name(self):
        for pn in range(self.game.players_number):
            player_name = input("Enter player's name: ")
            self.game.set_player(Player(player_name))
            logger.info('Player %s was added.', player_name)

    def enter_players_number(self):
        players_number = self.input(
            "Enter number of players: ", 'Invalid answer. Provide an integer.'
        )
        self.game.set_players_number(players_number)

    @staticmethod
    def input(q: str, e: str = 'Invalid answer. Choose 0 or 1.') -> int:
        while True:
            try:
                ans = int(input(q))
                break
            except ValueError:
                logger.error(e)
        return ans


if __name__ == '__main__':
    BlackJackCLI().run()
