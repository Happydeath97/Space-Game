import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VESMÍRNÁ ŘEŽBA!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT_SOUND.set_volume(0.15)
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND.set_volume(0.2)

YELLOW_WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Yellowwins.mp3'))
RED_WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Redwins.mp3'))

HEART_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 10
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
METEOR_WIDTH, METEOR_HEIGHT = 20, 20

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                                                  (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                                               (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
METEOR_IMAGE = pygame.image.load(os.path.join('Assets', 'meteor.png'))
METEOR = pygame.transform.scale(METEOR_IMAGE, (METEOR_WIDTH, METEOR_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, meteors, red_heart, yellow_heart):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_heart_text = HEART_FONT.render("Health: " + str(red_heart), 1, WHITE)
    yellow_heart_text = HEART_FONT.render("Health: " + str(yellow_heart), 1, WHITE)
    WIN.blit(red_heart_text, (WIDTH - red_heart_text.get_width() - 10, 10))
    WIN.blit(yellow_heart_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for meteor in meteors:
        WIN.blit(METEOR, (meteor.x, meteor.y))

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 2:  # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - yellow.height - 15:  # Down
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - yellow.width + 15:  # Right
        yellow.x += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Left
        red.x -= VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 2:  # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - red.height - 15:  # Down
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - red.width + 15:  # Right
        red.x += VEL

def handle_meteors(meteors, yellow, red):
    for meteor in meteors:
        meteor.y += BULLET_VEL
        if red.colliderect(meteor):
            pygame.event.post(pygame.event.Event(RED_HIT))
            meteors.remove(meteor)
        elif yellow.colliderect(meteor):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            meteors.remove(meteor)
        else:
            if meteor.y > HEIGHT:
                meteors.remove(meteor)
            else:
                pass

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    if text == "Yellow WINS!":
        YELLOW_WIN_SOUND.play()
    else:
        RED_WIN_SOUND.play()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect((WIDTH * 4) // 5, (HEIGHT//2) - (SPACESHIP_HEIGHT//2), SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect((WIDTH // 5) - SPACESHIP_WIDTH, (HEIGHT//2) - (SPACESHIP_HEIGHT//2),
                         SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []
    meteors = []

    red_heart = 10
    yellow_heart = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    meteor = pygame.Rect(random.randrange(WIDTH), 0, METEOR_WIDTH, METEOR_HEIGHT)
                    meteors.append(meteor)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 5, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    meteor = pygame.Rect(random.randrange(WIDTH), 0, METEOR_WIDTH, METEOR_HEIGHT)
                    meteors.append(meteor)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_heart -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_heart -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_heart <= 0:
            winner_text = "Yellow WINS!"

        if yellow_heart <= 0:
            winner_text = "Red WINS!"

        if winner_text != "":
            draw_winner(winner_text)

            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        handle_meteors(meteors, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, meteors, red_heart, yellow_heart)

    main()


if __name__ == "__main__":
    main()
