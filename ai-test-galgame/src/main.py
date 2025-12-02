import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_DIR = os.path.join(BASE_DIR, "resourse")
BG_PATH = os.path.join(RES_DIR, "background", "classroom.png")
CHAR_DIR = os.path.join(RES_DIR, "character", "xiaojingcha")
FONT_PATH = os.path.join(RES_DIR, "SimHei.ttf")

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Danganronpa-like Demo")
clock = pygame.time.Clock()

# Fonts
try:
    font_large = pygame.font.Font(FONT_PATH, 48)
    font_medium = pygame.font.Font(FONT_PATH, 32)
    font_small = pygame.font.Font(FONT_PATH, 24)
except Exception as e:
    print(f"Warning: Could not load custom font {FONT_PATH}. Using default.")
    font_large = pygame.font.Font(None, 48)
    font_medium = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.load_images()

    def load_images(self):
        # Load Background
        if os.path.exists(BG_PATH):
            self.images['bg'] = pygame.image.load(BG_PATH).convert()
            self.images['bg'] = pygame.transform.scale(self.images['bg'], (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            print(f"Error: Background not found at {BG_PATH}")
            self.images['bg'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.images['bg'].fill(GRAY)

        # Load Character Expressions
        # Looking at file list: sportswearing-xjc-normal-stand-angry.png, etc.
        # Simplify loading by checking specific files we need for the demo
        char_files = {
            'normal': "sportswearing-xjc-normal-stand-smile.png",
            'angry': "sportswearing-xjc-normal-stand-angry.png",
            'stony': "sportswearing-xjc-normal-stand-stonyfaced.png",
            'astonished': "sportswearing-xjc-normal-stand-astonished.png",
            'confused': "sportswearing-xjc-openmouth-stand-stonyfaced.png" # Approximation
        }

        for key, filename in char_files.items():
            path = os.path.join(CHAR_DIR, filename)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                # Scale if necessary, usually VN sprites are large
                # Let's target roughly 60-70% height
                scale_factor = 0.8
                new_size = (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))
                self.images[f'char_{key}'] = pygame.transform.smoothscale(img, new_size)
            else:
                print(f"Warning: Character image {filename} not found.")
                self.images[f'char_{key}'] = None

    def get_image(self, name):
        return self.images.get(name)

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_input(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class DialogueState(GameState):
    def __init__(self, game, script):
        super().__init__(game)
        self.script = script
        self.current_line_index = 0
        self.finished = False
        self.show_text = True

        # Dialogue box properties
        self.box_height = 200
        self.box_rect = pygame.Rect(0, SCREEN_HEIGHT - self.box_height, SCREEN_WIDTH, self.box_height)
        self.box_color = (0, 0, 0, 180) # Semi-transparent black

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.advance_script()

    def advance_script(self):
        current_line = self.script[self.current_line_index]
        if 'next' in current_line:
             # Logic to handle branching or simple next step,
             # but for linear script we just increment
             pass

        self.current_line_index += 1
        if self.current_line_index >= len(self.script):
            self.finished = True
            # In a real engine, we would pop state or trigger next event
            # For this demo, we might transition to choices
            self.game.handle_end_of_dialogue()
        else:
            # Check if new line triggers a choice
            if 'choices' in self.script[self.current_line_index]:
                self.game.change_state(ChoiceState(self.game, self.script[self.current_line_index]))

    def draw(self, screen):
        # Draw Background
        bg = self.game.resources.get_image('bg')
        screen.blit(bg, (0, 0))

        if self.finished:
            return

        current_line = self.script[self.current_line_index]

        # Draw Character
        char_key = f"char_{current_line.get('expression', 'normal')}"
        char_img = self.game.resources.get_image(char_key)
        if char_img:
            # Center the character
            x = (SCREEN_WIDTH - char_img.get_width()) // 2
            y = SCREEN_HEIGHT - char_img.get_height() # Bottom aligned
            # Adjust y if needed to be behind text box or not
            # Usually sprite is behind text box
            screen.blit(char_img, (x, y + 50)) # +50 to push it down a bit

        # Draw Text Box
        s = pygame.Surface((self.box_rect.width, self.box_rect.height))
        s.set_alpha(200)
        s.fill(BLACK)
        screen.blit(s, (self.box_rect.x, self.box_rect.y))

        # Draw Name
        name = current_line.get('name', '???')
        name_surf = font_medium.render(name, True, BLUE)
        screen.blit(name_surf, (self.box_rect.x + 40, self.box_rect.y + 20))

        # Draw Text
        text = current_line.get('text', '')
        # Simple word wrap or just display
        text_surf = font_medium.render(text, True, WHITE)
        screen.blit(text_surf, (self.box_rect.x + 40, self.box_rect.y + 70))

        # Hint
        hint = font_small.render("Click or Press Space to Continue", True, GRAY)
        screen.blit(hint, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 40))

class ChoiceState(GameState):
    def __init__(self, game, line_data):
        super().__init__(game)
        self.line_data = line_data
        self.choices = line_data['choices'] # List of dicts {'text': '...', 'result_index': int}
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        # Create rects for buttons
        start_y = 200
        for i, choice in enumerate(self.choices):
            rect = pygame.Rect(200, start_y + i * 100, SCREEN_WIDTH - 400, 60)
            self.buttons.append((rect, choice))

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for rect, choice in self.buttons:
                if rect.collidepoint(mouse_pos):
                    # Choice selected
                    print(f"Selected: {choice['text']}")
                    # Assume linear progression for demo: jump to 'next_index' or just next + 1
                    # Here we might need a jump mechanism
                    if 'jump_to' in choice:
                        self.game.current_script_index = choice['jump_to']
                        self.game.change_state(DialogueState(self.game, self.game.full_script[choice['jump_to']:]))
                    elif 'outcome_text' in choice:
                         # Show outcome then end
                         pass

    def draw(self, screen):
        # Draw Background & Character (Reuse last state if possible, but simpler to redraw)
        # For simplicity, just redraw background
        bg = self.game.resources.get_image('bg')
        screen.blit(bg, (0, 0))

        # Draw buttons
        for rect, choice in self.buttons:
            pygame.draw.rect(screen, (0, 100, 200), rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            text_surf = font_medium.render(choice['text'], True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

class Game:
    def __init__(self):
        self.resources = ResourceManager()
        self.running = True
        self.state = None

        # Script Definition
        # This is a linear list, but we can jump around
        self.full_script = [
            {'name': '小警察', 'text': '等等！那个证词有点奇怪！', 'expression': 'angry'},
            {'name': '小警察', 'text': '仔细看看现场的照片...', 'expression': 'stony'},
            {'name': '小警察', 'text': '凶手不可能从那个窗户逃走！', 'expression': 'normal'},
            {'name': '小警察', 'text': '因为...', 'expression': 'confused'},
             # Choice Event
            {'choices': [
                {'text': '窗户是锁着的', 'jump_to': 5},
                {'text': '窗户太高了', 'jump_to': 7}
            ]},
            # Index 5 (Correct)
            {'name': '小警察', 'text': '没错！窗户是从里面锁上的！', 'expression': 'astonished'},
            {'name': '小警察', 'text': '这是一个密室杀人案！', 'expression': 'angry', 'next': 'end'},
            # Index 7 (Wrong)
            {'name': '小警察', 'text': '不，高度不是问题，有梯子的话...', 'expression': 'stony'},
             {'name': '小警察', 'text': '再想一想！', 'expression': 'angry', 'next': 'retry'},
        ]

        self.current_script_index = 0
        self.state = DialogueState(self, self.full_script)

    def change_state(self, new_state):
        self.state = new_state

    def handle_end_of_dialogue(self):
        # Determine what to do based on context.
        # In this simple demo, if script ends, we exit or restart.
        # But wait, DialogueState logic advances index.
        # If we hit end of list, we exit.
        print("End of demo.")
        self.running = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.state.handle_input(event)

            self.state.update()
            self.state.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
