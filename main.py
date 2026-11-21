from src.dilemma import Dilemma
from src.player import Cooperator, Defector, Tft, Grudger, Detective4MovsTft, StatisticalPlayer
from src.tournament import Tournament

dilemma = Dilemma(2, -1, 3, 0)

cooperator_player = Cooperator(dilemma, "cooperator")
defector_player = Defector(dilemma, "defector")
tft_player = Tft(dilemma, "tft")
grudger_player = Grudger(dilemma, "grudger")
detective_player = Detective4MovsTft(dilemma, "detective")
statistical_player = StatisticalPlayer(dilemma, "statistical")

all_players = (cooperator_player, defector_player, tft_player, grudger_player,
               detective_player, statistical_player)

tournament = Tournament(all_players, n_rounds=100, error=0.3, repetitions=1)
tournament.play()
tournament.plot_results()
