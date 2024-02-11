import pygame

COLOR_INACTIVE = pygame.Color('white')
COLOR_ACTIVE = pygame.Color('white')

class InputBox():
    def __init__(self, x, y, w, h, fontSize,  text=''):
        self.font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", fontSize)
        self.rect = pygame.Rect(x,y,w,h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        
        self.max_length = False
        self.max_length_warning = self.font.render("Max Length reached", True, pygame.Color('red'))

    def handle_event(self, event):
        if (len(self.text) >= 4):
            self.max_length = True
        else: 
            self.max_length = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # if within bounding box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if not self.max_length:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def get_text_value(self):
        return self.text

    def draw(self, display: pygame.Surface):
        display.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(display, self.color, self.rect, 2)