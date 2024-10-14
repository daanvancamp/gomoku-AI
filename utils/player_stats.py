from utils import stats
from configuration.config import config

def reset_player_stats(game):#todo integrate in the right place
    for i in range(len(game.players)):
        game.players[i].reset_score()

# Update win / loss stats of game.players: -1 = tie; 1 = player 1 won; 2 = player 2 won
def update_player_stats(game, winning_player):
    AI_players=[p for p in game.players if p.TYPE=="AI-Model"]
    if winning_player > -1: # run if game was not a tie
        if winning_player == 1:
            if game.player1.TYPE =="AI-Model":
                game.player1.AI_model.log_win()
            if game.player2.TYPE =="AI-Model":
                game.player2.AI_model.log_loss()
        elif winning_player == 2:
            if game.player1.TYPE =="AI-Model":
                game.player1.AI_model.log_loss()
            if game.player2.TYPE =="AI-Model":
                game.player2.AI_model.log_win()

        for i in range(len(game.players)):
            if i == winning_player-1:
                game.players[i].wins += 1
                is_winner = True
            else:
                game.players[i].losses += 1
                is_winner = False
            game.players[i].calculate_score(int(config["OTHER VARIABLES"]["BOARDSIZE"]) ** 2, is_winner, game.current_game)
            if game.last_round:
                game.players[i].calculate_win_rate(game.current_game)
    else:
        for player in AI_players:
            player.AI_model.log_tie()

    for i in range(len(game.players)):
        game.players[i].calculate_score(0, False, game.current_game)
    stats.log_win(game.players)
    if game.last_round:
        stats.log_message(f"\nStatistics:\n{game.players[0].TYPE} {game.players[0].id}:\nwins: {game.players[0].wins} - win rate: {game.players[0].win_rate} - average score: {game.players[0].avg_score} - weighed score: {sum(game.players[0].weighed_scores)/len(game.players[0].weighed_scores)} - average moves: {game.players[0].avg_moves}.\n"
                          f"{game.players[1].TYPE} {game.players[1].id}:\nwins: {game.players[1].wins} - win rate: {game.players[1].win_rate} - average score: {game.players[1].avg_score} - weighed score: {sum(game.players[1].weighed_scores)/len(game.players[1].weighed_scores)} - average moves: {game.players[1].avg_moves}.")
