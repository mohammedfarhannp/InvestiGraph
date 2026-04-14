# core/edge.py
import pygame
import math
from settings import *

class Edge:
    def __init__(self, edge_id, source_node, target_node, label="Relationship"):
        self.id = edge_id
        self.source = source_node
        self.target = target_node
        self.label = label
        self.selected = False
        
    def draw(self, screen, camera):
        # Get screen positions
        start = camera.to_screen((self.source.x, self.source.y))
        end = camera.to_screen((self.target.x, self.target.y))
        
        # Draw line
        color = (255, 255, 0) if self.selected else (200, 200, 200)
        width = 3 if self.selected else 2
        pygame.draw.line(screen, color, start, end, width)
        
        # Draw arrowhead at target
        self.draw_arrowhead(screen, start, end, color)
        
        # Draw label at midpoint
        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        font = pygame.font.SysFont("Arial", 12)
        label_surface = font.render(self.label, True, (220, 220, 220))
        label_rect = label_surface.get_rect(center=(mid_x, mid_y - 10))
        
        # Background for label
        pygame.draw.rect(screen, (45, 45, 50), label_rect.inflate(6, 4))
        pygame.draw.rect(screen, (80, 80, 85), label_rect.inflate(6, 4), 1)
        screen.blit(label_surface, label_rect)
        
    def draw_arrowhead(self, screen, start, end, color):
        # Calculate angle
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        
        # Arrowhead points
        arrow_size = 10
        left_angle = angle + math.radians(150)
        right_angle = angle - math.radians(150)
        
        left_point = (end[0] + arrow_size * math.cos(left_angle),
                     end[1] + arrow_size * math.sin(left_angle))
        right_point = (end[0] + arrow_size * math.cos(right_angle),
                      end[1] + arrow_size * math.sin(right_angle))
        
        pygame.draw.polygon(screen, color, [end, left_point, right_point])
        
    def contains_point(self, screen_pos, camera, threshold=5):
        """Check if click is near the edge line"""
        start = camera.to_screen((self.source.x, self.source.y))
        end = camera.to_screen((self.target.x, self.target.y))
        
        # Calculate distance from point to line segment
        x1, y1 = start
        x2, y2 = end
        px, py = screen_pos
        
        line_len = math.hypot(x2 - x1, y2 - y1)
        if line_len == 0:
            return False
            
        t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_len ** 2)
        t = max(0, min(1, t))
        
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        
        dist = math.hypot(px - proj_x, py - proj_y)
        return dist <= threshold
        
    def to_dict(self):
        return {
            "id": self.id,
            "source_id": self.source.id,
            "target_id": self.target.id,
            "label": self.label
        }