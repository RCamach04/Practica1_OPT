from dilemma import Dilemma
from player import Cooperator, Defector, Tft, Grudger, Detective4MovsTft
from tournament import Tournament

dilemma = Dilemma(2, -1, 3, 0)

cooperator_player = Cooperator(dilemma, "cooperator")
defector_player = Defector(dilemma, "defector")
tft_player = Tft(dilemma, "tft")
grudger_player = Grudger(dilemma, "grudger")
detective_player = Detective4MovsTft(dilemma, "detective")

all_players = (cooperator_player, defector_player, tft_player, grudger_player,
               detective_player)

tournament = Tournament(all_players, n_rounds=10, error=0.0, repetitions=1)
tournament.play()
tournament.plot_results()