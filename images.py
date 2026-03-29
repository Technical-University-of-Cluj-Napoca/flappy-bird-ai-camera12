from config import *
MEDAL_SIZE = (60, 60)
bg = pygame.image.load('Assets/background-day.png').convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_img = pygame.image.load('Assets/start_btn.png').convert_alpha()
button_width = start_img.get_width() // 2
button_height = start_img.get_height() // 2
start_img = pygame.transform.scale(start_img, (button_width, button_height))
restart_img = pygame.image.load('Assets/restart_btn.png').convert_alpha()
restart_img = pygame.transform.scale(restart_img, (button_width, button_height))
bronze_img = pygame.image.load('Assets/bronze.png').convert_alpha()
silver_img = pygame.image.load('Assets/silver.png').convert_alpha()
gold_img = pygame.image.load('Assets/gold.png').convert_alpha()
platinum_img = pygame.image.load('Assets/platinum.png').convert_alpha()
bronze_img = pygame.transform.scale(bronze_img, MEDAL_SIZE)
silver_img = pygame.transform.scale(silver_img, MEDAL_SIZE)
gold_img = pygame.transform.scale(gold_img, MEDAL_SIZE)
platinum_img = pygame.transform.scale(platinum_img, MEDAL_SIZE)
digits_imgs = []
for i in range(10):
    digit_img = pygame.image.load(f'Assets/UI/Numbers/{i}.png').convert_alpha()
    digit_img = pygame.transform.scale(digit_img, (30, 40))
    digits_imgs.append(digit_img)
game_over_img = pygame.image.load('Assets/UI/gameover.png').convert_alpha()