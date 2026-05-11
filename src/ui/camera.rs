// src/camera.rs
pub struct Camera {
    pub x: f32,
    pub y: f32,
    pub zoom: f32,
}


impl Camera {
    pub fn new() -> Self {
        Self {
            x: 0.0,
            y: 0.0,
            zoom: 1.0,
        }
    }

    pub fn screen_to_world(&self, screen_x: f32, screen_y:f32) -> (f32, f32) {
        let world_x = (screen_x - self.x) / self.zoom;
        let world_y = (screen_y - self.y) / self.zoom;
        (world_x, world_y)
    }

    pub fn world_to_screen(&self, world_x: f32, world_y: f32) -> (f32, f32) {
        let screen_x = world_x * self.zoom + self.x;
        let screen_y = world_y * self.zoom + self.y;
        (screen_x, screen_y)
    }

}