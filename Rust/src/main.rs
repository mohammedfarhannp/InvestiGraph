// src/main.rs
use macroquad::prelude::*;

mod settings;
use settings::rgb();


#[macroquad::main(settings::APPLICATION_TITLE)]
async fn main() {
    loop {

        clear_background(rgb(BACKGROUND_COLOR));

        if is_key_pressed(KeyCode::Escape) {
            break;
        }

        next_frame().await;
    }

}
