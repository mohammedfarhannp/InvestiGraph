// src/main.rs
use macroquad::prelude::*;

mod settings;
mod ui;

use ui::camera::Camera;

use settings::*;

#[macroquad::main("InvestiGraph")]
async fn main() {
    request_new_screen_size(SCREEN_WIDTH, SCREEN_HEIGHT);

    // Camera Variables Set!
    let mut camera = Camera::new();
    let mut camera_dragging : bool = false;
    let drag_start = (0.0, 0.0);

    // Main Loop (I guess)
    loop {
        clear_background(rgb(BACKGROUND_COLOR));

        // Draw Grid
        let start_x = (-camera.x / camera.zoom / GRID_SPACING) as i32 -1;
        let start_y = (-camera.x / camera.zoom / GRID_SPACING) as i32 -1;

        let end_x = start_x + (SCREEN_WIDTH / camera.zoom / GRID_SPACING) as i32 + 2;
        let end_y = start_y + (SCREEN_HEIGHT / camera.zoom / GRID_SPACING) as i32 + 2;

        for i in start_x..end_x {
            for j in start_y..end_y {
                let screen_x = i as f32 * GRID_SPACING * camera.zoom + camera.x;
                let screen_y = j as f32 * GRID_SPACING * camera.zoom + camera.y;


                if screen_x >= -GRID_SPACING && screen_x <= SCREEN_WIDTH + GRID_SPACING && screen_y >= RIBBON_HEIGHT && screen_y <= SCREEN_HEIGHT + GRID_SPACING {
                    draw_circle(screen_x, screen_y, 2.0, rgb(GRID_COLOR));
                }
            }
        }

        // Camera Controls
        if is_mouse_button_down(MouseButton::Left) && !camera_dragging {
            camera_dragging = true;
        }

        // Camera Pan Logic
        if camera_dragging {
            if is_mouse_button_down(MouseButton::Left) {
                let (mouse_x, mouse_y) = mouse_position();
            } else {
                camera_dragging = false;
            }
        }

        // Zoom with mouse wheel
        let wheel = mouse_wheel();
        if wheel.1 != 0.0 {
            let zoom_factor = if wheel.1 > 0.0 { 1.1 } else { 0.9 };
            let new_zoom = (camera.zoom * zoom_factor).clamp(0.4, 2.0);

            // Zoom toward mouse position
            let (mouse_x, mouse_y) = mouse_position();
            let (world_x, world_y) = camera.screen_to_world(mouse_x, mouse_y);

            camera.zoom = new_zoom;
            let (new_mouse_x, new_mouse_y) = camera.world_to_screen(world_x, world_y);

            camera.x += mouse_x - new_mouse_x;
            camera.y += mouse_y - new_mouse_y;
        }

        if is_key_pressed(KeyCode::Escape) {
            break;
        }

        next_frame().await;
    }

}
