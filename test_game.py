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


def test_is_last_round_if_one_player_left():
    game = Game()
    player1 = Player('player1')
    player2 = Player('player2')
    game.set_player(player1)
    game.set_player(player2)

    player1.fold()
    assert game._is_last_round()


def test_is_game_over_if_score_higher_than_21():
    game = Game()
    player1 = Player('player1')
    player2 = Player('player2')
    game.set_player(player1)
    game.set_player(player2)

    game.players[0].score = 22

    assert game.is_game_over()


def test_is_game_over_if_all_players_folded():
    game = Game()
    player1 = Player('player1')
    player2 = Player('player2')
    game.set_player(player1)
    game.set_player(player2)

    for plr in game.players:
        plr.fold()

    assert game.is_game_over()