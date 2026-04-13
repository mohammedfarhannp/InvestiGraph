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

        self.add_node_dropdown = Dropdown(70, 40, ["Person (Male)", "Person (Female)", "Organization", "Email", "Phone"])
        self.active_dropdown = None
        self.font = pygame.font.SysFont("Arial", 14)
            
    def handle_click(self, pos):
        # Return button text if clicked, else None
        x, y = pos
        if y > self.height:
            return None
        
        # Check if dropdown is active
        if self.active_dropdown:
            result = self.active_dropdown.handle_click(pos)
            if result:
                self.active_dropdown = None
                return result
            self.active_dropdown = None
        
            
        for btn in self.buttons:
            text_width = self.font.size(btn["text"])[0]
            if btn["x"] <= x <= btn["x"] + text_width + 20:
                if btn["text"] == "Add Node":
                    self.active_dropdown = self.add_node_dropdown
                    self.add_node_dropdown.visible = True
                    return "dropdown_opened"
                return btn["text"]
        return None
    
    def draw(self, screen):
        # Draw ribbon background and buttons only
        ribbon_surface = pygame.Surface((SCREEN_WIDTH, self.height))
        ribbon_surface.fill(self.color)
        screen.blit(ribbon_surface, (0, 0))
        pygame.draw.line(screen, self.border_color, (0, self.height), (SCREEN_WIDTH, self.height), 2)
        
        for btn in self.buttons:
            text_surface = self.font.render(btn["text"], True, (220, 220, 220))
            screen.blit(text_surface, (btn["x"], 12))

    def draw_dropdowns(self, screen):
        # Draw dropdown on top
        if self.active_dropdown:
            self.active_dropdown.draw(screen)


# Dropdown class
class Dropdown:
    def __init__(self, x, y, options):
        self.x = x
        self.y = y
        self.options = options
        self.visible = False
        self.selected = None
        self.font = pygame.font.SysFont("Arial", 14)
        self.item_height = 30
        self.width = 150
        
    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw dropdown background
        dropdown_rect = pygame.Rect(self.x, self.y, self.width, len(self.options) * self.item_height)
        pygame.draw.rect(screen, (55, 55, 60), dropdown_rect)
        pygame.draw.rect(screen, (80, 80, 85), dropdown_rect, 2)
        
        # Draw options
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, (220, 220, 220))
            text_y = self.y + i * self.item_height + 8
            screen.blit(text_surface, (self.x + 10, text_y))
            
    def handle_click(self, pos):
        if not self.visible:
            return None
            
        x, y = pos
        if self.x <= x <= self.x + self.width:
            for i in range(len(self.options)):
                item_y = self.y + i * self.item_height
                if item_y <= y <= item_y + self.item_height:
                    self.visible = False
                    return self.options[i]
        return None