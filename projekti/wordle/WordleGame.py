import pygame
import random
import words
import common

pygame.init()

WIDTH = 500
HEIGHT = 900

black = (0, 0, 0)
gray = (200, 200, 200)
blue = (0, 0, 255)
green = (130, 255, 130)
yellow = (255, 255, 130)
dark_gray = (100, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle!!!")

board = [[" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]

keyboard = [["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P"],
               ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
                    ["Y", "X", "C", "V", "B", "N", "M"]]

stay_green = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                 ["0", "0", "0", "0", "0", "0", "0", "0", "0"],
                      ["0", "0", "0", "0", "0", "0", "0"]]

fps = 60
timer = pygame.time.Clock()

huge_font = pygame.font.Font("freesansbold.ttf", 56)
small_font = pygame.font.Font("freesansbold.ttf", 30)
secret_word = common.WORDS[random.randint(0, len(common.WORDS) - 1)]
game_over = False
win = False
turn = 0
letters = 0
turn_active = True
n = len(words.WORDS)

def draw_board():
    global turn 
    global board
    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(screen, black, [col * 100 + 12, row * 100 + 12, 75, 75], 3, 10)
            piece_text = huge_font.render(board[row][col], True, black)
            screen.blit(piece_text, (col * 100 + 30, row * 100 + 25))
    pygame.draw.rect(screen, blue, [5, 5 + turn * 100, WIDTH - 10, 90], 3, 10)

def draw_keyboard():
    for i in range(0, 10):
        pygame.draw.rect(screen, black, [i * 48 + 10, 700, 45, 45], 3, 5)
        slovo = small_font.render(keyboard[0][i], True, black)
        screen.blit(slovo, (i * 48 + 20, 709))
    for i in range(0, 9):
        pygame.draw.rect(screen, black, [i * 48 + 34, 754, 45, 45], 3, 5)
        slovo = small_font.render(keyboard[1][i], True, black)
        screen.blit(slovo, (i * 48 + 44, 763))
    for i in range(0, 7):
        pygame.draw.rect(screen, black, [i * 48 + 82, 808, 45, 45], 3, 5)
        slovo = small_font.render(keyboard[2][i], True, black)
        screen.blit(slovo, (i * 48 + 92, 817))

def check_words():
    global turn
    global letters
    global secret_word
    keyrow = 0
    keycol = 0
    for col in range(0, 5):
        for row in range(0, 6):
            if secret_word[col] == board[row][col] and turn > row:
                pygame.draw.rect(screen, green, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 10)

                for keyrow in range(0, 3):
                    for keycol in range(0, 10):
                        if keyrow == 1 and keycol > 8:
                            continue
                        if keyrow == 2 and keycol > 6:
                            continue
                        if board[row][col] == keyboard[keyrow][keycol].lower():
                            if keyrow == 0:
                                pygame.draw.rect(screen, green, [keycol * 48 + 10, 700, 45, 45], 0, 5)
                            elif keyrow == 1:
                                pygame.draw.rect(screen, green, [keycol * 48 + 34, 754, 45, 45], 0, 5)
                            elif keyrow == 2:
                                pygame.draw.rect(screen, green, [keycol * 48 + 82, 808, 45, 45], 0, 5)

                            stay_green[keyrow][keycol] = "1"
                            break

            elif board[row][col] in secret_word and turn > row:
                pygame.draw.rect(screen, yellow, [col * 100 + 12, row * 100 + 12, 75, 75], 0, 10)

                for keyrow in range(0, 3):
                    for keycol in range(0, 10):
                        if keyrow == 1 and keycol > 8:
                            continue
                        if keyrow == 2 and keycol > 6:
                            continue
                        if board[row][col] == keyboard[keyrow][keycol].lower() and stay_green[keyrow][keycol] == "0":
                            if keyrow == 0:
                                pygame.draw.rect(screen, yellow, [keycol * 48 + 10, 700, 45, 45], 0, 5)
                            elif keyrow == 1:
                                pygame.draw.rect(screen, yellow, [keycol * 48 + 34, 754, 45, 45], 0, 5)
                            elif keyrow == 2:
                                pygame.draw.rect(screen, yellow, [keycol * 48 + 82, 808, 45, 45], 0, 5)
                            break

            elif turn > row:

                for keyrow in range(0, 3):
                    for keycol in range(0, 10):
                        if keyrow == 1 and keycol > 8:
                            continue
                        if keyrow == 2 and keycol > 6:
                            continue
                        if board[row][col] == keyboard[keyrow][keycol].lower():
                            if keyrow == 0:
                                pygame.draw.rect(screen, dark_gray, [keycol * 48 + 10, 700, 45, 45], 0, 5)
                            elif keyrow == 1:
                                pygame.draw.rect(screen, dark_gray, [keycol * 48 + 34, 754, 45, 45], 0, 5)
                            elif keyrow == 2:
                                pygame.draw.rect(screen, dark_gray, [keycol * 48 + 82, 808, 45, 45], 0, 5)
                            break

def binary_search(l, r, word, array):
    if l <= r:
        mid = l + (r - l) // 2
        if word < array[mid]:
            return binary_search(l, mid - 1, word, array)
        if word > array[mid]:
            return binary_search(mid + 1, r, word, array)
        if word == array[mid]:
            return True
    else:
        return False


running = True

while running:

    timer.tick(fps)
    screen.fill(gray)
    check_words()
    draw_board()
    draw_keyboard()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT and turn_active and not game_over:
            entry = event.__getattribute__("text")
            if entry != " ":
                entry = entry.lower()
                board[turn][letters] = entry
                letters += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and letters > 0:
                board[turn][letters - 1] = " "
                letters -= 1
            if event.key == pygame.K_SPACE and not game_over and letters == 5:
                current_word = board[turn][0] + board[turn][1] + board[turn][2] + board[turn][3] + board[turn][4]
                if binary_search(0, n - 1, current_word, words.WORDS):
                    turn += 1
                    letters = 0
            if event.key == pygame.K_SPACE and game_over:
                turn = 0
                letters = 0
                game_over = False
                win = False
                secret_word = common.WORDS[random.randint(0, len(common.WORDS) - 1)]
                board = [[" ", " ", " ", " ", " "], 
                         [" ", " ", " ", " ", " "], 
                         [" ", " ", " ", " ", " "], 
                         [" ", " ", " ", " ", " "], 
                         [" ", " ", " ", " ", " "], 
                         [" ", " ", " ", " ", " "]]
                stay_green = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                ["0", "0", "0", "0", "0", "0", "0", "0", "0"],
                                    ["0", "0", "0", "0", "0", "0", "0"]]

        if letters == 5:
            turn_active = False
        if letters < 5:
            turn_active = True

        for row in range(0, 6):
            guess = board[row][0] + board[row][1] + board[row][2] + board[row][3] + board[row][4]
            if guess == secret_word and row < turn:
                game_over = True
                win = True

    if win:
        winner_text = huge_font.render("BRAVO!!!", True, black)
        screen.blit(winner_text, (120, 630))

    if turn == 6 and not win:
        game_over = True
        text = "NOOB!!! " + secret_word
        loser_text = huge_font.render(text, True, black)
        screen.blit(loser_text, (50, 630))
       

    pygame.display.flip()
pygame.quit()
