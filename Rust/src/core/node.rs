// src/core/node.rs
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum EntityType {
    PersonMale,
    PersonFemale,
    Organization,
    Email,
    Phone,
    Document,
    Database,
    SocialMedia,
    Location, 
    Device,
}

impl EntityType {
    pub fn display_name(&self) -> &str {
        match self {
            EntityType::PersonMale => "Person (Male)",
            EntityType::PersonFemale => "Person (Female)",
            EntityType::Organization => "Organization",
            EntityType::Email => "Email",
            EntityType::Phone => "Phone",
            EntityType::Document => "Document",
            EntityType::Database => "Database",
            EntityType::SocialMedia => "SocialMedia",
            EntityType::Location => "Location",
            EntityType::Device => "Device",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Node {
    pub id: u64,
    pub entity_type: EntityType,
    pub x: f32,
    pub y: f32,
    pub label: String,
    pub notes: String,
    pub radius: f32,
}

impl Node {
    pub fn new(id: u64, entity_type: EntityType, x: f32, y:f32, radius:f32) -> Self {
        Self {
            id,
            entity_type,
            x,
            y,
            label: String::new(),
            notes: String::new(),
            radius,
        }
    }
}