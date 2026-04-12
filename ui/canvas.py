# ui/canvas.py
import pygame
import sys

from settings import *
from ui.camera import Camera
from ui.ui_elements import Ribbon

class Canvas:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(APPLICATION_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.ribbon = Ribbon()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def draw_grid(self):
        # Calculate visible grid range
        start_x = int(-self.camera.x / self.camera.zoom / GRID_SPACING) - 1
        start_y = int(-self.camera.y / self.camera.zoom / GRID_SPACING) - 1
        end_x = start_x + int(SCREEN_WIDTH / self.camera.zoom / GRID_SPACING) + 2
        end_y = start_y + int(SCREEN_HEIGHT / self.camera.zoom / GRID_SPACING) + 2
        
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                screen_x = i * GRID_SPACING * self.camera.zoom + self.camera.x
                screen_y = j * GRID_SPACING * self.camera.zoom + self.camera.y
                
                # Only draw if on screen AND below ribbon
                if -GRID_SPACING <= screen_x <= SCREEN_WIDTH + GRID_SPACING and \
                   self.ribbon.height <= screen_y <= SCREEN_HEIGHT + GRID_SPACING:
                    pygame.draw.circle(self.screen, GRID_COLOR, (int(screen_x), int(screen_y)), 2)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = self.ribbon.handle_click(event.pos)
                if clicked:
                    print(f"Clicked: {clicked}")
                    
            elif event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            
            self.camera.handle_event(event)
                    
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.ribbon.draw(self.screen)
        self.draw_grid()
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()