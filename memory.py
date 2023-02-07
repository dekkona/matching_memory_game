# Memory Game
# Eric Kim
# 27 Nov 2020

import pygame, random, time


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Memory')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.images = []
 
        image1 = pygame.image.load("image1.bmp")
        self.images.append(image1)
        image2 = pygame.image.load("image2.bmp")
        self.images.append(image2)
        image3 = pygame.image.load("image3.bmp")
        self.images.append(image3)
        image4 = pygame.image.load("image4.bmp")
        self.images.append(image4)
        image5 = pygame.image.load("image5.bmp")
        self.images.append(image5)
        image6 = pygame.image.load("image6.bmp")
        self.images.append(image6)
        image7 = pygame.image.load("image7.bmp")
        self.images.append(image7)
        image8 = pygame.image.load("image8.bmp")        
        self.images.append(image8)
        
        self.images = self.images + self.images   
        random.shuffle(self.images)   
        
        # Length of tiles for sides
        self.board_size = 4
        self.board = []  
        self.create_board()  
        self.filled = 0
        # Keeps track of selected images for future comparison
        self.sel_img = []
        self.choice2 = False 
        self.match = False
        # Keeps track of first tile clicked on
        self.tile1 = None
        # Score is counted in seconds, the lower the better
        self.score = 0
        
    def create_board(self):
        # Square board
        width = self.surface.get_height()//self.board_size
        height = self.surface.get_height()//self.board_size
        
        for row_idx in range(0, self.board_size):
            # create row as an empty list
            row = []
            # for each column index
            for col_idx in range(0, self.board_size):
                #create row using column index and row index
                x = col_idx * width
                y = row_idx * height
                tile = Tile(x, y, width, height, self.surface, self.images[0])
                self.images.remove(self.images[0])
                # append tile to row
                row.append(tile)
            # append row to board
            self.board.append(row)    

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
                
    def handle_mouse_up(self, event):
        # Handles what happens when mouse is clicked
        pos = pygame.mouse.get_pos()
        for row in self.board:
            for tile in row:
                if tile.is_hidden():
                    if tile.clicked(pos) and not self.choice2:
                        self.sel_img.append(tile.get_image())
                        self.choice2 = True
                        self.tile1 = tile
                        tile.change_form(0) # 0 = Clicked on
                        
                    elif tile.clicked(pos) and self.choice2:
                        tile.change_form(0)
                        self.draw()
                        if tile.match(self.sel_img[0]):
                            tile.change_form(1) # 1 = Permanent show
                            self.filled = self.filled + 2 # Pairs of matching tiles
                            print(self.filled)
                            self.match = False
                        else:
                            pygame.time.wait(777)
                            self.tile1.change_form(2) # 2 = Revert to hidden
                            tile.change_form(2)   
                        self.sel_img.remove(self.sel_img[0])
                        self.choice2 = False
                        print(self.choice2)
                 
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        # draw the board
        self.surface.fill(self.bg_color)
        
        for row in self.board:
            for tile in row:
                tile.draw()
                
        text_font = pygame.font.SysFont('Comic Sans', 64, bold=True, italic=False)
        text_image = text_font.render(str(int(self.score)), True, pygame.Color('white'))  
        text_topright = (445, 0)
        self.surface.blit(text_image, text_topright)             
                
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game score
        self.score = pygame.time.get_ticks() / 1000     

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        # Game ends when all tiles are exposed
        if self.filled == self.board_size ** 2: # Total of tiles in board 
            self.continue_game = False
        
class Tile:
    # an object of this class represents a Rectangular tile
    def __init__(self, x, y, width, height, surface, image):
        # Initialize tile
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = surface 
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.hide = pygame.image.load("image0.bmp")
        self.hidden = True
        self.temp = False
        self.perm = False
                
    def draw(self):
        #Draws tile object
        color = pygame.Color('black')
        border_width = 3
        self.draw_hidden()
        pygame.draw.rect(self.surface, color, self.rect, border_width)
        
        if self.temp or self.perm:
            self.hidden = False
            self.draw_content()
            pygame.draw.rect(self.surface, color, self.rect, border_width)
        else: 
            self.hidden = True
            self.draw_hidden()
            pygame.draw.rect(self.surface, color, self.rect, border_width)
            
    def draw_content(self): 
        # Draws tile image
        content_x = self.rect.x + (self.rect.width - self.image.get_width()) // 2
        content_y = self.rect.y + (self.rect.width - self.image.get_height()) // 2
        text_pos = (content_x, content_y)
        self.surface.blit(self.image, text_pos)  
        
    def draw_hidden(self):
        # Draws hidden image
        content_x = self.rect.x + (self.rect.width - self.hide.get_width()) // 2
        content_y = self.rect.y + (self.rect.width - self.hide.get_height()) // 2
        text_pos = (content_x, content_y)
        self.surface.blit(self.hide, text_pos)        
    
    def clicked(self, pos):
        # Checks if tile is clicked on
        clicked = False
        if self.rect.collidepoint(pos):
            clicked = True
        return clicked
    
    def match(self, other_tile):
        # Checks if tile is matching
        match = False
        if other_tile == self.image:
            match = True
        return match  
    
    def is_hidden(self):
        # Checks if tile is hidden
        return self.hidden
    
    def get_image(self):
        return self.image    
    
    def change_form(self, check_val):
        # change the hidden status of the tile
        if check_val == 0:
            self.temp = True
        if check_val == 1:
            self.perm = True
        if check_val == 2:
            self.temp = False  
    
main()