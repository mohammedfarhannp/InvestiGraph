use std::env;
use std::fs;
use std::path::Path;

fn main() {
    // 1. Compile the native Windows resource (Fixes Taskbar/Exe icon blurriness)
    if std::env::var("CARGO_CFG_TARGET_OS").unwrap() == "windows" {
        embed_resource::compile("app.rc", embed_resource::NONE);
    }

    // 2. Generate icon.rs so main.rs compiles successfully
    let out_dir = env::var("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("icon.rs");
    
    // Load the icon
    let img = image::open("assets/icons/icon.ico")
        .expect("Failed to load icon");
    
    // Resize to required sizes for the macroquad fallback arrays
    let small = image::imageops::resize(&img, 16, 16, image::imageops::FilterType::Lanczos3);
    let medium = image::imageops::resize(&img, 32, 32, image::imageops::FilterType::Lanczos3);
    let big = image::imageops::resize(&img, 64, 64, image::imageops::FilterType::Lanczos3);
    
    let small_rgba = small.into_raw();
    let medium_rgba = medium.into_raw();
    let big_rgba = big.into_raw();
    
    let icon_code = format!(
        "pub const ICON_SMALL: [u8; 1024] = {:?};\n\
         pub const ICON_MEDIUM: [u8; 4096] = {:?};\n\
         pub const ICON_BIG: [u8; 16384] = {:?};",
        small_rgba, medium_rgba, big_rgba
    );
    
    fs::write(&dest_path, icon_code).unwrap();

    // Rerun triggers
    println!("cargo:rerun-if-changed=assets/icons/icon.ico");
    println!("cargo:rerun-if-changed=app.rc");
}