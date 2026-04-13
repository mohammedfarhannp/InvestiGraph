import pygame
from settings import *

class PropertiesPanel:
    def __init__(self):
        self.width = 250
        self.x = SCREEN_WIDTH - self.width
        self.y = 40  # Below ribbon
        self.height = SCREEN_HEIGHT - self.y
        self.visible = False
        self.current_node = None
        
        self.font = pygame.font.SysFont("Arial", 14)
        self.font_small = pygame.font.SysFont("Arial", 12)
        self.font_input = pygame.font.SysFont("Arial", 14)
        
        self.active_field = None  # For text editing
        self.edit_text = ""
        
    def set_node(self, node):
        self.current_node = node
        self.visible = node is not None
        
    def draw(self, screen):
        if not self.visible or not self.current_node:
            return
            
        # Panel background
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (45, 45, 50), panel_rect)
        pygame.draw.rect(screen, (80, 80, 85), panel_rect, 2)
        
        # Title (Node Type)
        y_offset = self.y + 15
        title = self.font.render(self.current_node.node_type, True, (255, 255, 255))
        screen.blit(title, (self.x + 10, y_offset))
        
        # Label field
        y_offset += 35
        label_text = self.font.render("Label:", True, (200, 200, 200))
        screen.blit(label_text, (self.x + 10, y_offset))
        
        # Label value (editable)
        label_value = self.current_node.label
        label_surface = self.font.render(label_value, True, (220, 220, 220))
        screen.blit(label_surface, (self.x + 70, y_offset))
        
        # Edit indicator (small pencil)
        edit_rect = pygame.Rect(self.x + self.width - 30, y_offset - 5, 20, 20)
        pygame.draw.rect(screen, (60, 60, 65), edit_rect)
        edit_text = self.font_small.render("✎", True, (150, 150, 150))
        screen.blit(edit_text, (self.x + self.width - 25, y_offset - 2))
        
        # Properties section
        y_offset += 30
        props_title = self.font.render("Properties:", True, (200, 200, 200))
        screen.blit(props_title, (self.x + 10, y_offset))
        
        y_offset += 25
        if hasattr(self.current_node, 'properties'):
            for key, value in self.current_node.properties.items():
                if value is not None:
                    prop_text = f"{key}: {value}"
                    prop_surface = self.font_small.render(prop_text, True, (180, 180, 180))
                    screen.blit(prop_surface, (self.x + 15, y_offset))
                    y_offset += 20
                else:
                    prop_text = f"{key}: —"
                    prop_surface = self.font_small.render(prop_text, True, (120, 120, 120))
                    screen.blit(prop_surface, (self.x + 15, y_offset))
                    y_offset += 20
        
        # Notes section
        y_offset += 15
        notes_title = self.font.render("Notes:", True, (200, 200, 200))
        screen.blit(notes_title, (self.x + 10, y_offset))
        
        y_offset += 25
        notes_text = "Click to add notes..."
        notes_surface = self.font_small.render(notes_text, True, (140, 140, 140))
        screen.blit(notes_surface, (self.x + 15, y_offset))
        
    def handle_click(self, pos):
        if not self.visible:
            return None
            
        x, y = pos
        # Check if edit button clicked
        edit_rect = pygame.Rect(self.x + self.width - 30, self.y + 45, 20, 20)
        if edit_rect.collidepoint(x, y):
            return "edit_label"
            
        return None
    
    def update_label(self, new_label):
        if self.current_node:
            self.current_node.label = new_label