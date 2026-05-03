// src/main.rs
use macroquad::prelude::*;

mod settings;
use settings::*;


#[macroquad::main(APPLICATION_TITLE)]
async fn main() {
    request_new_screen_size(SCREEN_WIDTH, SCREEN_HEIGHT);

    loop {
        clear_background(rgb(BACKGROUND_COLOR));

        if is_key_pressed(KeyCode::Escape) {
            break;
        }

        next_frame().await;
    }

}
