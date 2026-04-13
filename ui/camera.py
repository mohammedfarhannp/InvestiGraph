# ui/camera.py
import pygame

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.width = width
        self.height = height
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def handle_event(self, event, allow_drag=True):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and allow_drag:  # Left mouse button
                self.dragging = True
                self.drag_start_x = event.pos[0]
                self.drag_start_y = event.pos[1]
            elif event.button == 4:  # Scroll up
                self.zoom = min(self.zoom * 1.1, 3.0)
            elif event.button == 5:  # Scroll down
                self.zoom = max(self.zoom / 1.1, 0.3)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.drag_start_x
                dy = event.pos[1] - self.drag_start_y
                self.x += dx
                self.y += dy
                self.drag_start_x = event.pos[0]
                self.drag_start_y = event.pos[1]
    
    def apply(self, pos):
        # Convert screen pos to world pos
        x = (pos[0] - self.x) / self.zoom
        y = (pos[1] - self.y) / self.zoom
        return (x, y)
    
    def to_screen(self, pos):
        # Convert world pos to screen pos
        x = pos[0] * self.zoom + self.x
        y = pos[1] * self.zoom + self.y
        return (x, y)