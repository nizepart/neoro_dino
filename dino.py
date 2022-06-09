import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)
jump_event = pygame.event.Event(pygame.KEYDOWN, attr1='jumpEvent')

white = (255, 255, 255)
black = (0, 0, 0)


# Classes


class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super(Cloud, self).__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super(Dino, self).__init__()
        # pygame.sprite.Sprite.__init__(self)
        self.running_sprites = []
        self.ducking_sprites = []

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino1.png"), (80, 100)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Dino2.png"), (80, 100)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.down = 4.5
        self.up = -7
        self.is_jumping = False

    def jump(self):
        if self.rect.centery >= 340:
            jump_sfx.play()
            self.is_jumping = True

    def apply_gravity(self):
        if self.rect.centery <= 340 and self.is_jumping is False:
            self.rect.centery += self.down
        elif self.rect.centery >= 150 and self.is_jumping is True:
            self.rect.centery += self.up
            if self.rect.centery <= 150:
                self.is_jumping = False

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.running_sprites[int(self.current_image)]


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super(Cactus, self).__init__()
        # pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load('assets/cacti/cactus{}.png'.format(i)), (80, 80))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


# Variables


game_speed = 5
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

# Surfaces

ground = pygame.image.load("assets/ground.png")
ground = pygame.transform.scale(ground, (1280, 20))
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))
cloud = pygame.image.load("assets/cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Groups

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()

# Objects
dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# Sounds
death_sfx = pygame.mixer.Sound("assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("assets/sfx/jump.mp3")

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)


# Functions


def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, black)
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render('Score: {}'.format(int(player_score)), True, black)
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()


def run_game_cycle():
    global game_over, obstacle_spawn, ground_x, game_speed, player_score, obstacle_timer
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == CLOUD_EVENT:
                current_cloud_y = random.randint(50, 300)
                current_cloud = Cloud(cloud, 1380, current_cloud_y)
                cloud_group.add(current_cloud)
            if event.type == pygame.KEYDOWN or event == jump_event:
                # if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0

        screen.fill(white)

        # Collisions
        if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
            game_over = True
            death_sfx.play()
        if game_over:
            end_game()

        if not game_over:
            game_speed += 0.0025
            if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
                points_sfx.play()

            if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
                obstacle_spawn = True

            if obstacle_spawn:
                obstacle_random = random.randint(1, 50)
                if obstacle_random in range(1, 7):
                    new_obstacle = Cactus(1280, 340)
                    obstacle_group.add(new_obstacle)
                    obstacle_timer = pygame.time.get_ticks()
                    obstacle_spawn = False

            player_score += 0.1
            player_score_surface = game_font.render(
                str(int(player_score)), True, black)
            screen.blit(player_score_surface, (1150, 10))

            cloud_group.update()
            cloud_group.draw(screen)

            dino_group.update()
            dino_group.draw(screen)

            obstacle_group.update()
            obstacle_group.draw(screen)

            ground_x -= game_speed

            screen.blit(ground, (ground_x, 360))
            screen.blit(ground, (ground_x + 1280, 360))

            if ground_x <= -1280:
                ground_x = 0

        clock.tick(120)
        pygame.display.update()


def invoke_jump_event():
    pygame.event.post(jump_event)