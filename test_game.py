from unittest import mock

from game import Game, Deck, Player, Mode, Card


def test_game_setting_number_of_players():
    game = Game()

    game.set_players_number(2)

    assert game.players_number == 2


def test_game_setting_players():
    game = Game()
    player1 = Player('Player1')
    player2 = Player('Player2')

    game.set_player(player1)
    game.set_player(player2)

    assert game.players == [player1, player2]


def test_game_entering_players_name():
    with mock.patch('builtins.input', return_value='test') as input_mock:
        game = Game()
        game.set_players_number(2)

        game.enter_players_name()

        assert input_mock.call_count == 2


def test_shuffle_a_deck():
    deck = Deck()

    before_shuffle = deck.cards.copy()
    deck.shuffle()
    after_shuffle = deck.cards

    assert before_shuffle != after_shuffle


def test_deck_draw_a_card():
    deck = Deck()
    first_card = deck.cards[0]

    card = deck.draw_card()

    assert card == first_card


def test_player_takes_card():
    player = Player('player1')
    card = Card(suit='Spades', rank='10')

    player.take_card(card)

    assert player.cards == [card]
    assert player.score == int(card.rank)


def test_select_game_mode():
    game = Game()

    assert game.mode == Mode.AUTO
    game.set_mode(Mode.MANUAL)
    assert game.mode == Mode.MANUAL

