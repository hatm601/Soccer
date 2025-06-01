import pygame
import math

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Soccer")
clock = pygame.time.Clock()
goal_width = 100
goal_height = 200
player_radius = 30
player2_radius = 30
player_head_radius = 20
player_body_length = 40
player_leg_length = 30
player_height = player_head_radius * 2 + player_body_length + player_leg_length
speed = 5
is_jumping = False
player2_is_jumping = False
jump_velocity = -10
gravity = 0.3
velocity_y = 0
player2_velocity_y = 0
ground_y = 500
player_x, player_y = 300, 0
player_speed = 5
player2_x, player2_y = 800, 0
player2_speed = 5
player2_y = ground_y
player_y = ground_y
ground_height = SCREEN_HEIGHT - ground_y
ball_gravity = 0.5
ball_x, ball_y = 500, 500
ball_radius = 20
ball_velocity_x = 0
ball_velocity_y = 0
friction = 0.98  
left_goal_x = 0
right_goal_x = SCREEN_WIDTH - goal_width
GOAL_WIDTH = 100
GOAL_HEIGHT = 150
GOAL_Y = ground_y - GOAL_HEIGHT
ball_start_x = SCREEN_WIDTH // 2
ball_start_y = ground_y - ball_radius
player_distance = 200
player_x_start = ball_start_x - player_distance
player2_x_start = ball_start_x + player_distance
player_y_start = ground_y
player2_y_start = ground_y
score_red = 0
score_blue = 0
font = pygame.font.SysFont(None, 60)
game_over = False
animation_frame = 0
animation_timer = 0
animation_interval = 10
player_moving = False
player2_moving = False
left_goal_rect = pygame.Rect(left_goal_x, GOAL_Y, GOAL_WIDTH, ground_y - GOAL_Y)
right_goal_rect = pygame.Rect(right_goal_x, GOAL_Y, GOAL_WIDTH, ground_y - GOAL_Y)
GAME_DURATION = 90
start_ticks = pygame.time.get_ticks()
sudden_death = False
def show_countdown(screen, font, screen_width, screen_height):
    for i in range(3, 0, -1):
        screen.fill((64, 199, 255))
        pygame.draw.rect(screen, (67, 200, 10), (0, ground_y, SCREEN_WIDTH, ground_height))
        text = font.render(str(i), True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
    screen.fill((64, 199, 255))
    pygame.draw.rect(screen, (67, 200, 10), (0, ground_y, SCREEN_WIDTH, ground_height))
    text = font.render("GO!", True, (0, 200, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000)
show_countdown(screen, font, SCREEN_WIDTH, SCREEN_HEIGHT)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not is_jumping:
                is_jumping = True
                velocity_y = jump_velocity
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not player2_is_jumping:
                player2_is_jumping = True
                player2_velocity_y = jump_velocity
    key_pressed = pygame.key.get_pressed()
    player_moving = False
    player2_moving = False
    if key_pressed[pygame.K_LEFT]:
        player_x -= player_speed
        player_moving = True
    if key_pressed[pygame.K_RIGHT]:
        player_x += player_speed
        player_moving = True
    if is_jumping:
        player_y += velocity_y
        velocity_y += gravity
        if player_y >= ground_y:
            player_y = ground_y
            velocity_y = 0
            is_jumping = False
    if player2_is_jumping:
        player2_y += player2_velocity_y
        player2_velocity_y += gravity
        if player2_y >= ground_y:
           player2_y = ground_y
           player2_velocity_y = 0
           player2_is_jumping = False
    if ball_x < player2_x:
        player2_x -= player2_speed
        player2_moving = True
    elif ball_x > player2_x:
       player2_x += player2_speed
       player2_moving = True
    if not player2_is_jumping and ball_y < player2_y - 50 and abs(player2_x - ball_x) < 100:
       player2_is_jumping = True
       player2_jump_velocity = -10
    if player2_x - player2_radius < 0:
        player2_x = player2_radius     
    if player2_x + player2_radius > SCREEN_WIDTH:
        player2_x = SCREEN_WIDTH - player2_radius
    if player2_y - player2_radius < 0:
        player2_y = player2_radius
    if player_x - player_radius < 0:
        player_x = player_radius
    if player_x + player_radius > SCREEN_WIDTH:
        player_x = SCREEN_WIDTH - player_radius
    distance = math.hypot(player_x - ball_x, player_y - ball_y)
    if distance < player_radius + ball_radius:
        dx = ball_x - player_x
        direction = 1 if dx >= 0 else -1
        ball_velocity_x = 20 * direction
        ball_velocity_y = -17
    distance2 = math.hypot(player2_x - ball_x, player2_y - ball_y)
    if distance2 < player2_radius + ball_radius:
        dx = ball_x - player2_x
        direction = 1 if dx >= 0 else -1
        ball_velocity_x = 20 * direction
        ball_velocity_y = -17
    ball_velocity_y += ball_gravity
    ball_x += ball_velocity_x
    ball_y += ball_velocity_y
    ball_velocity_x *= friction
    ball_velocity_y *= friction
    if ball_x - ball_radius < 0:
        ball_x = ball_radius
        ball_velocity_x *= -0.6
    if ball_x + ball_radius > SCREEN_WIDTH:
        ball_x = SCREEN_WIDTH - ball_radius
        ball_velocity_x *= -0.6
    if ball_y + ball_radius > ground_y:
        ball_y = ground_y - ball_radius
        ball_velocity_y *= -0.6
        if abs(ball_velocity_y) < 1:
            ball_velocity_y = 0
    left_goal_x = 0
    right_goal_x = SCREEN_WIDTH - 100
    goal_width = 100
    goal_y = ground_y - 100
    prev_ball_x = ball_x
    prev_ball_y = ball_y
    if distance < player_radius + ball_radius:
        dx = ball_x - player_x
        direction = 1 if dx >= 0 else -1
        ball_velocity_x = 20 * direction
        ball_velocity_y = -17
    if distance2 < player2_radius + ball_radius:
        dx = ball_x - player2_x
        direction = 1 if dx >= 0 else -1
        ball_velocity_x = 20 * direction
        ball_velocity_y = -17
    if not game_over:
        if left_goal_rect.collidepoint(ball_x, ball_y) and ball_velocity_x < 0:
            if not sudden_death or (sudden_death and score_red == score_blue):
                score_blue += 1
                player_x, player_y = player_x_start, player_y_start
                player2_x, player2_y = player2_x_start, player2_y_start
                ball_x, ball_y = ball_start_x, ball_start_y
                is_jumping = False
                player2_is_jumping = False
            if sudden_death:
                game_over = True
                running = False
        if right_goal_rect.collidepoint(ball_x, ball_y) and ball_velocity_x > 0:
            if not sudden_death or (sudden_death and score_red == score_blue):
                score_red += 1
                handball_by = None
                handball_message = ""
                player_x, player_y = player_x_start, player_y_start
                player2_x, player2_y = player2_x_start, player2_y_start
                ball_x, ball_y = ball_start_x, ball_start_y
                is_jumping = False
                player2_is_jumping = False
            if sudden_death and (score_red != score_blue):
                game_over = True
                running = False
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, GAME_DURATION - int(seconds_passed))
    if time_left <= 0 and not sudden_death:
        if score_red == score_blue:
            sudden_death = True
        else:
            game_over = True
            running = False
    animation_timer += 1
    if animation_timer >= animation_interval:
        animation_timer = 0
        animation_frame = (animation_frame + 1) % 2
    def draw_stickman(screen, x, y, color, moving, frame):
        head_radius = 20
        body_length = 40
        arm_length = 25
        leg_length = 30
        body_top = y - leg_length - body_length
        head_center_y = body_top - head_radius
        pygame.draw.circle(screen, color, (x, head_center_y), head_radius)
        pygame.draw.line(screen, color, (x, body_top), (x, y - leg_length), 3)
        if moving and frame == 1:
            pygame.draw.line(screen, color, (x - arm_length, body_top + 10), (x + arm_length, body_top + 30), 3)
        else:
            pygame.draw.line(screen, color, (x - arm_length, body_top + 20), (x + arm_length, body_top + 20), 3)
        if moving and frame == 1:
            pygame.draw.line(screen, color, (x, y - leg_length), (x - 20, y), 3)
            pygame.draw.line(screen, color, (x, y - leg_length), (x + 20, y), 3)
        else:
            pygame.draw.line(screen, color, (x, y - leg_length), (x - 15, y), 3)
            pygame.draw.line(screen, color, (x, y - leg_length), (x + 15, y), 3)
    screen.fill((64, 199, 255))
    pygame.draw.rect(screen, (67, 200, 10), (0, ground_y, SCREEN_WIDTH, ground_height))
    draw_stickman(screen, int(player_x), int(player_y), (255, 0, 0), player_moving, animation_frame)
    draw_stickman(screen, int(player2_x), int(player2_y), (0, 0, 255), player2_moving, animation_frame)
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.rect(screen, (255, 255, 255), (0, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT), 4)
    pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH - GOAL_WIDTH, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT), 4)
    P1_score_text = font.render(f"P1(Human): {score_red}", True, (0, 0, 0))
    P2_score_text = font.render(f"P2(Computer): {score_blue}", True, (0, 0, 0))
    screen.blit(P1_score_text, (20, 20))
    screen.blit(P2_score_text, (20, 65))
    if sudden_death:
        timer_text = font.render("Sudden Death!", True, (255, 0, 0))
    else:
        timer_text = font.render(f"Time Left: {time_left}s", True, (0, 0, 0))
    screen.blit(timer_text, (SCREEN_WIDTH - 310, 20))
    if game_over:
        if sudden_death:
            if score_red > score_blue:
                text_surface = font.render("P1(Human) Has Won In Sudden Death!", True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
            elif score_blue > score_red:
                text_surface = font.render("P2(Computer) Has Won In Sudden Death!", True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
        else:
            if score_red > score_blue:
                text_surface = font.render("The Winner is Player 1(Human)!", True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
            elif score_blue > score_red:
                text_surface = font.render("The Winner is Player 2(Computer)!", True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
            else:                
                text_surface = font.render("It's A Tie!", True, (0, 255, 0))
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.time.delay(1500)

pygame.quit()

