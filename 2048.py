import pygame
import random

pygame.init()

# Initial setup
WIDTH = 400
HEIGHT = 500
icon = pygame.image.load('2048.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('2048')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
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

# Game variables initialization
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
high_score = 0

# Draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

# Take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    
    # (Same logic as before for moving the tiles)
    # ...

    return board

# Spawn new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# Draw board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))

def draw_pieces(board):
    for i in range(4):
        for j in range(4):
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

# Draw buttons for directions
def draw_buttons():
    button_size = 60
    pygame.draw.rect(screen, 'blue', [50, 420, button_size, button_size])  # Up
    pygame.draw.rect(screen, 'blue', [50, 490, button_size, button_size])  # Down
    pygame.draw.rect(screen, 'blue', [10, 455, button_size, button_size])  # Left
    pygame.draw.rect(screen, 'blue', [110, 455, button_size, button_size])  # Right
    
    up_text = font.render('↑', True, 'white')
    down_text = font.render('↓', True, 'white')
    left_text = font.render('←', True, 'white')
    right_text = font.render('→', True, 'white')
    
    screen.blit(up_text, (75, 430))
    screen.blit(down_text, (75, 500))
    screen.blit(left_text, (20, 460))
    screen.blit(right_text, (120, 460))

# Game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    draw_buttons()

    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True

    if game_over:
        draw_over()
        if score > high_score:
            high_score = score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Check if any button is clicked
            if 50 <= mouse_pos[0] <= 110 and 420 <= mouse_pos[1] <= 480:  # Up
                direction = 'UP'
            elif 50 <= mouse_pos[0] <= 110 and 490 <= mouse_pos[1] <= 550:  # Down
                direction = 'DOWN'
            elif 10 <= mouse_pos[0] <= 70 and 455 <= mouse_pos[1] <= 515:  # Left
                direction = 'LEFT'
            elif 110 <= mouse_pos[0] <= 170 and 455 <= mouse_pos[1] <= 515:  # Right
                direction = 'RIGHT'

            if game_over:
                if event.button == 1:  # Left mouse button
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()
