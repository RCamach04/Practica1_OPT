from __future__ import annotations

import numpy as np

C: int = 0
D: int = 1


class Dilemma:

    def __init__(self, cc: float, cd: float, dc: float, dd: float) -> None:
        """
        Represents a 2x2 symmetric dilemma.

        Parameters:
            - cc (float): payoff for mutual cooperation
            - cd (float): payoff when one cooperates, but the opponent defects
            - dc (float): payoff when one defects, and the opponent cooperates
            - dd (float): payoff for mutual defection
        """
        self.cc: float = float(cc)
        self.cd: float = float(cd)
        self.dc: float = float(dc)
        self.dd: float = float(dd)

        self.matrix: np.ndarray = np.array(
            [
                [self.cc, self.cd],
                [self.dc, self.dd],
            ],
            dtype=float,
        )


    @property
    def payoff_matrix(self) -> np.ndarray:
        """
        Symmetric pay-off matrix of the dilemma.

        Returns:
            - 2x2 np array of the matrix
        """
        return self.matrix

    def evaluate_result(self, a_1: int, a_2: int) -> tuple[float, float]:
        """
        Given two actions, returns the payoffs of the two players.

        Parameters:
            - a_1 (int): action of player 1 (C=0 or D=1)
            - a_2 (int): action of player 2 (C=0 or D=1)

        Returns:
            - tuple of two floats, being the first and second values the payoff
              for the first and second player, respectively.
        """
        return float(self.matrix[a_1, a_2]), float(self.matrix[a_2, a_1])

  