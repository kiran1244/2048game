# build 2048 in python using pygame!!
import pygame
import random
import copy

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
board_values = [[0 for _ in range(3)] for _ in range(3)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(3)] for _ in range(3)]
    if direc == 'UP':
        for i in range(3):
            for j in range(3):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
                    Q=2    

    elif direc == 'DOWN':
        for i in range(2, -1, -1):  # Iterate in reverse order
            for j in range(3):
                if board[i][j] != 0:
                    row = i
                    while row < 2 and board[row + 1][j] == 0:
                        row += 1
                    if row != i:
                        board[row][j] = board[i][j]
                        board[i][j] = 0
                    if row < 2 and board[row][j] == board[row + 1][j]:
                        board[row + 1][j] *= 2
                        score += board[row + 1][j]
                        board[row][j] = 0
        
    elif direc == 'LEFT':
        for i in range(3):
            for j in range(3):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(3):
            for j in range(2, -1, -1):  # Iterate in reverse order
                if board[i][j] != 0:
                    col = j
                    while col < 2 and board[i][col + 1] == 0:
                        col += 1
                    if col != j:
                        board[i][col] = board[i][j]
                        board[i][j] = 0
                    if col < 2 and board[i][col] == board[i][col + 1]:
                        board[i][col + 1] *= 2
                        score += board[i][col + 1]
                        board[i][col] = 0
      
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass
    
def save_board(board, filename):
    with open(filename, 'w') as file:
        for row in board:
            line = ' '.join(map(str, row))
            file.write(line + '\n')

def load_board(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        board = [list(map(int, line.strip().split())) for line in lines]
    return board
            


# draw tiles for game
def draw_pieces(board):
    for i in range(3):
        for j in range(3):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# Main game loop
run = True
move_made = False
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)

    if init_count < 2:
        original_board = [row[:] for row in board_values]
        board_values, game_over = new_pieces(board_values)
        init_count += 1

    if direction != '':
        original_board = copy.deepcopy(board_values)
        print("orignal_board")
        print(original_board)
        print("boardvalues")
        board_values = take_turn(direction, board_values)
        print(board_values)
        if board_values != original_board:
            print("came here;;;;;;;;;;")
            board_values, game_over = new_pieces(board_values)
            move_made = True
            
        direction = ''

    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            elif event.key == pygame.K_s:
                save_board(board_values, 'saved_board.txt')
            elif event.key == pygame.K_l:
                board_values = load_board('saved_board.txt')

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(3)] for _ in range(3)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()
