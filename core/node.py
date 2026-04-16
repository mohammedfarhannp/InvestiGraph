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
        
        # Scale radius based on zoom
        scaled_radius = int(self.radius * camera.zoom)
        if scaled_radius < 5:  # Minimum size to avoid disappearing
            scaled_radius = 5
        
        # Scale border width
        border_width = max(1, int(3 if self.selected else 2))
        
        # Draw circle
        border_color = (255, 255, 0) if self.selected else (0, 0, 0)
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), scaled_radius)
        pygame.draw.circle(screen, border_color, (int(screen_x), int(screen_y)), scaled_radius, border_width)
        
        # Draw icon (scale with zoom)
        if self.icon:
            icon_size = int(24 * camera.zoom)
            if icon_size > 8:  # Only draw if large enough
                scaled_icon = pygame.transform.scale(self.icon, (icon_size, icon_size))
                icon_rect = scaled_icon.get_rect(center=(int(screen_x), int(screen_y)))
                screen.blit(scaled_icon, icon_rect)
        
        # Draw label (scale font size with zoom)
        font_size = max(8, int(DEFAULT_FONT_SIZE * camera.zoom))
        font = pygame.font.SysFont("Arial", font_size)
        text_surface = font.render(self.label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(screen_x), int(screen_y + scaled_radius + 5)))
        screen.blit(text_surface, text_rect)
        
    def get_rect(self, camera):
        screen_x, screen_y = camera.to_screen((self.x, self.y))
        scaled_radius = int(self.radius * camera.zoom)
        return pygame.Rect(screen_x - scaled_radius, screen_y - scaled_radius, 
                          scaled_radius * 2, scaled_radius * 2)

    def contains_point(self, screen_pos, camera):
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