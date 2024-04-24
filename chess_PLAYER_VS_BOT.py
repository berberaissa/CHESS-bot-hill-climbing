import chess
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants for the board
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

# Colors
WHITE = (255, 255, 255)
BLACK = (116, 90, 64)
HIGHLIGHT_SELECTED = (255, 50, 50)  # Color for selected square

# Chess board initialization
chess_board = chess.Board()

# Load and scale images
def load_images():
    pieces = ["P", "R", "N", "B", "Q", "K", "p", "r", "n", "b", "q", "k"]
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f"/home/e20230011829/Documents/chess/chess_pieces/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Draw the chess board
def draw_board(screen, selected_square):
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else pygame.Color('gray')
            if selected_square is not None and selected_square == chess.square(col, row):
                color = HIGHLIGHT_SELECTED
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces on the board
def draw_pieces(screen, board, images):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board.piece_at(chess.square(c, r))
            if piece:
                screen.blit(images[str(piece)], (c * SQUARE_SIZE, r * SQUARE_SIZE))

def random_move():
    move = random.choice(list(chess_board.legal_moves))
    chess_board.push(move)
    
def render_text(screen, message, pos, size=32, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=pos)
    screen.blit(text, text_rect)                
                
                

def display_game_result(screen, board):
    if board.is_checkmate():
        message = "Checkmate!"
    elif board.is_stalemate():
        message = "Stalemate!"
    elif board.is_insufficient_material():
        message = "Draw due to insufficient material!"
    elif board.is_seventyfive_moves():
        message = "Draw due to 75-move rule!"
    elif board.is_fivefold_repetition():
        message = "Draw due to fivefold repetition!"
    else:
        message = "Unknown game result!"

    # Display the message
    screen.fill((0, 0, 0))  # Optional: Fill the screen with black or another color before displaying the message
    render_text(screen, message, (WIDTH // 2, HEIGHT // 2), size=50, color=(255, 0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)  # Keep the message displayed for 5 seconds

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:  # If it's White's turn, black wins
            return float('-inf')
        else:           # If it's Black's turn, white wins
            return float('inf')
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    
    eval = 0
    eval += len(board.pieces(chess.PAWN, chess.WHITE)) * 1
    eval += len(board.pieces(chess.KNIGHT, chess.WHITE)) * 3
    eval += len(board.pieces(chess.BISHOP, chess.WHITE)) * 3
    eval += len(board.pieces(chess.ROOK, chess.WHITE)) * 5
    eval += len(board.pieces(chess.QUEEN, chess.WHITE)) * 9
    eval -= len(board.pieces(chess.PAWN, chess.BLACK)) * 1
    eval -= len(board.pieces(chess.KNIGHT, chess.BLACK)) * 3
    eval -= len(board.pieces(chess.BISHOP, chess.BLACK)) * 3
    eval -= len(board.pieces(chess.ROOK, chess.BLACK)) * 5
    eval -= len(board.pieces(chess.QUEEN, chess.BLACK)) * 9
    return eval


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def hill_climbing_move(board, depth=3):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in legal_moves:
        board.push(move)
        current_value = minimax(board, depth - 1, alpha, beta, False)
        board.pop()

        if current_value > best_value:
            best_value = current_value
            best_move = move

    return best_move

def main():
    clock = pygame.time.Clock()
    images = load_images()
    running = True
    selected_square = None
    player_turn = True  # True if human player's turn, False for bot

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if chess_board.is_game_over():
                # When the game ends, display the result
                display_game_result(screen, chess_board)
                pygame.time.wait(5000)  # Display for 5 seconds
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                square = chess.square(col, row)

                if selected_square is not None:
                    move = chess.Move(selected_square, square)
                    if move in chess_board.legal_moves:
                        chess_board.push(move)
                        selected_square = None
                        player_turn = False
                    else:
                        selected_square = square if chess_board.piece_at(square) else None
                else:
                    selected_square = square if chess_board.piece_at(square) else None

        if not player_turn:
            move = hill_climbing_move(chess_board)
            if move:
                chess_board.push(move)
            player_turn = True

        draw_board(screen, selected_square)
        draw_pieces(screen, chess_board, images)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
