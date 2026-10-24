"""
Module that defines the base Player class and basic strategies for the IPD.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

try:
    from dilemma import C, D, Dilemma
except ImportError:
    from src.dilemma import C, D, Dilemma


class Player(ABC):
    """
    Abstract class that represents a generic player in the Prisoner's Dilemma.
    """

    @abstractmethod
    def __init__(self, dilemma: Dilemma, name: str = ""):
        """
        Abstract class that represents a generic player

        Parameters:
            - name (str): the name of the strategy
            - dilemma (Dilemma): the dilemma that this player will play
        """

        self.name = name
        self.dilemma = dilemma

        self.history  = []  # This is the main variable of this class. It is
                            # intended to store all the history of actions
                            # performed by this player.
                            # Example: [C, C, D, D, D] <- So far, the
                            # interaction lasts five rounds. In the first one,
                            # this player cooperated. In the second, he also
                            # cooperated. In the third, he defected. Etc.

    @abstractmethod
    def strategy(self, opponent: Player) -> int:
        """
        Main call of the class. Gives the action for the following round of the
        interaction, based on the history.

        Parameters:
            - opponent (Player): is another instance of Player.

        Returns:
            - An integer representing Cooperation (C=0) or Defection (D=1)
        """
        pass

    def compute_scores(self, opponent: Player) -> tuple[float, float]:
        """
        Compute the cumulative scores for a given opponent over the interaction history.

        Parameters:
            - opponent (Player): is another instance of Player.

        Returns:
            - A tuple of two floats, where the first value is the current
              player's payoff, and the second value is the opponent's payoff.
        """
        assert len(self.history) == len(opponent.history), (
            f"Histories have unequal lengths: {len(self.history)} vs {len(opponent.history)}"
        )

        score_self: float = 0.0
        score_opponent: float = 0.0

        for a_1, a_2 in zip(self.history, opponent.history):
            p1, p2 = self.dilemma.evaluate_result(a_1, a_2)
            score_self += p1
            score_opponent += p2

        return (score_self, score_opponent)

    # Este método ya está implementado
    def clean_history(self) -> None:
        """Resets the history of the current player"""
        self.history = []


# Basic strategies from Nicky Case's "The Evolution of Trust"


class Cooperator(Player):
    """Player that always cooperates."""

    def __init__(self, dilemma: Dilemma, name: str = "") -> None:
        """Cooperator"""
        super().__init__(dilemma, name or "cooperator")

    def strategy(self, opponent: Player) -> int:
        """Cooperates always"""
        return C


class Defector(Player):
    """Player that always defects."""

    def __init__(self, dilemma: Dilemma, name: str = "") -> None:
        """Defector"""
        super().__init__(dilemma, name or "defector")

    def strategy(self, opponent: Player) -> int:
        """Defects always"""
        return D


class Tft(Player):
    """
    Tit-for-Tat player: cooperates on the first move, then copies the
    opponent's previous move.
    """

    def __init__(self, dilemma: Dilemma, name: str = "") -> None:
        """Tit-for-tat"""
        super().__init__(dilemma, name or "tft")

    def strategy(self, opponent: Player) -> int:
        """Cooperates first, then repeat last action of the opponent"""
        if not opponent.history:
            return C
        return opponent.history[-1]


class Grudger(Player):
    """
    Grudger (Friedman) player: cooperates until the opponent defects once,
    then defects forever.
    """

    def __init__(self, dilemma: Dilemma, name: str = "") -> None:
        """Grudger"""
        super().__init__(dilemma, name or "grudger")

    def strategy(self, opponent: Player) -> int:
        """
        Cooperates always, but if opponent ever defects, it will defect for the
        rest of the game
        """
        if D in opponent.history:
            return D
        return C


class Detective4MovsTft(Player):
    """
    Detective player: starts with [C, D, C, C]. If the opponent ever defected,
    plays TFT; otherwise, plays Defector.
    """

    INITIAL_MOVES: tuple[int, int, int, int] = (C, D, C, C)

    def __init__(self, dilemma: Dilemma, name: str = "") -> None:
        """Four movement - tit for tat detective"""
        super().__init__(dilemma, name or "detective")

    def strategy(self, opponent: Player) -> int:
        """
        Starts with a fixed sequence of actions: [C,D,C,C]. After that, if
        the opponent has ever defected, plays 'TFT'. If not, plays 'Defector'.
        """
        round_idx = len(self.history)
        if round_idx < 4:
            return self.INITIAL_MOVES[round_idx]
        if D in opponent.history:
            return opponent.history[-1]
        return D
