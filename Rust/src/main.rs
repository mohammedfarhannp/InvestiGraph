// src/main.rs
use macroquad::prelude::*;

#[macroquad::main("InvestiGraph")]
async fn main() {
    loop {

        clear_background(Color::new(30.0/255.0, 30.0/255.0, 35.0/255.0, 1.0));

        if is_key_pressed(KeyCode::Escape) {
            break;
        }

        next_frame().await;
    }

}
