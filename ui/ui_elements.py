# ui/ui_elements.py
import pygame
from settings import *

# Top Ribbon
class Ribbon:
    def __init__(self):
        self.height = 40
        self.color = (45, 45, 50)
        self.border_color = (80, 80, 85)
        
        # Buttons (x position, text)
        self.buttons = [
            {"x": 10, "text": "File"},
            {"x": 70, "text": "Add Node"},
            {"x": 150, "text": "Transforms"},
            {"x": 240, "text": "Help"},
        ]
        
        self.font = pygame.font.SysFont("Arial", 14)
        
    def draw(self, screen):
        # Create solid opaque surface
        ribbon_surface = pygame.Surface((SCREEN_WIDTH, self.height))
        ribbon_surface.fill(self.color)
        screen.blit(ribbon_surface, (0, 0))
        
        # Draw bottom border
        pygame.draw.line(screen, self.border_color, (0, self.height), (SCREEN_WIDTH, self.height), 2)
        
        # Draw buttons
        for btn in self.buttons:
            text_surface = self.font.render(btn["text"], True, (220, 220, 220))
            screen.blit(text_surface, (btn["x"], 12))
            
    def handle_click(self, pos):
        # Return button text if clicked, else None
        x, y = pos
        if y > self.height:
            return None
            
        for btn in self.buttons:
            text_width = self.font.size(btn["text"])[0]
            if btn["x"] <= x <= btn["x"] + text_width + 20:
                return btn["text"]
        return None