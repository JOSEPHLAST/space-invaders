import pygame

class Laser:
    """Handles the lasers."""
    def __init__(self, si_game, x, y):
        self.laser_image = None
        self.settings = si_game.settings
        self.screen = si_game.screen
        self.screen_rect = si_game.screen_rect
        self.x, self.y = x, y
        self.laser_speed = 0

    def collide(self, obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

    def collision(self, obj):
        return self.collide(self, obj)
    
    def update_laser(self):
        """Update the laser's position on the screen."""
        self.y += self.laser_speed
    
    def draw_laser(self):
        """Draws the laser to the screen."""
        self.screen.blit(self.laser_image, (self.x, self.y))

class EnemyLaser(Laser):
    """Creates an enemy laser instance."""
    color_map = {
        "red": pygame.image.load("assets/pixel_laser_red.png"),
        "green": pygame.image.load("assets/pixel_laser_green.png"),
        "blue": pygame.image.load("assets/pixel_laser_blue.png")
    }

    def __init__(self, si_game, x, y, color):
        super().__init__(si_game, x, y)
        self.laser_image = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.laser_image)
        self.laser_speed = self.settings.enemy_laser_speed
        self.color = color

class PlayerLaser(Laser):
    """Creates a player laser instance."""
    def __init__(self, si_game, x, y):
        super().__init__(si_game, x, y)
        self.laser_image = pygame.image.load("assets/pixel_laser_yellow.png")
        self.mask = pygame.mask.from_surface(self.laser_image)
        self.laser_speed = self.settings.player_laser_speed