import pygame, sys, random # Pygame set-up & import other files/presets
from pygame.math import Vector2 # Import Vector2 for easier writing and easier movement control later on

# Creates a snake (player)
class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)] # Creates the first 3 body parts of the snake
        self.direction = Vector2(1,0) # Controls the direction of which the snake is moving
        self.new_block = False 
        
        # Loads the images/assets for the snake
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
    
    # Function to draw the snake
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        
        for index,block in enumerate(self.body): 
            x_pos = int(block.x * cell_size) # Searches for the x position of the snake body parts
            y_pos = int(block.y * cell_size) # Searches for the y position of the snake body parts
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size) #Creates the rough snake body
             
            if index == 0:
                screen.blit(self.head, block_rect) # Loads the head image of the snake
                
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect) # Loads the tail image of the snake
            
            # 
            # 
            # Loads the corner images of the snake
            else:
                previous_block = self.body[index + 1] - block # Gets the previous block
                next_block = self.body[index - 1] - block # Gets the next block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect) # Checks if the snake should be vertical
                elif previous_block.y == next_block.y: 
                    screen.blit(self.body_horizontal, block_rect) # Checks if the snake should be horizontal
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    # Checks what direction the head should be facing
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
    
    # Checks what direction the tail should be facing
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
    
    # Controls snake movement according to it's direction
    def move_snake(self):
        if self.new_block == True: 
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
            
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        
    # Adds a new body part to the snake when it eats a fruit
    def add_block(self):
        self.new_block = True
        
        
# Generates a fruit
class FRUIT:
    def __init__(self):
        self.randomize() # Calls the randomize function
    
    # Draws the fruit onto the board
    def draw_fruit(self):
        #create a rectangle
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        
        # Draw the fruit with the graphics
        screen.blit(apple, fruit_rect)
    
    # Generates a random position for the fruit    
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x,self.y)
        

# Game logic
class LOGIC:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    # Continuesly checks the snake's condition
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    # Draws all the elements onto the board
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    # Checks for snake collision with the fruit
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
    
    # Checks if the snake collided with a wall or with its self
    def check_fail(self):
        if  not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    # Quits the game if the snake dies
    def game_over():
        pygame.quit()
        sys.exit()
    
    # Draws the checker style grass for detail
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:    
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                        
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    
    # Generates a score
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True , (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)
        
# Map set-up
cell_size = 40
cell_number = 18

# Pygame set-up
pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load("Graphics/apple.png").convert_alpha()
game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)

#Screen update
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

logic = LOGIC()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE:
            logic.update()
            
        # Event listener
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if logic.snake.direction.y != 1:
                    logic.snake.direction = Vector2(0, -1)
                    
            if event.key == pygame.K_DOWN:
                if logic.snake.direction.y != -1:
                    logic.snake.direction = Vector2(0, 1)
                    
            if event.key == pygame.K_RIGHT:
                if logic.snake.direction.x != -1:
                    logic.snake.direction = Vector2(1, 0)
                    
            if event.key == pygame.K_LEFT:
                if logic.snake.direction.x != 1:
                    logic.snake.direction = Vector2(-1, 0)

    # Final settings
    screen.fill((175, 215, 70))
    logic.draw_elements()
    pygame.display.update()
    clock.tick(60)