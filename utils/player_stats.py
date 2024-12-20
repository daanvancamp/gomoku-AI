from utils import stats
from configuration.config import config

def reset_player_stats(game):
	for i in range(len(game.players)):
		game.players[i].reset_score()

# Update win / loss stats of game.players: -1 = tie; 1 = player 1 won; 2 = player 2 won
def update_player_stats(game, winner:int):
	AI_players=[p for p in game.players if p.type=="AI"]
	if winner > -1: # run if game was not a tie
		print("win player", winner)
		winning_player = game.players[winner-1]
		opponent = game.players[2-winner] #=losing player

		if winning_player.type == "AI":
			winning_player.AI_model.log_win(opponent.type)

		if opponent.type == "AI":
			opponent.AI_model.log_loss(winning_player.type)

		for i in range(len(game.players)):
			if i == winner-1:
				game.players[i].wins += 1
				is_winner = True
			else:
				game.players[i].losses += 1
				is_winner = False
			game.players[i].calculate_score(int(config["GAME"]["board_size"]) ** 2, is_winner, game.current_game)
			if game.last_round:
				game.players[i].calculate_win_rate(game.current_game)
	else:
		for player in AI_players:
			player.AI_model.log_tie()

	for i in range(len(game.players)):
		game.players[i].calculate_score(0, False, game.current_game)
	stats.log_win(game.players)
	if game.last_round:
		stats.log_message(f"\nStatistics:\n{game.players[0].type} {game.players[0].id}:\nwins: {game.players[0].wins} - win rate: {game.players[0].win_rate} - average score: {game.players[0].avg_score} - weighed score: {sum(game.players[0].weighed_scores)/len(game.players[0].weighed_scores)} - average moves: {game.players[0].avg_moves}.\n"
						  f"{game.players[1].type} {game.players[1].id}:\nwins: {game.players[1].wins} - win rate: {game.players[1].win_rate} - average score: {game.players[1].avg_score} - weighed score: {sum(game.players[1].weighed_scores)/len(game.players[1].weighed_scores)} - average moves: {game.players[1].avg_moves}.")
