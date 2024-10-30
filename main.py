import sys
import pygame
from components.game import Game

def show_start_menu(screen, font):
    WIDTH, HEIGHT = Game.WIDTH, Game.HEIGHT
    background_image = pygame.image.load("assets/sprites/menu-inicial.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    menu_options = ["Start", "Credits", "Exit"]
    selected_option = 0

    while True:
        screen.blit(background_image, (0, 0))
        for i, option in enumerate(menu_options):
            main_color = (255, 255, 255) if i == selected_option else (200, 200, 200)
            shadow_color = (50, 50, 50)

            text_surface = font.render(option, True, main_color)
            shadow_surface = font.render(option, True, shadow_color)

            x_pos = WIDTH // 2 - text_surface.get_width() // 2
            y_pos = 400 + i * 50

            screen.blit(shadow_surface, (x_pos + 2, y_pos + 2))
            screen.blit(text_surface, (x_pos, y_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        game = Game()
                        game.run()
                    elif selected_option == 1:
                        show_credits_screen(screen, font)
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()

def show_credits_screen(screen, font):
    WIDTH, HEIGHT = Game.WIDTH, Game.HEIGHT
    background_image = pygame.image.load("assets/sprites/credits-background.jpg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    credits_text = [
        "Dirty Motors", "", "Developed by:", "Gustavo O. Guidetti", "Luis F. Brasil", "",
        "Music: Rock n' Roll Racing [1993]", "", "Special Thanks:", "Prof Eduardo H. M. Cruz",
        "Prof Helio T. Kamakawa", "", "", "", "Press ESC to return to the main menu"
    ]

    while True:
        screen.blit(background_image, (0, 0))
        for i, line in enumerate(credits_text):
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 100 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def main():
    pygame.init()
    screen = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
    pygame.display.set_caption("Dirty Motors")
    font = pygame.font.Font(None, 36)

    while True:
        show_start_menu(screen, font)

if __name__ == "__main__":
    main()
