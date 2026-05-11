use macroquad::prelude::*;
use std::collections::HashMap;
use crate::settings::*;

pub struct AssetManager {
    textures:HashMap<String, Texture2D>,
}

impl AssetManager {
    pub async fn new() -> Self {
        let mut textures = HashMap::new();

        let icons: [(&str, &str); 10] = [
            ("PersonMale", PERSON_MALE_ICON),
            ("PersonFemale", PERSON_FEMALE_ICON),
            ("Organization", ORGANIZATION_ICON),
            ("Email", EMAIL_ICON),
            ("Phone", PHONE_ICON),
            ("Document", DOCUMENT_ICON),
            ("Database", DATABASE_ICON),
            ("SocialMedia", SOCIAL_MEDIA_ICON),
            ("Location", LOCATION_ICON),
            ("Device", DEVICE_ICON),
        ];

        for (name, path) in icons {
            if let Ok(texture) = load_texture(path).await {
                textures.insert(name.to_string(), texture);
            }
        }

        Self { textures }
    }

    pub fn get_icon(&self, entity_type: &str) -> Option<&Texture2D> {
        self.textures.get(entity_type)
    }
}