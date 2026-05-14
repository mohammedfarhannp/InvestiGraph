// src/utils/assets.rs

use macroquad::prelude::*;
use std::collections::HashMap;

// Include the generated embedded assets
include!(concat!(env!("OUT_DIR"), "/embedded_assets.rs"));

pub struct AssetManager {
    textures: HashMap<String, Texture2D>,
}

impl AssetManager {
    pub fn new() -> Self {
        let mut textures = HashMap::new();

        // Map entity type names to their embedded PNG bytes
        let icons: [(&str, &[u8]); 10] = [
            ("PersonMale",    PERSON_MALE_PNG),
            ("PersonFemale",  PERSON_FEMALE_PNG),
            ("Organization",  ORGANIZATION_PNG),
            ("Email",         EMAIL_PNG),
            ("Phone",         PHONE_PNG),
            ("Document",      DOCUMENT_PNG),
            ("Database",      DATABASE_PNG),
            ("SocialMedia",   SOCIAL_MEDIA_PNG),
            ("Location",      LOCATION_PNG),
            ("Device",        DEVICE_PNG),
        ];

        for (name, bytes) in icons {
            let texture = Texture2D::from_file_with_format(bytes, Some(image::ImageFormat::Png));
            textures.insert(name.to_string(), texture);
        }

        Self { textures }
    }

    pub fn get_icon(&self, entity_type: &str) -> Option<&Texture2D> {
        self.textures.get(entity_type)
    }

    /// Returns the embedded trash icon PNG bytes for use in the ribbon
    pub fn trash_icon_bytes() -> &'static [u8] {
        TRASH_PNG
    }
}