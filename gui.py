import pandas as pd
import pygame
import json
from settings import *


pygame.init()

TEST_WIDTH = WIDTH
TEST_HEIGHT = HEIGHT

leaderboard_path = 'leaderboard.csv'

screen = pygame.display.set_mode((TEST_WIDTH, TEST_HEIGHT))
pygame.display.set_caption("Game Over Screen")
font = pygame.font.Font(None, 36)


class gameOverScreen():
    def __init__(self):
        self.font_name_input = pygame.font.Font(None, 28)
        self.name_input = ''
        self.run()

    def read_leaderboard(self):
        df = pd.read_csv(leaderboard_path)
        df_sorted = df.sort_values(by='ROOMS_CLEARED', ascending=False)
        return df_sorted.head(10)

    def handle_new_score(self,player_score=10, player_level=10, player_name=''):
        df = pd.read_csv(leaderboard_path)
        df_sorted = df.sort_values(by='ROOMS_CLEARED', ascending=False)
        leaderboard = df_sorted.head(10)
        
        if len(leaderboard) < 10 or player_score > leaderboard.iloc[-1]['ROOMS_CLEARED']:

            new_entry = pd.DataFrame({
                'NAME': [player_name],
                'LEVEL': [player_level],
                'ROOMS_CLEARED': [player_score]
            })
            leaderboard = pd.concat([leaderboard, new_entry], ignore_index=True)
            
            leaderboard = leaderboard.sort_values(by='ROOMS_CLEARED', ascending=False).head(10)

            leaderboard.to_csv(leaderboard_path, index=False)

    def draw_leaderboard(self):
        leaderboard = self.read_leaderboard()
        leaderboard_y = HEIGHT // 2 + 150  
        for i, row in leaderboard.iterrows():
            player_text = font.render(f"{i+1}. {row['NAME']} - Level {row['LEVEL']} - Rooms Cleared: {row['ROOMS_CLEARED']}", True, 'white')
            screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, leaderboard_y + i * 30))

        name_input_text = self.font_name_input.render(f"Enter your name: {self.name_input}", True, 'white')
        screen.blit(name_input_text, (WIDTH // 2 - name_input_text.get_width() // 2, HEIGHT // 2 + 120))
        return name_input_text

    def run(self, player_score=10, player_level=10):
        input_active = True
        cursor_visible = True
        cursor_timer = pygame.time.get_ticks()

        while True:
            screen.fill('black')

            # Game over text
            game_over_text = font.render("GAME OVER", True, 'red')
            score_text = font.render(f"Your Score: {player_score}", True, 'white')
            continue_text = font.render("Press Space to continue", True, 'white')
            restart_text = font.render("Press R to Restart or Q to Quit", True, 'white')

            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 40))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
            screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 80))

            name = self.draw_leaderboard()

            if pygame.time.get_ticks() - cursor_timer >= 500:
                cursor_visible = not cursor_visible
                cursor_timer = pygame.time.get_ticks()
            
            if cursor_visible:
                cursor_rect = pygame.Rect(WIDTH // 2 + name.get_width() // 2, HEIGHT // 2 + 120, 10, 30)
                pygame.draw.rect(screen, 'white', cursor_rect)
            
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.name_input != '':
                            self.handle_new_score(player_score, player_level, self.name_input)
                            mainMenu()
                        
                    elif event.key == pygame.K_r:
                        if self.name_input != '':
                            self.handle_new_score(player_score, player_level, self.name_input)
                            
                            from main import Game
                            game = Game()
                            game.run()
                        
                    elif event.key == pygame.K_q:
                        if self.name_input != '':
                            self.handle_new_score(player_score, player_level, self.name_input)
                            pygame.quit()                        

                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    else:
                        if len(self.name_input) < 20:  
                            self.name_input += event.unicode

def get_font(size): 
    return pygame.font.SysFont('arial', size, bold=True)


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, height, inside=False, width=654):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = hovering_color, base_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Resize image to match the button height
        self.image = pygame.transform.scale(self.image, (width, height))

        if self.image is None:
            self.image = self.text
        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        if inside:
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos+100))
        else:
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.next_button = None  # Pointer to the next button in the linked list
        self.prev_button = None
        self.height = height  # Store the height for scaling the buttons

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):  # Checks if the pointer is hovering over the button
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False


    def changeColor(self, is_highlighted):
        # Change color based on whether this button is highlighted or not
        if type(is_highlighted) == bool:
            if is_highlighted:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
        else:
            if is_highlighted[0] in range(self.rect.left, self.rect.right) and is_highlighted[1] in range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)

    def setNext(self, next_button):
        self.next_button = next_button

    def setPrev(self, prev_button):
        self.prev_button = prev_button


