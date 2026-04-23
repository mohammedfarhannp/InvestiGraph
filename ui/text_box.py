# ui/text_box.py - Enhanced with multi-line support

import pygame
from settings import *

class TextBox:
    def __init__(self, x, y, width, height, text="", placeholder="", multiline=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.placeholder = placeholder
        self.active = False
        self.multiline = multiline
        self.font = pygame.font.SysFont("Arial", 14)
        self.color_bg = IN_THE_DARK
        self.color_border = WATER_OUZEL
        self.color_active = BLUE_GENIE
        self.color_text = GAINSBORO
        self.color_placeholder = WESTCHESTER_GRAY
        self.color_selection = CASTING_SEA
        
        self.cursor_visible = True
        self.cursor_timer = 0
        self.scroll_offset = 0
        
        # For single line
        if not multiline:
            self.text = text
            self.cursor_pos = len(text)
            self.selection_start = None
            self.selection_end = None
            self.dragging = False
        else:
            # For multi-line: text is list of lines
            self.lines = text.split('\n') if text else [""]
            self.cursor_line = 0
            self.cursor_col = len(self.lines[0])
            self.selection_start_line = None
            self.selection_start_col = None
            self.selection_end_line = None
            self.selection_end_col = None
            self.dragging = False
            self.line_height = self.font.get_height() + 4
            self.visible_lines = height // self.line_height
        
    def get_text(self):
        if not self.multiline:
            return self.text
        else:
            return '\n'.join(self.lines)
    
    def set_text(self, text):
        if not self.multiline:
            self.text = text
            self.cursor_pos = len(text)
        else:
            self.lines = text.split('\n') if text else [""]
            self.cursor_line = len(self.lines) - 1
            self.cursor_col = len(self.lines[self.cursor_line])
    
    def draw_singleline(self, screen):
        # Background
        pygame.draw.rect(screen, self.color_bg, self.rect)
        
        # Border
        border_color = self.color_active if self.active else self.color_border
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        # Text
        display_text = self.text if self.text else self.placeholder
        color = self.color_text if self.text else self.color_placeholder
        text_surface = self.font.render(display_text, True, color)
        
        # Handle scrolling
        max_width = self.rect.width - 10
        text_width = text_surface.get_width()
        scroll_offset = 0
        
        if text_width > max_width and self.active:
            cursor_x = self.font.size(self.text[:self.cursor_pos])[0]
            if cursor_x > scroll_offset + max_width - 20:
                scroll_offset = cursor_x - max_width + 20
            elif cursor_x < scroll_offset:
                scroll_offset = cursor_x
        
        if scroll_offset > 0:
            text_surface = text_surface.subsurface((scroll_offset, 0, min(max_width, text_width - scroll_offset), text_surface.get_height()))
        
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 8))
        
        # Cursor
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + self.font.size(self.text[:self.cursor_pos])[0] - scroll_offset
            if 5 <= cursor_x - self.rect.x <= self.rect.width - 5:
                pygame.draw.line(screen, WHITE, 
                               (cursor_x, self.rect.y + 5), 
                               (cursor_x, self.rect.y + self.rect.height - 5), 2)
    
    def draw_multiline(self, screen):
        # Background
        pygame.draw.rect(screen, self.color_bg, self.rect)
        
        # Border
        border_color = self.color_active if self.active else self.color_border
        pygame.draw.rect(screen, border_color, self.rect, 2)
        
        if not self.lines or (len(self.lines) == 1 and not self.lines[0] and not self.active):
            # Show placeholder
            text_surface = self.font.render(self.placeholder, True, self.color_placeholder)
            screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 8))
            return
        
        # Calculate which lines are visible
        start_line = self.scroll_offset
        end_line = min(len(self.lines), start_line + self.visible_lines)
        
        y_offset = self.rect.y + 5
        for i in range(start_line, end_line):
            line = self.lines[i]
            x_offset = self.rect.x + 5
            
            # Draw selection highlight
            if self.active and self.selection_start_line is not None:
                # Check if this line is selected
                sel_start_line = min(self.selection_start_line, self.selection_end_line)
                sel_end_line = max(self.selection_start_line, self.selection_end_line)
                sel_start_col = self.selection_start_col if self.selection_start_line == sel_start_line else 0
                sel_end_col = self.selection_end_col if self.selection_end_line == sel_end_line else len(line)
                
                if sel_start_line <= i <= sel_end_line:
                    start_col = sel_start_col if i == sel_start_line else 0
                    end_col = sel_end_col if i == sel_end_line else len(line)
                    
                    if start_col < end_col:
                        # Get rect of selected text
                        prefix = line[:start_col]
                        selected = line[start_col:end_col]
                        prefix_width = self.font.size(prefix)[0]
                        selected_width = self.font.size(selected)[0]
                        
                        sel_rect = pygame.Rect(x_offset + prefix_width, y_offset, selected_width, self.line_height - 4)
                        pygame.draw.rect(screen, self.color_selection, sel_rect)
            
            # Draw text
            text_surface = self.font.render(line, True, self.color_text)
            screen.blit(text_surface, (x_offset, y_offset))
            
            # Draw cursor on this line if active
            if self.active and self.cursor_visible and self.cursor_line == i:
                cursor_x = x_offset + self.font.size(line[:self.cursor_col])[0]
                pygame.draw.line(screen, WHITE, 
                               (cursor_x, y_offset), 
                               (cursor_x, y_offset + self.line_height - 4), 2)
            
            y_offset += self.line_height
    
    def draw(self, screen):
        if not self.multiline:
            self.draw_singleline(screen)
        else:
            self.draw_multiline(screen)
    
    def handle_singleline_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                # Set cursor position based on click
                click_x = event.pos[0] - self.rect.x - 5
                if click_x > 0:
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
                self.selection_start = None
            return self.active and not was_active
            
        elif event.type == pygame.MOUSEMOTION and self.active:
            # Drag to select
            if event.buttons[0]:
                click_x = event.pos[0] - self.rect.x - 5
                new_pos = 0
                if click_x > 0:
                    for i in range(len(self.text) + 1):
                        char_width = self.font.size(self.text[:i])[0]
                        if char_width >= click_x:
                            new_pos = i
                            break
                    else:
                        new_pos = len(self.text)
                else:
                    new_pos = 0
                
                if self.selection_start is None:
                    self.selection_start = self.cursor_pos
                self.cursor_pos = new_pos
                self.selection_end = new_pos
            else:
                self.dragging = False
            
        elif event.type == pygame.KEYDOWN and self.active:
            # Handle selection deletion
            if self.selection_start is not None and self.selection_end is not None:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    start = min(self.selection_start, self.selection_end)
                    end = max(self.selection_start, self.selection_end)
                    self.text = self.text[:start] + self.text[end:]
                    self.cursor_pos = start
                    self.selection_start = None
                    self.selection_end = None
                    return True
            
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
                self.selection_start = None
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                self.selection_start = None
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
            else:
                if event.unicode and len(self.text) < 100:
                    self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
            return True
        return False
    
    def handle_multiline_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                # Calculate which line was clicked
                click_y = event.pos[1] - self.rect.y - 5
                line_index = self.scroll_offset + (click_y // self.line_height)
                if 0 <= line_index < len(self.lines):
                    self.cursor_line = line_index
                    # Calculate column
                    click_x = event.pos[0] - self.rect.x - 5
                    line = self.lines[self.cursor_line]
                    if click_x > 0:
                        for i in range(len(line) + 1):
                            char_width = self.font.size(line[:i])[0]
                            if char_width >= click_x:
                                self.cursor_col = i
                                break
                        else:
                            self.cursor_col = len(line)
                    else:
                        self.cursor_col = 0
                else:
                    # Click below last line, go to end
                    self.cursor_line = len(self.lines) - 1
                    self.cursor_col = len(self.lines[self.cursor_line])
                
                self.cursor_visible = True
                self.cursor_timer = 0
                self.selection_start_line = None
            return self.active and not was_active
            
        elif event.type == pygame.MOUSEMOTION and self.active:
            if event.buttons[0]:
                click_y = event.pos[1] - self.rect.y - 5
                line_index = self.scroll_offset + (click_y // self.line_height)
                if 0 <= line_index < len(self.lines):
                    if self.selection_start_line is None:
                        self.selection_start_line = self.cursor_line
                        self.selection_start_col = self.cursor_col
                    
                    self.cursor_line = line_index
                    click_x = event.pos[0] - self.rect.x - 5
                    line = self.lines[self.cursor_line]
                    if click_x > 0:
                        for i in range(len(line) + 1):
                            char_width = self.font.size(line[:i])[0]
                            if char_width >= click_x:
                                self.cursor_col = i
                                break
                        else:
                            self.cursor_col = len(line)
                    else:
                        self.cursor_col = 0
                    
                    self.selection_end_line = self.cursor_line
                    self.selection_end_col = self.cursor_col
            else:
                self.dragging = False
            
        elif event.type == pygame.KEYDOWN and self.active:
            # Handle selection deletion
            if self.selection_start_line is not None:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    # Remove selected text across lines
                    start_line = min(self.selection_start_line, self.selection_end_line)
                    end_line = max(self.selection_start_line, self.selection_end_line)
                    start_col = self.selection_start_col if self.selection_start_line == start_line else 0
                    end_col = self.selection_end_col if self.selection_end_line == end_line else len(self.lines[end_line])
                    
                    if start_line == end_line:
                        line = self.lines[start_line]
                        self.lines[start_line] = line[:start_col] + line[end_col:]
                    else:
                        # Keep first part of first line
                        first_line = self.lines[start_line][:start_col]
                        # Keep last part of last line
                        last_line = self.lines[end_line][end_col:]
                        # Replace with combined
                        self.lines = self.lines[:start_line] + [first_line + last_line] + self.lines[end_line+1:]
                    
                    self.cursor_line = start_line
                    self.cursor_col = start_col
                    self.selection_start_line = None
                    return True
            
            if event.key == pygame.K_RETURN:
                # Insert new line
                current_line = self.lines[self.cursor_line]
                self.lines[self.cursor_line] = current_line[:self.cursor_col]
                self.lines.insert(self.cursor_line + 1, current_line[self.cursor_col:])
                self.cursor_line += 1
                self.cursor_col = 0
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_col > 0:
                    line = self.lines[self.cursor_line]
                    self.lines[self.cursor_line] = line[:self.cursor_col-1] + line[self.cursor_col:]
                    self.cursor_col -= 1
                elif self.cursor_line > 0:
                    # Merge with previous line
                    prev_line = self.lines[self.cursor_line - 1]
                    curr_line = self.lines[self.cursor_line]
                    self.cursor_col = len(prev_line)
                    self.lines[self.cursor_line - 1] = prev_line + curr_line
                    self.lines.pop(self.cursor_line)
                    self.cursor_line -= 1
            elif event.key == pygame.K_DELETE:
                line = self.lines[self.cursor_line]
                if self.cursor_col < len(line):
                    self.lines[self.cursor_line] = line[:self.cursor_col] + line[self.cursor_col+1:]
                elif self.cursor_line < len(self.lines) - 1:
                    # Merge with next line
                    curr_line = self.lines[self.cursor_line]
                    next_line = self.lines[self.cursor_line + 1]
                    self.lines[self.cursor_line] = curr_line + next_line
                    self.lines.pop(self.cursor_line + 1)
            elif event.key == pygame.K_UP:
                if self.cursor_line > 0:
                    self.cursor_line -= 1
                    self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_line]))
            elif event.key == pygame.K_DOWN:
                if self.cursor_line < len(self.lines) - 1:
                    self.cursor_line += 1
                    self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_line]))
            elif event.key == pygame.K_LEFT:
                if self.cursor_col > 0:
                    self.cursor_col -= 1
                elif self.cursor_line > 0:
                    self.cursor_line -= 1
                    self.cursor_col = len(self.lines[self.cursor_line])
            elif event.key == pygame.K_RIGHT:
                if self.cursor_col < len(self.lines[self.cursor_line]):
                    self.cursor_col += 1
                elif self.cursor_line < len(self.lines) - 1:
                    self.cursor_line += 1
                    self.cursor_col = 0
            elif event.key == pygame.K_HOME:
                self.cursor_col = 0
            elif event.key == pygame.K_END:
                self.cursor_col = len(self.lines[self.cursor_line])
            else:
                if event.unicode:
                    line = self.lines[self.cursor_line]
                    self.lines[self.cursor_line] = line[:self.cursor_col] + event.unicode + line[self.cursor_col:]
                    self.cursor_col += 1
            
            # Update scroll to keep cursor visible
            if self.cursor_line < self.scroll_offset:
                self.scroll_offset = self.cursor_line
            elif self.cursor_line >= self.scroll_offset + self.visible_lines:
                self.scroll_offset = self.cursor_line - self.visible_lines + 1
            
            return True
        return False
    
    def handle_event(self, event):
        if not self.multiline:
            return self.handle_singleline_event(event)
        else:
            return self.handle_multiline_event(event)