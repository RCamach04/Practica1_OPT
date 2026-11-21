from __future__ import annotations

import random

from .dilemma import C, D
from .player import Player


class Game:

    # Este método ya está implementado
    def __init__(self, player_1: Player,
                       player_2: Player,
                       n_rounds: int = 100,
                       error: float = 0.0):
        """
        Game class to represent an iterative dilema

        Parameters:
            - player_1 (Player): first player of the game
            - player_2 (Player): second player of the game
            - n_rounds (int = 100): number of rounds in the game
            - error (float = 0.0): error probability (in base 1)
        """

        assert n_rounds > 0, "'n_rounds' should be greater than 0"

        self.player_1 = player_1
        self.player_2 = player_2
        self.n_rounds = n_rounds
        self.error = error

        self.score = (0.0, 0.0)  # this variable will store the final result of
                                 # the game, once the 'play()' function has
                                 # been called. The two values of the tuple
                                 # correspond to the points scored by the first
                                 # and second player, respectively.


    def play(self, do_print: bool = False) -> None:
        """
        Main call of the class. Play the game.
        Stores the final result in 'self.score'

        Parameters
            - do_print (bool = False): if True, should print the ongoing
            results at the end of each round (i.e. print round number, last
            actions of both players and ongoing score).
        """
        self.player_1.clean_history()
        self.player_2.clean_history()

        for r in range(self.n_rounds):
            a_1 = self.player_1.strategy(self.player_2)
            a_2 = self.player_2.strategy(self.player_1)

            if self.error > 0.0:
                if random.random() < self.error:
                    a_1 = D if a_1 == C else C
                if random.random() < self.error:
                    a_2 = D if a_2 == C else C

            self.player_1.history.append(a_1)
            self.player_2.history.append(a_2)

            if do_print:
                ongoing_score = self.player_1.compute_scores(self.player_2)
                p1_name = getattr(self.player_1, "name", "Player 1")
                p2_name = getattr(self.player_2, "name", "Player 2")
                print(
                    f"Round {r + 1}: {p1_name}={a_1}, {p2_name}={a_2} "
                    f"-> Score: {ongoing_score}"
                )

        self.score = self.player_1.compute_scores(self.player_2)
