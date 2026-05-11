// src/core/edge.rs
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Edge {
    pub id: u64,
    pub source_id: u64,
    pub target_id: u64,
    pub label: String,
    pub notes: String,
}

impl Edge {
    pub fn new(id: u64, source_id: u64, target_id: u64) -> Self {
        Self {
            id,
            source_id,
            target_id,
            label: String::new(),
            notes: String::new(),
        }
    }
}