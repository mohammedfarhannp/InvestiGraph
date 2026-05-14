// build.rs

use std::env;
use std::fs;
use std::path::Path;
use std::io::Write;

fn main() {
    // 1. Compile the native Windows resource (Fixes Taskbar/Exe icon blurriness)
    if std::env::var("CARGO_CFG_TARGET_OS").unwrap() == "windows" {
        embed_resource::compile("app.rc", embed_resource::NONE);
    }

    // 2. Generate embedded_assets.rs with all icons baked in
    let out_dir = env::var("OUT_DIR").unwrap();
    let dest_path = Path::new(&out_dir).join("embedded_assets.rs");
    let mut f = fs::File::create(&dest_path).unwrap();

    // --- Application icon arrays (for macroquad window icon fallback) ---
    let icon_img = image::open("assets/logo/icon.ico")
        .expect("Failed to load icon.ico");
    
    let small = image::imageops::resize(&icon_img, 16, 16, image::imageops::FilterType::Lanczos3);
    let medium = image::imageops::resize(&icon_img, 32, 32, image::imageops::FilterType::Lanczos3);
    let big = image::imageops::resize(&icon_img, 64, 64, image::imageops::FilterType::Lanczos3);
    
    writeln!(f, "pub const ICON_SMALL: [u8; 1024] = {:?};", small.into_raw()).unwrap();
    writeln!(f, "pub const ICON_MEDIUM: [u8; 4096] = {:?};", medium.into_raw()).unwrap();
    writeln!(f, "pub const ICON_BIG: [u8; 16384] = {:?};", big.into_raw()).unwrap();

    // --- All entity icons + trash icon ---
    let png_icons = [
        ("DATABASE_PNG", "assets/icons/Database.png"),
        ("DEVICE_PNG", "assets/icons/Device.png"),
        ("DOCUMENT_PNG", "assets/icons/Document.png"),
        ("EMAIL_PNG", "assets/icons/Email.png"),
        ("LOCATION_PNG", "assets/icons/Location.png"),
        ("ORGANIZATION_PNG", "assets/icons/Organization.png"),
        ("PHONE_PNG", "assets/icons/Phone.png"),
        ("SOCIAL_MEDIA_PNG", "assets/icons/Social_Media.png"),
        ("PERSON_MALE_PNG", "assets/icons/male.png"),
        ("PERSON_FEMALE_PNG", "assets/icons/female.png"),
        ("TRASH_PNG", "assets/icons/trash.png"),
    ];

    for (const_name, path) in &png_icons {
        let bytes = fs::read(path)
            .unwrap_or_else(|e| panic!("Failed to read {}: {}", path, e));
        writeln!(f, "pub const {}: &[u8] = &{:?};", const_name, bytes).unwrap();
    }

    // Rerun triggers
    println!("cargo:rerun-if-changed=assets/logo/icon.ico");
    for (_, path) in &png_icons {
        println!("cargo:rerun-if-changed={}", path);
    }
    println!("cargo:rerun-if-changed=app.rc");
}