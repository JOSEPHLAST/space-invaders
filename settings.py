class Settings:
    def __init__(self):
        """Contains the parameters for the game."""

        # Screen settings
        self.screen_dimensions = 800, 600
        self.level = 0
        self.lives = 5
        self.score = 0
        self.text_color = (255, 255, 255)

        # Ship settings
        self.ship_speed = 5
        self.enemy_speed = 1
        self.enemies = []
        self.wave_length = 3

        # Laser settings
        self.lasers = []
        self.enemy_lasers = []
        self.player_laser_speed = -5
        self.enemy_laser_speed = 1.5
        self.lasers_cooldown = 0
        self.player_cooldown = 30
        self.enemy_cooldown = 200
        self.max_lasers = 5