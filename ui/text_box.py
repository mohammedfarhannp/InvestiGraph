import pygame
from settings import *

class TextBox:
    def __init__(self, x, y, width, height, text="", placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.placeholder = placeholder
        self.active = False
        self.cursor_pos = len(text)
        self.font = pygame.font.SysFont("Arial", 14)
        self.color_bg = (60, 60, 65)
        self.color_border = (80, 80, 85)
        self.color_active = (100, 100, 255)
        self.color_text = (220, 220, 220)
        self.color_placeholder = (120, 120, 120)
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, self.color_bg, self.rect)
        
        # Border
        border_color = self.color_active if self.active else self.color_border
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # Text with cursor position handling
        display_text = self.text if self.text else self.placeholder
        color = self.color_text if self.text else self.color_placeholder
        
        # Handle text scrolling if too long
        text_surface = self.font.render(display_text, True, color)
        
        # Calculate visible portion
        text_width = text_surface.get_width()
        max_width = self.rect.width - 10
        scroll_offset = 0
        
        if text_width > max_width and self.active:
            # Scroll to show cursor position
            cursor_x = self.font.size(self.text[:self.cursor_pos])[0]
            if cursor_x > scroll_offset + max_width - 20:
                scroll_offset = cursor_x - max_width + 20
            elif cursor_x < scroll_offset:
                scroll_offset = cursor_x
        
        # Create clipped surface for text
        if scroll_offset > 0:
            text_surface = text_surface.subsurface((scroll_offset, 0, min(max_width, text_width - scroll_offset), text_surface.get_height()))
        
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 8))
        
        # Cursor blink if active
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            if self.cursor_visible:
                cursor_x = self.rect.x + 5 + self.font.size(self.text[:self.cursor_pos])[0] - scroll_offset
                if 5 <= cursor_x - self.rect.x <= self.rect.width - 5:
                    pygame.draw.line(screen, (255, 255, 255), 
                                   (cursor_x, self.rect.y + 5), 
                                   (cursor_x, self.rect.y + self.rect.height - 5), 2)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                # Set cursor position based on click
                click_x = event.pos[0] - self.rect.x - 5
                if click_x > 0:
                    # Find closest character
                    for i in range(len(self.text) + 1):
                        char_width = self.font.size(self.text[:i])[0]
                        if char_width >= click_x:
                            self.cursor_pos = i
                            break
                    else:
                        self.cursor_pos = len(self.text)
                else:
                    self.cursor_pos = 0
                self.cursor_visible = True
                self.cursor_timer = 0
            return self.active and not was_active
            
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            elif event.key == pygame.K_a and (event.mod & pygame.KMOD_CTRL):
                # Ctrl+A to select all
                # For now, just select all text (cursor to end, but we'd need selection highlight)
                pass
            else:
                if event.unicode and len(self.text) < 100:
                    self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
            return True
        return False