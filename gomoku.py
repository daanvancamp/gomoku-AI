import time
import pygame

# Initialize Pygame
pygame.init()


class GomokuGame:
    def __init__(self, values):
        self.WIDTH = values[0]
        self.HEIGHT = values[1]
        self.GRID_SIZE = values[2]
        self.CELL_SIZE = self.WIDTH // self.GRID_SIZE
        self.P1COL = values[3]
        self.P2COL = values[4]
        self.BOARD_COL = values[5]
        self.LINE_COL = values[6]
        self.SLEEP_BEFORE_END = values[7]
        self.board = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))


window_name = "Gomoku"
victory_text = ""
pygame.display.set_caption(window_name)

current_player = 1


# Function to draw the game board
def draw_board(instance):
    instance.screen.fill(instance.BOARD_COL)
    for row in range(instance.GRID_SIZE):
        for col in range(instance.GRID_SIZE):
            pygame.draw.rect(instance.screen, instance.LINE_COL, (col * instance.CELL_SIZE, row * instance.CELL_SIZE, instance.CELL_SIZE, instance.CELL_SIZE), 1)
            if instance.board[row][col] == 1:
                pygame.draw.circle(instance.screen, instance.P1COL, (col * instance.CELL_SIZE + instance.CELL_SIZE // 2, row * instance.CELL_SIZE + instance.CELL_SIZE // 2), instance.CELL_SIZE // 2 - 5)
            elif instance.board[row][col] == 2:
                pygame.draw.circle(instance.screen, instance.P2COL, (col * instance.CELL_SIZE + instance.CELL_SIZE // 2, row * instance.CELL_SIZE + instance.CELL_SIZE // 2), instance.CELL_SIZE // 2 - 5)


def reset_game(instance):
    global current_player
    instance.board = [[0] * instance.GRID_SIZE for _ in range(instance.GRID_SIZE)]
    current_player = 1
    print("reset game")


def check_win(row, col, player, instance):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 5):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < instance.GRID_SIZE and 0 <= c < instance.GRID_SIZE and instance.board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - i * dr, col - i * dc
            if 0 <= r < instance.GRID_SIZE and 0 <= c < instance.GRID_SIZE and instance.board[r][c] == player:
                count += 1
            else:
                break
        if count >= 5:  # Victory condition
            return True
    return False


def run(instance):
    # Main game loop
    global window_name, victory_text, current_player
    running = True
    while running:
        window_name = "Gomoku -- Player " + str(current_player)
        pygame.display.set_caption(window_name)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = x // instance.CELL_SIZE
                row = y // instance.CELL_SIZE
                if instance.GRID_SIZE > row >= 0 == instance.board[row][col] and 0 <= col < instance.GRID_SIZE:
                    instance.board[row][col] = current_player
                    if check_win(row, col, current_player, instance):
                        victory_text = f"Player {current_player} wins!"
                        print(victory_text)
                        running = False
                    else:
                        # Switch player if neither player have won
                        current_player = 3 - current_player
        draw_board(instance)
        pygame.display.flip()

    # End game
    pygame.display.set_caption("Gomoku -- " + victory_text)
    time.sleep(instance.SLEEP_BEFORE_END)
    reset_game(instance)
    running = True
