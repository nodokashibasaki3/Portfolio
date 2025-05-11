import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
FPS = 10
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Tetromino shapes
TETROMINOS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
score = 0

def draw_board():
    screen.fill((30, 30, 30))
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    for y in range(ROWS):
        for x in range(COLS):
            if board[y][x]:
                pygame.draw.rect(screen, COLORS[board[y][x] - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (200, 200, 200), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

class Piece:
    def __init__(self):
        self.shape_idx = random.randint(0, len(TETROMINOS) - 1)
        self.shape = TETROMINOS[self.shape_idx]
        self.color = self.shape_idx + 1  # Match color index with shape index
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dx, dy):
        if not self.collision(dx, dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def rotate(self):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        original_x = self.x
        
        # Try to rotate, if it causes collision, try to adjust x position
        if not self.collision(0, 0, rotated_shape):
            self.shape = rotated_shape
            return True
        
        # Try to adjust position if rotation causes collision with the walls
        for offset in [1, -1, 2, -2]:
            if not self.collision(offset, 0, rotated_shape):
                self.x += offset
                self.shape = rotated_shape
                return True
        
        self.x = original_x
        return False

    def collision(self, dx, dy, shape=None):
        if shape is None:
            shape = self.shape
            
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                        return True
                    if new_y >= 0 and board[new_y][new_x]:
                        return True
        return False

    def place(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and 0 <= self.y + y < ROWS and 0 <= self.x + x < COLS:
                    board[self.y + y][self.x + x] = self.color

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[self.color - 1],
                                    ((self.x + x) * BLOCK_SIZE, (self.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, (200, 200, 200),
                                    ((self.x + x) * BLOCK_SIZE, (self.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def clear_lines():
    global board, score
    
    # Find completed rows (no empty cells)
    completed_rows = []
    for y in range(ROWS):
        if all(cell != 0 for cell in board[y]):
            completed_rows.append(y)
    
    # Update score based on number of completed rows
    lines_cleared = len(completed_rows)
    score += lines_cleared * 100
    
    # If no lines were cleared, return early
    if lines_cleared == 0:
        return
    
    # Create a new board without the completed rows
    new_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    new_row = ROWS - 1
    
    # Copy non-completed rows to the new board, bottom-up
    for old_row in range(ROWS - 1, -1, -1):
        if old_row not in completed_rows:
            new_board[new_row] = board[old_row].copy()
            new_row -= 1
    
    board = new_board

def show_game_over_screen():
    global score, board
    screen.fill((0, 0, 0))
    
    # Game Over text
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont(None, 36)
    
    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = font_small.render("Press ENTER to restart", True, (0, 255, 0))
    quit_text = font_small.render("Press ESC to quit", True, (255, 165, 0))
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - game_over_text.get_height() // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT * 2 // 3 - restart_text.get_height() // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT * 2 // 3 + 40))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    # Reset game
                    score = 0
                    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                    waiting = False
                elif event.key == pygame.K_ESCAPE:  # Escape key
                    pygame.quit()
                    sys.exit()
        
        clock.tick(FPS)

def main():
    global score
    
    # Set up the game
    pygame.display.set_caption("Tetris")
    game_active = True
    
    while game_active:
        # Start a new game
        score = 0
        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        
        current_piece = Piece()
        next_piece = Piece()  # Prepare the next piece
        
        fall_time = 0
        fall_speed = 500  # Starting speed in milliseconds
        last_fall_speed_increase = 0
        paused = False
        
        running = True
        while running:
            # Calculate time since last frame
            dt = clock.tick(FPS)
            fall_time += dt
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        current_piece.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        if current_piece.move(0, 1):
                            fall_time = 0  # Reset fall time
                    elif event.key == pygame.K_UP:
                        current_piece.rotate()
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
            
            if paused:
                continue
                
            # Move piece down automatically
            if fall_time >= fall_speed:
                if not current_piece.collision(0, 1):
                    current_piece.move(0, 1)
                else:
                    # The piece can't move down, place it on the board
                    current_piece.place()
                    
                    # Check for completed lines
                    clear_lines()
                    
                    # Get the next piece
                    current_piece = next_piece
                    next_piece = Piece()
                    
                    # Check if the new piece can be placed
                    if current_piece.collision(0, 0):
                        running = False  # Game over
                
                fall_time = 0
            
            # Draw everything
            screen.fill((30, 30, 30))
            draw_board()
            current_piece.draw()
            
            # Display score
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            
            pygame.display.update()
        
        # Game over - show the game over screen
        show_game_over_screen()

if __name__ == "__main__":
    main()