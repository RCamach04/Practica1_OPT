from __future__ import annotations

import copy
import itertools
import matplotlib.pyplot as plt

from .player import Player
from .dilemma import Dilemma
from .game import Game


class Tournament:

    # Este método ya está implementado
    def __init__(self, players: tuple[Player, ...],
                       n_rounds: int = 100,
                       error: float = 0.0,
                       repetitions: int = 2):
        """
        All-against-all tournament

        Parameters:
            - players (tuple[Player, ...]): tuple of players that will play the
         tournament
            - n_rounds (int = 100): number of rounds in the game
            - error (float = 0.0): error probability (in base 1)
            - repetitions (int = 2): number of games each player plays against
         the rest
        """

        self.players = players
        self.n_rounds = n_rounds
        self.error = error
        self.repetitions = repetitions

        # This is a key variable of the class. It is intended to store the
        # ongoing ranking of the tournament. It is a dictionary whose keys are
        # the players in the tournament, and its corresponding values are the
        # points obtained in their interactions with each other. In the end, to
        # see the winner, it will be enough to sort this dictionary by the
        # values.
        self.ranking = {player: 0.0 for player in self.players}  # initial vals


    def sort_ranking(self) -> None:
        """Sort the ranking by the value (score)"""
        sorted_items = sorted(
            self.ranking.items(),
            key=lambda item: item[1],
            reverse=True,
        )
        self.ranking.clear()
        self.ranking.update(sorted_items)


    #pista: utiliza 'itertools.combinations' para hacer los cruces
    def play(self) -> None:
        """
        Main call of the class. It must simulate the championship and update
        the variable 'self.ranking' with the accumulated points obtained by
        each player in their interactions.
        """
        self.ranking = {player: 0.0 for player in self.players}

        dilemma = self.players[0].dilemma if self.players else Dilemma(2, -1, 3, 0)

        for p1, p2 in itertools.combinations(self.players, 2):
            for _ in range(self.repetitions):
                inst1 = p1(dilemma) if isinstance(p1, type) else p1
                inst2 = p2(dilemma) if isinstance(p2, type) else p2

                if inst1 is inst2:
                    inst2 = copy.deepcopy(inst1)

                game = Game(inst1, inst2, n_rounds=self.n_rounds, error=self.error)
                game.play()
                s1, s2 = game.score

                self.ranking[p1] += s1
                self.ranking[p2] += s2

        self.sort_ranking()


    def plot_results(self):
        """
        Plots a bar chart of the final ranking. On the x-axis should appear
        the names of the sorted ranking of players participating in the
        tournament. On the y-axis the points obtained.
        """
        self.sort_ranking()

        names = [
            getattr(player, "name", None) or getattr(player, "__name__", str(player))
            for player in self.ranking.keys()
        ]
        scores = list(self.ranking.values())
        positions = list(range(len(names)))

        colors = plt.cm.viridis([i / max(len(names) - 1, 1) for i in range(len(names))])

        plt.figure(figsize=(10, 6))

        bars = plt.bar(positions, scores, color=colors, edgecolor='black')

        plt.xticks(positions, names, rotation=45, ha="right")

        plt.xlabel("Player")
        plt.ylabel("Score")
        plt.title("Tournament Ranking")

        plt.bar_label(bars, fmt='%g', padding=3)

        plt.tight_layout()
        plt.show()
