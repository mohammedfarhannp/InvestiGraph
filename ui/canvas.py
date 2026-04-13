# ui/canvas.py
import pygame
import sys

from settings import *
from ui.camera import Camera
from ui.ui_elements import Ribbon
from ui.properties_panel import PropertiesPanel

from entities.person import Person
from entities.email import Email
from entities.phone import Phone
from entities.organization import Organization
from entities.document import Document
from entities.database import Database
from entities.social_media import SocialMedia

class Canvas:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(APPLICATION_TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.ribbon = Ribbon()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.nodes = []
        self.selected_node = None
        
        self.placement_mode = False
        self.pending_node_type = None
        
        self.dragging_node = False
        self.drag_node_offset = (0, 0)
        
        self.properties_panel = PropertiesPanel()
        

    def draw_grid(self):
        # Calculate visible grid range
        start_x = int(-self.camera.x / self.camera.zoom / GRID_SPACING) - 1
        start_y = int(-self.camera.y / self.camera.zoom / GRID_SPACING) - 1
        end_x = start_x + int(SCREEN_WIDTH / self.camera.zoom / GRID_SPACING) + 2
        end_y = start_y + int(SCREEN_HEIGHT / self.camera.zoom / GRID_SPACING) + 2
        
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                screen_x = i * GRID_SPACING * self.camera.zoom + self.camera.x
                screen_y = j * GRID_SPACING * self.camera.zoom + self.camera.y
                
                # Only draw if on screen AND below ribbon
                if -GRID_SPACING <= screen_x <= SCREEN_WIDTH + GRID_SPACING and \
                   self.ribbon.height <= screen_y <= SCREEN_HEIGHT + GRID_SPACING:
                    pygame.draw.circle(self.screen, GRID_COLOR, (int(screen_x), int(screen_y)), 2)
        
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DELETE and self.selected_node:
                    self.properties_panel.set_node(None)
                    self.nodes.remove(self.selected_node)
                    self.selected_node = None
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check dropdown first
                dropdown_result = None
                if self.ribbon.active_dropdown:
                    dropdown_result = self.ribbon.active_dropdown.handle_click(event.pos)
                    if dropdown_result:
                        print(f"Selected: {dropdown_result}")
                        self.placement_mode = True
                        self.pending_node_type = dropdown_result
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                        self.ribbon.active_dropdown = None
                        # Don't process further
                        continue
                    else:
                        # Clicked outside dropdown, close it
                        self.ribbon.active_dropdown = None
                
                # Then check ribbon buttons
                ribbon_result = self.ribbon.handle_click(event.pos)
                if ribbon_result == "delete":
                    if self.selected_node:
                        self.properties_panel.set_node(None)
                        self.nodes.remove(self.selected_node)
                        self.selected_node = None
                    continue
                
                panel_result = self.properties_panel.handle_click(event.pos)
                if panel_result == "edit label":
                    print("Edit label clicked")
                
                elif ribbon_result:
                    print(f"Clicked: {ribbon_result}")
                    
                
                # Check if in placement mode
                if self.placement_mode and not self.ribbon.active_dropdown:
                    # Convert screen to world position
                    world_x, world_y = self.camera.apply(event.pos)
                    
                    # Create node based on type
                    node_id = f"{self.pending_node_type}_{len(self.nodes)}"
                    # Add logic to create appropriate entity
                    # For now, just create Person
                    # Map dropdown text to entity
                    if self.pending_node_type in ("Person (Male)", "Person (Female)"):
                        gender = "male" if self.pending_node_type == "Person (Male)" else "female"
                        new_node = Person(node_id, "New Person", world_x, world_y, gender)
                    
                    elif self.pending_node_type == "Email":
                        new_node = Email(node_id, "Email", world_x, world_y)
                    
                    elif self.pending_node_type == "Phone":
                        new_node = Phone(node_id, "Phone", world_x, world_y)
                        
                    elif self.pending_node_type == "Organization":
                        new_node = Organization(node_id, "Organization", world_x, world_y)
                        
                    elif self.pending_node_type == "Document":
                        new_node = Document(node_id, "Document", world_x, world_y)

                    elif self.pending_node_type == "Database":
                        new_node = Database(node_id, "Database", world_x, world_y)
                        
                    elif self.pending_node_type == "Social Media":
                        new_node = SocialMedia(node_id, "Social Media", world_x, world_y)
                    

                    self.nodes.append(new_node)
                    
                    # Exit placement mode
                    self.placement_mode = False
                    self.pending_node_type = None
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    continue
                
                click_on_panel = self.properties_panel.visible and self.properties_panel.rect.collidepoint(event.pos)
                if click_on_panel:
                    # Let panel handle click, don't deselect node
                    panel_result = self.properties_panel.handle_click(event.pos)
                    if panel_result == "edit_label":
                        print("Edit label clicked")
                    # Keep current selection, don't change anything
                else:
                    # Not clicking on panel - normal node selection/deselection
                    self.selected_node = None
                    for node in reversed(self.nodes):
                        if node.contains_point(event.pos, self.camera):
                            self.selected_node = node
                            node.selected = True
                        else:
                            node.selected = False
                    
                    # Update panel based on selection
                    if self.selected_node:
                        self.properties_panel.set_node(self.selected_node)
                        # Start dragging
                        self.dragging_node = True
                        node_screen_pos = self.camera.to_screen((self.selected_node.x, self.selected_node.y))
                        self.drag_node_offset = (event.pos[0] - node_screen_pos[0], event.pos[1] - node_screen_pos[1])
                    else:
                        self.properties_panel.set_node(None)

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_node and self.selected_node:
                    world_x, world_y = self.camera.apply((event.pos[0] - self.drag_node_offset[0], 
                                                          event.pos[1] - self.drag_node_offset[1]))
                    self.selected_node.x = world_x
                    self.selected_node.y = world_y
        
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging_node = False
            
            # Camera handles its own events
            camera_should_drag = not self.selected_node
            self.camera.handle_event(event, camera_should_drag)
                    
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.ribbon.draw(self.screen)
        self.draw_grid()
        self.properties_panel.draw(self.screen)
        
        for node in self.nodes:
            node.draw(self.screen, self.camera)
            
        self.ribbon.draw_dropdowns(self.screen)
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()