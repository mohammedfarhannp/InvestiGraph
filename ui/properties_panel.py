# ui/properties_panel.py
import pygame
from settings import *
from ui.text_box import TextBox

class PropertiesPanel:
    def __init__(self):
        self.width = 280
        self.x = SCREEN_WIDTH - self.width
        self.y = 40
        self.height = SCREEN_HEIGHT - self.y
        self.visible = False
        self.current_node = None
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.font = pygame.font.SysFont("Arial", 14)
        self.font_small = pygame.font.SysFont("Arial", 12)
        
        self.label_box = None
        self.property_boxes = {}
        self.notes_box = None
        
    def set_node(self, node):
        self.current_node = node
        self.visible = node is not None
        
        if node:
            # Label text box (right-aligned)
            self.label_box = TextBox(self.x + 80, self.y + 35, 180, 28, node.label)
            
            # Property text boxes
            self.property_boxes = {}
            y_offset = self.y + 100
            
            # Handle gender separately (read-only, no text box)
            if hasattr(node, 'gender'):
                self.gender_value = node.gender
            else:
                self.gender_value = None
            
            for key, value in node.properties.items():
                # Skip non-editable fields
                if key in ["gender", "name"]:
                    continue
                # Create text box for editable properties
                box = TextBox(self.x + 100, y_offset, 160, 25, 
                             str(value) if value else "", "")
                self.property_boxes[key] = box
                y_offset += 32
            
            # Notes box
            self.notes_box = TextBox(self.x + 15, self.y + 280, 250, 60, "", "Add notes...", multiline=True)
            self.notes_box.multiline = True  # Will handle later
    
    def draw(self, screen):
        if not self.visible or not self.current_node:
            return
        
        # Panel background
        pygame.draw.rect(screen, (45, 45, 50), self.rect)
        pygame.draw.rect(screen, (80, 80, 85), self.rect, 2)
        
        # Title
        title = self.font.render(self.current_node.node_type, True, (255, 255, 255))
        screen.blit(title, (self.x + 10, self.y + 10))
        
        # Label row
        label_text = self.font.render("Label:", True, (200, 200, 200))
        screen.blit(label_text, (self.x + 10, self.y + 40))
        if self.label_box:
            self.label_box.draw(screen)
        
        # Properties section title
        y_offset = self.y + 85
        props_title = self.font.render("Properties:", True, (200, 200, 200))
        screen.blit(props_title, (self.x + 10, y_offset))
        y_offset += 30
        
        # Gender (read-only)
        if self.gender_value:
            gender_y = self.y + 175
            gender_text = self.font.render(f"Gender: {self.gender_value}", True, (180, 180, 180))
            screen.blit(gender_text, (self.x + 15, gender_y))
        
        # Property text boxes
        for key, box in self.property_boxes.items():
            # Draw label
            key_display = key.replace('_', ' ').title()
            key_text = self.font_small.render(f"{key_display}:", True, (180, 180, 180))
            screen.blit(key_text, (self.x + 15, box.rect.y + 6))
            # Draw text box
            box.draw(screen)
        
        # Notes section
        notes_y = self.y + 250
        notes_title = self.font.render("Notes:", True, (200, 200, 200))
        screen.blit(notes_title, (self.x + 10, notes_y))
        
        if self.notes_box:
            self.notes_box.rect.y = notes_y + 25
            self.notes_box.draw(screen)
    
    def handle_click(self, pos):
        if not self.visible:
            return None
        
        if self.label_box:
            self.label_box.active = False
        for box in self.property_boxes.values():
            box.active = False
        if self.notes_box:
            self.notes_box.active = False
        
        if self.label_box and self.label_box.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos)):
            return "label_edit"
        
        for box in self.property_boxes.values():
            if box.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos)):
                return "property_edit"
        
        if self.notes_box and self.notes_box.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos)):
            return "notes_edit"
        
        return None
    
    def handle_keyboard(self, event):
        if not self.visible:
            return
        
        if self.label_box and self.label_box.active:
            self.label_box.handle_event(event)
            self.current_node.label = self.label_box.text
        
        for key, box in self.property_boxes.items():
            if box.active:
                box.handle_event(event)
                self.current_node.properties[key] = box.text
        
        if self.notes_box and self.notes_box.active:
            self.notes_box.handle_event(event)