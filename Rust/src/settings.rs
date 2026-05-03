// src/settings.rs

// Window
pub const SCREEN_WIDTH : f32 = 1000.0;
pub const SCREEN_HEIGHT : f32 = 600.0;

// Grid
pub const GRID_COLOR : (u8, u8, u8) = (50, 50, 55);
pub const GRID_SPACING: f32 = 50.0

// Background
pub const BACKGROUND_COLOR: (u8, u8, u8) = (30, 30, 35);

// Application
pub const APPLICATION_TITLE: &str = "InvestiGraph";
pub const FPS: u32 = 60;

// Node Colors
pub const COLOR_PERSON_MALE: (u8, u8, u8) = (100, 150, 255);
pub const COLOR_PERSON_FEMALE: (u8, u8, u8) = (255, 150, 200);
pub const COLOR_ORGANIZATION: (u8, u8, u8) = (255, 165, 0);
pub const COLOR_EMAIL: (u8, u8, u8) = (100, 255, 100);
pub const COLOR_PHONE: (u8, u8, u8) = (180, 100, 255);
pub const COLOR_DOCUMENT: (u8, u8, u8) = (255, 255, 100);
pub const COLOR_DATABASE: (u8, u8, u8) = (128, 128, 128);
pub const COLOR_SOCIAL_MEDIA: (u8, u8, u8) = (29, 161, 242);
pub const COLOR_LOCATION: (u8, u8, u8) = (0, 150, 200);
pub const COLOR_DEVICE: (u8, u8, u8) = (100, 200, 100);

// Node Defaults
pub const DEFAULT_NODE_RADIUS: f32 = 30.0;
pub const DEFAULT_FONT_SIZE: f32 = 12.0;
pub const DEFAULT_NODE_COLOR: (u8, u8, u8) = (150, 150, 150);

// Icon Paths
pub const ICON_PATH : &str = "assets/icons/";

pub const DATABASE_ICON : &str = concat!(ICON_PATH, "Database.png");
pub const DEVICE_ICON : &str = concat!(ICON_PATH, "Device.png");
pub const DOCUMENT_ICON : &str = concat!(ICON_PATH, "Document.png");
pub const EMAIL_ICON : &str = concat!(ICON_PATH, "Email.png");
pub const LOCATION_ICON : &str = concat!(ICON_PATH, "Location.png");
pub const ORGANIZATION_ICON : &str = concat!(ICON_PATH, "Organization.png");
pub const PHONE_ICON : &str = concat!(ICON_PATH, "Phone.png");
pub const SOCIAL_MEDIA_ICON : &str = concat!(ICON_PATH, "Social_Media.png");
pub const PERSON_MALE_ICON : &str = concat!(ICON_PATH, "male.png");
pub const PERSON_FEMALE_ICON : &str = concat!(ICON_PATH, "female.png");
pub const TRASH_ICON : &str = concat!(ICON_PATH, "trash.png");

// Named Colors (RGB u8)
pub const BASTILLE: (u8, u8, u8) = (45, 45, 50);
pub const WATER_OUZEL: (u8, u8, u8) = (80, 80, 85);
pub const GAINSBORO: (u8, u8, u8) = (220, 220, 220);
pub const VULCAN: (u8, u8, u8) = (55, 55, 60);
pub const BLACK: (u8, u8, u8) = (0, 0, 0);
pub const YELLOW: (u8, u8, u8) = (255, 255, 0);
pub const WHITE: (u8, u8, u8) = (255, 255, 255);
pub const BRUSHED_METAL: (u8, u8, u8) = (200, 200, 200);
pub const BRAINSTEM_GRAY: (u8, u8, u8) = (180, 180, 180);
pub const BLUE_GENIE: (u8, u8, u8) = (100, 100, 255);
pub const IN_THE_DARK: (u8, u8, u8) = (60, 60, 65);
pub const WESTCHESTER_GRAY: (u8, u8, u8) = (120, 120, 120);
pub const CASTING_SEA: (u8, u8, u8) = (70, 130, 200);

// Helper function to convert (u8, u8, u8) to macroquad Color
pub fn rgb(rgb: (u8, u8, u8)) -> macroquad::color::Color {
    macroquad::color::Color::new(
        rgb.0 as f32 / 255.0,
        rgb.1 as f32 / 255.0,
        rgb.2 as f32 / 255.0,
        1.0,
    )
}