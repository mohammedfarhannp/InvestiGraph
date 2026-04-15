# core/node.py
import pygame
from settings import *

class Node:
    def __init__(self, node_id, node_type, label, x, y, color=None, icon_path=None):
        self.id = node_id
        self.node_type = node_type
        self.label = label
        self.x = x
        self.y = y
        self.radius = DEFAULT_NODE_RADIUS
        self.color = color if color else (150, 150, 150)  # Default gray
        self.selected = False
        
        self.notes = ""
        
        self.icon = None
        if icon_path:
            try:
                self.icon = pygame.image.load(icon_path).convert_alpha()
                self.icon = pygame.transform.scale(self.icon, (24, 24))
            except:
                print(f"Could not load icon: {icon_path}")
        
    def draw(self, screen, camera):
        # Convert world coordinates to screen
        screen_x, screen_y = camera.to_screen((self.x, self.y))
        
        # Draw circle
        border_color = (255, 255, 0) if self.selected else (0, 0, 0)
        border_width = 3 if self.selected else 2
        
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.radius)
        pygame.draw.circle(screen, border_color, (int(screen_x), int(screen_y)), self.radius, border_width)
        
        if self.icon:
            icon_rect = self.icon.get_rect(center=(int(screen_x), int(screen_y)))
            screen.blit(self.icon, icon_rect)
        
        # Draw label below the node
        font = pygame.font.SysFont("Arial", DEFAULT_FONT_SIZE)
        text_surface = font.render(self.label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(screen_x), int(screen_y + self.radius + 10)))
        screen.blit(text_surface, text_rect)
        
    def get_rect(self, camera):
        # Return pygame.Rect for click detection (screen coordinates)
        screen_x, screen_y = camera.to_screen((self.x, self.y))
        return pygame.Rect(screen_x - self.radius, screen_y - self.radius, self.radius * 2, self.radius * 2)
    
    def contains_point(self, screen_pos, camera):
        # Check if a screen point is inside the node
        rect = self.get_rect(camera)
        return rect.collidepoint(screen_pos)
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.node_type,
            "label": self.label,
            "x": self.x,
            "y": self.y,
            "color": self.color
        }