import pygame
from random import randrange, choice
from settings import Settings
from ship import EnemyShip, PlayerShip
from laser import EnemyLaser, PlayerLaser
pygame.font.init()
pygame.mixer.init()

class SpaceInvaders:
    """The main game class."""
    def __init__(self):
        self.settings = Settings()
        self.screen_width, self.screen_height = self.settings.screen_dimensions
        self.screen = pygame.display.set_mode((self.settings.screen_dimensions))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Space Invaders")
        self.bg_image = pygame.transform.scale(pygame.image.load("assets/background-black.png"), (self.settings.screen_dimensions))
        self.run = False
        self.player_ship = PlayerShip(self, (self.screen_width - 100)//2, self.screen_height - 100)
        self.main_font = pygame.font.SysFont("comicsans", 30)
        self.lost_font = pygame.font.SysFont("comicsans", 40)
        self.level = self.settings.level
        self.lives = self.settings.lives
        self.score = self.settings.score
        self.player_laser = PlayerLaser(self, self.player_ship.x, self.player_ship.y)
        self.enemy_ship = EnemyShip(self, randrange(50, self.screen_width - 100), randrange(-1500 + self.level*5, -100), self._choose_color())
        self.fire_sound = pygame.mixer.Sound("assets/red.mp3")
        self.hit_sound = pygame.mixer.Sound("assets/yellow.mp3")
        self.gameover_sound = pygame.mixer.Sound("assets/wrong.mp3")
        self.collision_sound = pygame.mixer.Sound("assets/kick-bass.mp3")
        self.new_level_sound = pygame.mixer.Sound("assets/tada.mp3")
        self.offscreen_enemy = pygame.mixer.Sound("assets/tie.mp3")

    def main(self):
        """Runs the game."""
        self.run = True
        clock = pygame.time.Clock()

        while self.run:
            clock.tick(700)
            self._check_events()
            self._update_enemies()
            self._update_enemy_laser()
            self._update_player_laser()
            self._gameover()
            self._draw()
            if self.run == False:
                pygame.time.delay(3000)
                self.__init__()
                self.main_menu()

    def _choose_color(self):
        return choice(["red", "green", "blue"])

    def _check_events(self):   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_ship.handle_ship_movement("left")
        if keys[pygame.K_RIGHT]:
            self.player_ship.handle_ship_movement("right")
        # if keys[pygame.K_UP]:
        #     self.player_ship.handle_ship_movement("up")
        # if keys[pygame.K_DOWN]:
        #     self.player_ship.handle_ship_movement("down")
        if keys[pygame.K_SPACE]:
            # self.fire_sound.play()
            self.player_ship.shoot_laser(self)
        if keys[pygame.K_q]:
            pygame.quit()

    def _update_enemies(self):
        if len(self.settings.enemies) == 0:
            self.level += 1
            self.settings.wave_length += 3
            if self.level > 1:
                self.settings.enemy_speed += 0.1
                self.settings.enemy_laser_speed += 0.1
                self.new_level_sound.play()
                pygame.time.delay(1000)
            
                level_label = self.lost_font.render(f"Level {self.level}", 1, self.settings.text_color)
                self.screen.blit(level_label, ((self.screen_width - level_label.get_width())//2, 100))
                pygame.display.update()
                pygame.time.delay(1000)
                level_label = self.lost_font.render(f"", 1, self.settings.text_color)
                self.screen.blit(level_label, ((self.screen_width - level_label.get_width())//2, 100))
                pygame.display.update()
            
            for _ in range(self.settings.wave_length):
                enemy = EnemyShip(self, randrange(50, self.screen_width - 100), randrange(-1500 + self.level*5, -100), self._choose_color())
                self.settings.enemies.append(enemy)

        for enemy in self.settings.enemies[:]:
            enemy.move()

            if randrange(0, 20*60//self.level) == 1:
                enemy.shoot_laser(self)

            if self.player_laser.collide(enemy, self.player_ship):
                if enemy.color == "red":
                    self.player_ship.health -= 20
                elif enemy.color == "green":
                    self.player_ship.health -= 10
                elif enemy.color == "blue":
                    self.player_ship.health -= 5
                self.settings.enemies.remove(enemy)
                self.hit_sound.play()
            elif enemy.y + enemy.ship_image.get_height() > self.screen_height:
                self.lives -= 1
                self.offscreen_enemy.play()
                self.settings.enemies.remove(enemy)

    def _update_enemy_laser(self):
        self.enemy_ship.cool_down(self.settings.enemy_cooldown)
        for laser in self.settings.enemy_lasers:
            laser.update_laser()
            if laser.y >= self.screen_width:
                self.settings.enemy_lasers.remove(laser)
            elif laser.collision(self.player_ship):
                if laser.color == "red":
                    self.player_ship.health -= 10
                elif laser.color == "green":
                    self.player_ship.health -= 5
                elif laser.color == "blue":
                    self.player_ship.health -= 3
                self.hit_sound.play()
                self.settings.enemy_lasers.remove(laser)
            elif laser.y + laser.laser_image.get_height() < 0:
                self.settings.enemy_lasers.remove(laser)
            else:
                for p_laser in self.settings.lasers:
                    if laser.collision(p_laser):
                        self.collision_sound.play()
                        self.settings.enemy_lasers.remove(laser)
                        self.settings.lasers.remove(p_laser)

    def _update_player_laser(self):
        self.player_ship.cool_down(self.settings.player_cooldown)
        for laser in self.settings.lasers:
            laser.update_laser()
            if laser.y <= 0:
                self.settings.lasers.remove(laser)
            else:
                for enemy in self.settings.enemies:
                    if laser.collision(enemy):
                        if laser in self.settings.lasers:
                            self.settings.lasers.remove(laser)
                        self.settings.enemies.remove(enemy)
                        if enemy.color == "red":
                            self.score += 5
                        elif enemy.color == "green":
                            self.score += 3
                        elif enemy.color == "blue":
                            self.score += 1

    def _gameover(self):
        if self.lives <= 0 or self.player_ship.health <= 0:
            self.gameover_sound.play()
            self.run = False 
    
    def main_menu(self):
        title_font = pygame.font.SysFont("comicsans", 60)
        begin_font = pygame.font.SysFont("comicsans", 35)
        name_font = pygame.font.SysFont("comicsans", 20)
        run = True

        while run:
            self.screen.blit(self.bg_image, (0, 0))
            title_label = title_font.render("SPACE INVADERS", 1, (self.settings.text_color))
            begin_label = begin_font.render("Press the mouse to begin...", 1, (self.settings.text_color))
            name_label = name_font.render("# JOSEPHLAST", 1, (self.settings.text_color))
            self.screen.blit(title_label, ((self.screen_rect.centerx - title_label.get_width()//2), 100))
            self.screen.blit(begin_label, ((self.screen_rect.centerx - begin_label.get_width()//2), 350))
            self.screen.blit(name_label, ((self.screen_rect.centerx - name_label.get_width()//2), 550))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()

    def _draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        score_label = self.main_font.render(f"Score: {self.score}", 1, self.settings.text_color)
        lives_label = self.main_font.render(f"Lives: {self.lives}", 1, self.settings.text_color)
        self.screen.blit(lives_label, (10, 10))
        self.screen.blit(score_label, (self.screen_rect.right - score_label.get_width() - 10, 10))

        for laser in self.settings.enemy_lasers:
            laser.draw_laser()

        for laser in self.settings.lasers:
            laser.draw_laser()
        
        for enemy in self.settings.enemies:
            enemy.blit_ship()

        self.player_ship.blit_ship()

        if self.run == False:
            lost_text = self.lost_font.render(f"You lost!", 1, self.settings.text_color)
            self.screen.blit(lost_text, ((self.screen_width - lost_text.get_width())//2, (self.screen_height - lost_text.get_height())//2))

        pygame.display.update()


if __name__ == "__main__":
    si_game = SpaceInvaders()
    si_game.main_menu()