# Fonts and colors
def get_font(size):
    return pygame.font.Font(None, size)


class mainMenu():
    def __init__(self):
        with open("player_data.json", "r") as file:
            self.data = json.load(file)
            self.currency = self.data.get('total_score', 0)
            self.upgrades = {
                'ATK': self.data.get('ATK', 0),
                'HP': self.data.get('HP', 0),
                'DEF': self.data.get('DEF', 0),
                'SPEED': self.data.get('SPEED', 0)
            }
            self.current_class = self.data.get('selected_class', 0)
            
        self.main_menu = mainMenu

        self.button_height = 720 // 5  # Divide screen height by number of buttons

        self.PLAY_BUTTON = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 250), 
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)
        self.STORE_BUTTON = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 380), 
                             text_input="STORE", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)
        self.LEADERBOARD_BUTTON = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 490), 
                        text_input="LEADERBOARD", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)
        self.CLASS_BUTTON = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 590), 
                text_input="CLASS", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)
        self.QUIT_BUTTON = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 690), 
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)


        self.PLAY_BUTTON.setNext(self.STORE_BUTTON)
        self.STORE_BUTTON.setNext(self.LEADERBOARD_BUTTON)
        self.LEADERBOARD_BUTTON.setNext(self.CLASS_BUTTON)
        self.CLASS_BUTTON.setNext(self.QUIT_BUTTON)
        self.QUIT_BUTTON.setNext(self.PLAY_BUTTON)  

        self.PLAY_BUTTON.setPrev(self.QUIT_BUTTON)
        self.STORE_BUTTON.setPrev(self.PLAY_BUTTON)
        self.LEADERBOARD_BUTTON.setPrev(self.STORE_BUTTON)
        self.CLASS_BUTTON.setPrev(self.LEADERBOARD_BUTTON)
        self.QUIT_BUTTON.setPrev(self.CLASS_BUTTON)  

   
        self.current_button = self.PLAY_BUTTON

        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("UNTITLED DUNGEON GAME", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            screen.fill('black')  

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [self.PLAY_BUTTON, self.STORE_BUTTON, self.LEADERBOARD_BUTTON, self.CLASS_BUTTON, self.QUIT_BUTTON]:
                if button.checkForInput(MENU_MOUSE_POS): # Checks if the pointer is hovering over the button
                    self.current_button = button
                    button.changeColor(MENU_MOUSE_POS)  # Update the button's color based on selection
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.handle_button_action(self.current_button)
                    elif event.key == pygame.K_TAB:
                        self.current_button = self.current_button.next_button  # Move to next button
                    elif event.key == pygame.K_UP:
                        self.current_button = self.current_button.prev_button  # Move to previous button
                    elif event.key == pygame.K_DOWN:
                        self.current_button = self.current_button.next_button  # Move to next button

                # hover logic
                for button in [self.PLAY_BUTTON, self.STORE_BUTTON, self.LEADERBOARD_BUTTON, self.CLASS_BUTTON, self.QUIT_BUTTON]:
                    if button == self.current_button and not button.checkForInput(MENU_MOUSE_POS):
                        button.changeColor(True)  # Highlight button on mouse hover
                    else:
                        button.changeColor(False)  # Revert to base color if not hovered


                    # Keyboard input handling
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.handle_button_action(self.PLAY_BUTTON)
                            break
                        if self.STORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.handle_button_action(self.STORE_BUTTON)
                        if self.LEADERBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.handle_button_action(self.LEADERBOARD_BUTTON)
                        if self.CLASS_BUTTON.checkForInput(MENU_MOUSE_POS):
                            
                            self.handle_button_action(self.CLASS_BUTTON)
                        if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                            self.handle_button_action(self.QUIT_BUTTON)

            pygame.display.update()
    
    def save(self):
        data = {
            'total_score': self.currency,
            'selected_class': self.current_class,
            'ATK': self.upgrades['ATK'],
            'HP': self.upgrades['HP'],
            'SPEED': self.upgrades['SPEED'],
            'DEF': self.upgrades['DEF']
        }
        with open("player_data.json", "w") as file:
            json.dump(data, file)

    def play(self):
        running = True

        while running:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            screen.fill('black')

            menu_text = get_font(45).render("Choose a difficulty", True, 'white')
            menu_text_rect = menu_text.get_rect(center=(640, 100))
            screen.blit(menu_text, menu_text_rect)

            BUTTON_HEIGHT = 700  
            difficulty_1_button = Button(image=pygame.image.load("./assets/vertical_button.png"), pos=(320, 340), 
                                        text_input="EASY", font=get_font(50), base_color="#d7fcd4", hovering_color='white',width=250, inside=True, height=BUTTON_HEIGHT)
            difficulty_2_button = Button(image=pygame.image.load("./assets/vertical_button.png"), pos=(640, 340), 
                                        text_input="MEDIUM", font=get_font(50), base_color="#d7fcd4", hovering_color='white',width=250, inside=True, height=BUTTON_HEIGHT)
            difficulty_3_button = Button(image=pygame.image.load("./assets/vertical_button.png"), pos=(960, 340), 
                                        text_input="HARD", font=get_font(50), base_color="#d7fcd4", hovering_color='white',width=250, inside=True,height=BUTTON_HEIGHT)

            back = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 650), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)

            # Update buttons
            difficulty_1_button.changeColor(OPTIONS_MOUSE_POS)
            difficulty_2_button.changeColor(OPTIONS_MOUSE_POS)
            difficulty_3_button.changeColor(OPTIONS_MOUSE_POS)
            back.changeColor(OPTIONS_MOUSE_POS)

            difficulty_1_button.update(screen)
            difficulty_2_button.update(screen)
            difficulty_3_button.update(screen)
            back.update(screen)
                       
            buttons = [difficulty_1_button, difficulty_2_button, difficulty_3_button]
            for i in range(3): # Icon addition
                icon = pygame.image.load(f"./Assets/difficulty{i}.png")

                button_rect = buttons[i].rect
                icon_rect = icon.get_rect(center=button_rect.center)
                screen.blit(icon, icon_rect) 


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.checkForInput(OPTIONS_MOUSE_POS):
                        running = False
                        self.main_menu()

                    if difficulty_1_button.checkForInput(OPTIONS_MOUSE_POS):
                        from main import Game

                        diffculty_modifier = 0.1
                        difficulty = 0.5
                        game = Game()
                        game.run()
                        
                    
                    if difficulty_2_button.checkForInput(OPTIONS_MOUSE_POS):
                        from main import Game

                        diffculty_modifier = 0.15
                        difficulty = 1
                        game = Game()
                        game.run()

                    if difficulty_3_button.checkForInput(OPTIONS_MOUSE_POS):
                        from main import Game

                        diffculty_modifier = 0.3
                        difficulty = 1.3
                        game = Game()
                        game.run()

            pygame.display.update()

    def store(self):
        running = True
        while running:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            screen.fill('black')

            menu_text = get_font(45).render("STORE", True, 'white')
            menu_text_rect = menu_text.get_rect(center=(640, 50))
            screen.blit(menu_text, menu_text_rect)

            # Display current score as currency at the top right corner
            currency_text = get_font(40).render(f"Currency: {self.currency}", True, 'white')
            currency_rect = currency_text.get_rect(topright=(1280 - 20, 20))
            screen.blit(currency_text, currency_rect)

          
            upgrade_buttons = {
                'ATK': Button(image=pygame.image.load("./assets/button.png"), pos=(200, 100), text_input="Upgrade ATK", 
                            font=get_font(40), base_color="#d7fcd4", hovering_color='white', width=300, height=self.button_height),
                'HP': Button(image=pygame.image.load("./assets/button.png"), pos=(200, 250), text_input="Upgrade HP", 
                            font=get_font(40), base_color="#d7fcd4", hovering_color='white', width=300, height=self.button_height),
                'DEF': Button(image=pygame.image.load("./assets/button.png"), pos=(200, 400), text_input="Upgrade DEF", 
                            font=get_font(40), base_color="#d7fcd4", hovering_color='white', width=300, height=self.button_height),
                'SPEED': Button(image=pygame.image.load("./assets/button.png"), pos=(200, 550), text_input="Upgrade SPEED", 
                                font=get_font(40), base_color="#d7fcd4", hovering_color='white', width=300, height=self.button_height)
            }

            # Draw upgrade buttons and display information
            for attribute, button in upgrade_buttons.items():
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(screen)

                # Show the current upgrade level next to each button
                upgrade_level_text = get_font(30).render(f"Level: {self.upgrades[attribute]}", True, 'white')
                upgrade_level_rect = upgrade_level_text.get_rect(center=(button.rect.centerx, button.rect.centery + 40))
                screen.blit(upgrade_level_text, upgrade_level_rect)

                # Show the cost for the next level
                next_level_cost = self.upgrades[attribute] * 4
                cost_text = get_font(30).render(f"Next level: {next_level_cost}", True, 'white')
                cost_rect = cost_text.get_rect(center=(button.rect.centerx, button.rect.centery + 70))
                screen.blit(cost_text, cost_rect)

                # Draw squares for upgrades (each tier of upgrade represented by a square)
                for i in range(1, 11):  # 10 tiers max
                    square_color = "yellow" if self.upgrades[attribute] >= i else "brown"
                    pygame.draw.rect(screen, square_color, 
                                     (button.rect.centerx + (i-1) * 40 + 200, button.rect.centery, 30, 30))

            # Back button
            back = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 650), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)
            back.changeColor(OPTIONS_MOUSE_POS)
            back.update(screen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle upgrades
                    for attribute, button in upgrade_buttons.items():
                        if button.checkForInput(OPTIONS_MOUSE_POS):
                            if self.currency >= self.upgrades[attribute] * 4 and self.upgrades[attribute] < 10:
                                # Deduct currency and increase upgrade
                                self.currency -= self.upgrades[attribute] * 4
                                self.upgrades[attribute] += 1
                                
                                self.save()


                    if back.checkForInput(OPTIONS_MOUSE_POS):
                        running = False
                        self.main_menu()

            pygame.display.update()

    def leaderboard(self):
        df = pd.read_csv(leaderboard_path)
        df_sorted = df.sort_values(by='ROOMS_CLEARED', ascending=False).head(10)

        while True:

            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            screen.fill('black')
            menu_text = get_font(45).render("LEADERBOARD", True, 'black')
            menu_text_rect = menu_text.get_rect(center=(640, 50))
            screen.blit(menu_text, menu_text_rect)

            leaderboard = df_sorted
            leaderboard_y = 150
            for i, row in leaderboard.iterrows():
                player_text = font.render(f"{i+1}. {row['NAME']} - Level {row['LEVEL']} - Rooms Cleared: {row['ROOMS_CLEARED']}", True, WHITE)
                screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, leaderboard_y + i * 30))

                        # Back button
            back = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 650), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)
            
            back.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back.checkForInput(OPTIONS_MOUSE_POS):
                        running = False
                        self.main_menu()
            pygame.display.update()
          

    def class_screen(self):


        running = True

        while running:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            screen.fill('black')
            class_text = get_font(40).render(f"Selected class: {self.current_class}", True, 'white')
            class_rect = class_text.get_rect(topright=(1280 - 20, 20))
            screen.blit(class_text, class_rect)

            menu_text = get_font(45).render("Choose a class", True, 'white')
            menu_text_rect = menu_text.get_rect(center=(640, 100))
            screen.blit(menu_text, menu_text_rect)

            BUTTON_HEIGHT = 700  # Increased button height for play screen
            class_1_button = Button(image=pygame.image.load("./assets/vertical_button.png"), pos=(320, 340), 
                                        text_input="ARCHER", font=get_font(50), base_color="#d7fcd4", hovering_color='white',width=250, inside=True, height=BUTTON_HEIGHT)
            class_2_button = Button(image=pygame.image.load("./assets/vertical_button.png"), pos=(640, 340), 
                                        text_input="WARRIOR", font=get_font(50), base_color="#d7fcd4", hovering_color='white',width=250, inside=True, height=BUTTON_HEIGHT)
            class_3_button = Button(image=pygame.image.load("./assets/vertical_button.png"), pos=(960, 340), 
                                        text_input="PALADIN", font=get_font(50), base_color="#d7fcd4", hovering_color='white',width=250, inside=True,height=BUTTON_HEIGHT)


            back = Button(image=pygame.image.load("./assets/button.png"), pos=(640, 650), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color='white', height=self.button_height)


            class_1_button.changeColor(OPTIONS_MOUSE_POS)
            class_2_button.changeColor(OPTIONS_MOUSE_POS)
            class_3_button.changeColor(OPTIONS_MOUSE_POS)
            back.changeColor(OPTIONS_MOUSE_POS)

            class_1_button.update(screen)
            class_2_button.update(screen)
            class_3_button.update(screen)
            back.update(screen)

            buttons = [class_1_button, class_2_button, class_3_button]
            for i in range(3):
                icon = pygame.image.load(f"./Assets/class{i}.png")

                button_rect = buttons[i].rect
                icon_rect = icon.get_rect(center=button_rect.center)
                screen.blit(icon, icon_rect) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if class_1_button.checkForInput(OPTIONS_MOUSE_POS):
                        self.current_class="archer"
                        self.save()
                        
                    if class_2_button.checkForInput(OPTIONS_MOUSE_POS):
                        self.current_class="warrior"
                        self.save()
                        
                    if class_3_button.checkForInput(OPTIONS_MOUSE_POS):
                        self.current_class="paladin"
                        self.save()

                    if back.checkForInput(OPTIONS_MOUSE_POS):
                        running = False
                        self.main_menu()

            pygame.display.update()


    def handle_button_action(self, button):
        if button == self.PLAY_BUTTON:
            self.play()
        elif button == self.STORE_BUTTON:

            self.store()
        elif button == self.LEADERBOARD_BUTTON:

            self.leaderboard()
        elif button == self.CLASS_BUTTON:

            self.class_screen()
        elif button == self.QUIT_BUTTON:

            pygame.quit()
            sys.exit()