import pygame
from laser import PlayerLaser, EnemyLaser

class Ship:
    """Handles the ships."""
    def __init__(self, si_game, x, y, health=100):
        self.ship_image = None
        self.x, self.y = x, y
        self.health = health
        self.settings = si_game.settings
        self.screen = si_game.screen
        self.screen_rect = si_game.screen_rect
        self.ship_speed = si_game.settings.ship_speed
        self.enemy_speed = si_game.settings.enemy_speed
        self.color_choice = si_game._choose_color()

    def cool_down(self, cooldown):
        if self.settings.lasers_cooldown >= cooldown:
            self.settings.lasers_cooldown = 0
        elif self.settings.lasers_cooldown > 0:
            self.settings.lasers_cooldown += 1

    def blit_ship(self):
        """Blit the player's ship to the screen."""
        self.screen.blit(self.ship_image, (self.x, self.y - 15))

class EnemyShip(Ship):
    """Creates an enemy ship instance."""
    color_map = {
        "red": pygame.image.load("assets/pixel_ship_red_small.png"),
        "green": pygame.image.load("assets/pixel_ship_green_small.png"),
        "blue": pygame.image.load("assets/pixel_ship_blue_small.png")
    }

    def __init__(self, si_game, x, y, color, health=100):
        super().__init__(si_game, x, y, health)
        self.ship_image = self.color_map[color]
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.color = color

    def move(self):
        self.y += self.enemy_speed

    def shoot_laser(self, si_game):
        if self.settings.lasers_cooldown == 0:
            laser = EnemyLaser(si_game, self.x - 25 if self.color == "blue" else self.x - 15, self.y, self.color)
            self.settings.enemy_lasers.append(laser)
            self.settings.lasers_cooldown = 1

class PlayerShip(Ship):
    """Creates a player ship instance."""
    def __init__(self, si_game, x, y, health=100):
        super().__init__(si_game, x, y, health)
        self.ship_image = pygame.image.load("assets/pixel_ship_yellow.png")
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

    def handle_ship_movement(self, direction):
        """Handles the player's ship movements."""
        if direction == "left" and self.x > self.screen_rect.left:
            self.x -= self.ship_speed
        if direction == "right" and self.x + self.ship_image.get_width() < self.screen_rect.right:
            self.x += self.ship_speed

    def shoot_laser(self, si_game):
        if len(self.settings.lasers) < self.settings.max_lasers:
            if self.settings.lasers_cooldown == 0:
                laser = PlayerLaser(si_game, self.x, self.y - self.ship_image.get_height()//2)
                self.settings.lasers.append(laser)
                self.settings.lasers_cooldown = 1

    def health_bar(self):
        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y + self.ship_image.get_height() - 10, self.ship_image.get_width(), 10))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y + self.ship_image.get_height() - 10, self.ship_image.get_width() * (self.health/self.max_health), 10))

    def blit_ship(self):
        super().blit_ship()
        self.health_bar()