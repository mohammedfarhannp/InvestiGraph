// src/main.rs
use macroquad::prelude::*;

mod core;
mod settings;
mod ui;

use core::graph::Graph;
use core::node::EntityType;
use ui::camera::Camera;
use ui::ribbon::Ribbon;

use settings::*;

#[macroquad::main("InvestiGraph")]
async fn main() {
    request_new_screen_size(SCREEN_WIDTH, SCREEN_HEIGHT);

    // Graph
    let mut graph = Graph::new();
    let mut pending_node_type: Option<EntityType> = None;
    let mut creating_edge_from: Option<u64> = None;

    // Camera Variables Set!
    let mut camera = Camera::new();
    let mut camera_dragging: bool = false;
    let mut drag_start = (0.0, 0.0);
    let mut drag_start_camera = (0.0, 0.0);

    // Node dragging
    let mut node_dragging: Option<u64> = None;
    let mut node_drag_offset = (0.0, 0.0);

    // Ribbon
    let mut ribbon = Ribbon::new();

    // Main Loop (I guess)
    loop {
        clear_background(rgb(BACKGROUND_COLOR));

        ribbon.draw();

        // --- Handle ribbon actions ---
        // Check if a node type was selected from ribbon
        if let Some(ref entity_type) = ribbon.selected_entity_type {
            pending_node_type = Some(entity_type.clone());
            ribbon.selected_entity_type = None;
        }

        // Draw Grid
        let start_x = (-camera.x / camera.zoom / GRID_SPACING) as i32 - 1;
        let start_y = (-camera.y / camera.zoom / GRID_SPACING) as i32 - 1;

        let end_x = start_x + (SCREEN_WIDTH / camera.zoom / GRID_SPACING) as i32 + 2;
        let end_y = start_y + (SCREEN_HEIGHT / camera.zoom / GRID_SPACING) as i32 + 2;

        for i in start_x..end_x {
            for j in start_y..end_y {
                let screen_x = i as f32 * GRID_SPACING * camera.zoom + camera.x;
                let screen_y = j as f32 * GRID_SPACING * camera.zoom + camera.y;

                if screen_x >= -GRID_SPACING
                    && screen_x <= SCREEN_WIDTH + GRID_SPACING
                    && screen_y >= RIBBON_HEIGHT
                {
                    draw_circle(screen_x, screen_y, 2.0, rgb(GRID_COLOR));
                }
            }
        }

        // Draw edges
        for edge in &graph.edges {
            let source = graph.nodes.iter().find(|n| n.id == edge.source_id);
            let target = graph.nodes.iter().find(|n| n.id == edge.target_id);
            if let (Some(s), Some(t)) = (source, target) {
                let (sx, sy) = camera.world_to_screen(s.x, s.y);
                let (tx, ty) = camera.world_to_screen(t.x, t.y);

                // Line
                let edge_color = if graph.selected_edge_id == Some(edge.id) {
                    MY_YELLOW
                } else {
                    GAINSBORO
                };
                draw_line(sx, sy, tx, ty, 2.0, rgb(edge_color));

                // Arrowhead at target
                let angle = (ty - sy).atan2(tx - sx);
                let arrow_len = 10.0 * camera.zoom;
                let arrow_angle = std::f32::consts::PI / 6.0;
                let ax1 = tx - arrow_len * (angle - arrow_angle).cos();
                let ay1 = ty - arrow_len * (angle - arrow_angle).sin();
                let ax2 = tx - arrow_len * (angle + arrow_angle).cos();
                let ay2 = ty - arrow_len * (angle + arrow_angle).sin();
                draw_line(tx, ty, ax1, ay1, 2.0, rgb(edge_color));
                draw_line(tx, ty, ax2, ay2, 2.0, rgb(edge_color));
            }
        }

        // Edge creation preview (when creating_edge_from is set)
        if let Some(source_id) = creating_edge_from {
            if let Some(source) = graph.nodes.iter().find(|n| n.id == source_id) {
                let (sx, sy) = camera.world_to_screen(source.x, source.y);
                let (mouse_x, mouse_y) = mouse_position();
                // Don't draw line into ribbon area
                if mouse_y > RIBBON_HEIGHT {
                    draw_line(sx, sy, mouse_x, mouse_y, 2.0, rgb(BLUE_GENIE));
                }
            }
        }

        // Draw nodes
        for node in &graph.nodes {
            let (sx, sy) = camera.world_to_screen(node.x, node.y);
            let screen_radius = (node.radius * camera.zoom).max(5.0);

            if sx + screen_radius < 0.0
                || sx - screen_radius > SCREEN_WIDTH
                || sy + screen_radius < RIBBON_HEIGHT
                || sy - screen_radius > SCREEN_HEIGHT
            {
                continue; // Skip off-screen nodes
            }

            let color = get_entity_color(&node.entity_type);

            // Selection highlight
            if graph.selected_node_id == Some(node.id) {
                draw_circle(sx, sy, screen_radius + 3.0, rgb(MY_YELLOW));
            }

            // Node body
            draw_circle(sx, sy, screen_radius, rgb(color));

            // Label
            let font_size = (DEFAULT_FONT_SIZE * camera.zoom).max(8.0);
            if !node.label.is_empty() {
                let text_width = measure_text(&node.label, None, font_size as u16, 1.0).width;
                draw_text(
                    &node.label,
                    sx - text_width / 2.0,
                    sy + screen_radius + font_size,
                    font_size,
                    rgb(GAINSBORO),
                );
            }
        }

        // --- Mouse Interaction ---
        let (mouse_x, mouse_y) = mouse_position();
        let mouse_in_canvas = mouse_y > RIBBON_HEIGHT;

        // Handle node dragging
        if is_mouse_button_pressed(MouseButton::Left) && mouse_in_canvas {
            let (world_x, world_y) = camera.screen_to_world(mouse_x, mouse_y);

            // Check if clicking on a node
            let mut clicked_node = None;
            for node in graph.nodes.iter().rev() {
                let dx = world_x - node.x;
                let dy = world_y - node.y;
                let hit_radius = (node.radius * 1.5).max(15.0 / camera.zoom);
                if dx * dx + dy * dy <= hit_radius * hit_radius {
                    clicked_node = Some(node.id);
                    break;
                }
            }

            if let Some(node_id) = clicked_node {
                // Node clicked
                if creating_edge_from.is_some() {
                    // Completing an edge
                    let source_id = creating_edge_from.take().unwrap();
                    if source_id != node_id {
                        graph.add_edge(source_id, node_id);
                    }
                } else {
                    // Select and start dragging
                    graph.select_node(Some(node_id));
                    node_dragging = Some(node_id);
                    if let Some(node) = graph.nodes.iter().find(|n| n.id == node_id) {
                        node_drag_offset = (node.x - world_x, node.y - world_y);
                    }
                }
                camera_dragging = false;
            } else if creating_edge_from.is_some() {
                // Clicked empty space while creating edge -> cancel
                creating_edge_from = None;
            } else if pending_node_type.is_some() {
                // Place new node
                let entity_type = pending_node_type.take().unwrap();
                let id = graph.add_node(entity_type, world_x, world_y, DEFAULT_NODE_RADIUS);
                graph.select_node(Some(id));
                node_dragging = Some(id);
                node_drag_offset = (0.0, 0.0);
                camera_dragging = false;
            } else {
                // Clicked empty space -> deselect
                graph.clear_selection();
                camera_dragging = true;
                drag_start = (mouse_x, mouse_y);
                drag_start_camera = (camera.x, camera.y);
            }
        }

        // Handle right-click for edge creation
        if is_mouse_button_pressed(MouseButton::Right) && mouse_in_canvas {
            let (world_x, world_y) = camera.screen_to_world(mouse_x, mouse_y);

            let mut clicked_node = None;
            for node in graph.nodes.iter().rev() {
                let dx = world_x - node.x;
                let dy = world_y - node.y;
                let hit_radius = (node.radius * 1.5).max(15.0 / camera.zoom);
                if dx * dx + dy * dy <= hit_radius * hit_radius {
                    clicked_node = Some(node.id);
                    break;
                }
            }

            if let Some(node_id) = clicked_node {
                creating_edge_from = Some(node_id);
            } else {
                creating_edge_from = None;
            }
        }

        // Node dragging movement
        if is_mouse_button_down(MouseButton::Left) {
            if let Some(node_id) = node_dragging {
                let (world_x, world_y) = camera.screen_to_world(mouse_x, mouse_y);
                if let Some(node) = graph.nodes.iter_mut().find(|n| n.id == node_id) {
                    node.x = world_x + node_drag_offset.0;
                    node.y = world_y + node_drag_offset.1;
                }
            } else if camera_dragging {
                let (mx, my) = mouse_position();
                camera.x = drag_start_camera.0 + (mx - drag_start.0);
                camera.y = drag_start_camera.1 + (my - drag_start.1);
            }
        } else {
            node_dragging = None;
            camera_dragging = false;
        }

        // Zoom with mouse wheel
        let wheel = mouse_wheel();
        if wheel.1 != 0.0 {
            let zoom_factor = if wheel.1 > 0.0 { 1.1 } else { 0.9 };
            let new_zoom = (camera.zoom * zoom_factor).clamp(0.4, 2.0);

            let (mx, my) = mouse_position();
            let (world_x, world_y) = camera.screen_to_world(mx, my);

            camera.zoom = new_zoom;
            let (new_mx, new_my) = camera.world_to_screen(world_x, world_y);

            camera.x += mx - new_mx;
            camera.y += my - new_my;
        }

        // Delete key
        if is_key_pressed(KeyCode::Delete) {
            if let Some(node_id) = graph.selected_node_id {
                graph.remove_node(node_id);
            } else if let Some(edge_id) = graph.selected_edge_id {
                graph.remove_edge(edge_id);
            }
        }

        if is_key_pressed(KeyCode::Escape) {
            pending_node_type = None;
            creating_edge_from = None;
        }

        egui_macroquad::draw();
        next_frame().await;
    }
}

fn get_entity_color(entity_type: &EntityType) -> (u8, u8, u8) {
    match entity_type {
        EntityType::PersonMale => COLOR_PERSON_MALE,
        EntityType::PersonFemale => COLOR_PERSON_FEMALE,
        EntityType::Organization => COLOR_ORGANIZATION,
        EntityType::Email => COLOR_EMAIL,
        EntityType::Phone => COLOR_PHONE,
        EntityType::Document => COLOR_DOCUMENT,
        EntityType::Database => COLOR_DATABASE,
        EntityType::SocialMedia => COLOR_SOCIAL_MEDIA,
        EntityType::Location => COLOR_LOCATION,
        EntityType::Device => COLOR_DEVICE,
    }
}