// src/core/graph.rs
use crate::core::edge::Edge;
use crate::core::node::{EntityType, Node};

#[derive(Debug, Clone)]
pub struct Graph {
    pub nodes: Vec<Node>,
    pub edges: Vec<Edge>,
    pub selected_node_id: Option<u64>,
    pub selected_edge_id: Option<u64>,
    next_id: u64,
}

impl Graph {
    pub fn new() -> Self {
        Self {
            nodes: Vec::new(),
            edges: Vec::new(),
            selected_node_id: None,
            selected_edge_id: None,
            next_id: 1,
        }
    }

    // Add Node
    pub fn add_node(&mut self, entity_type: EntityType, x: f32, y: f32, radius:f32) -> u64 {
        let id = self.next_id;
        self.next_id += 1;
        let node = Node::new(id, entity_type, x, y, radius);
        self.nodes.push(node);
        id
    }

    // Remove Node
    pub fn remove_node(&mut self, id: u64) {
        self.nodes.retain(|n| n.id != id);
        self.edges.retain(|e| e.source_id != id && e.target_id != id);
        if self.selected_node_id == Some(id) {
            self.selected_node_id = None;
            self.selected_edge_id = None;
        }
    }

    // Add Edge
    pub fn add_edge(&mut self, source_id: u64, target_id: u64) -> u64 {
        let id = self.next_id;
        self.next_id += 1;
        let edge = Edge::new(id, source_id, target_id);
        self.edges.push(edge);
        id
    }

    // Remove Edge
    pub fn remove_edge(&mut self, id: u64) {
        self.edges.retain(|e| e.id != id);
        if self.selected_edge_id == Some(id) {
            self.selected_edge_id = None;
        }
    }

    // Select Node
    pub fn select_node(&mut self, id: Option<u64>) {
        self.selected_node_id = id;
        self.selected_edge_id = None;
    }

    // Select Node
    pub fn select_edge(&mut self, id: Option<u64>) {
        self.selected_edge_id = id;
        self.selected_node_id = None;
    }

    // Clear Selection
    pub fn clear_selection(&mut self, id: Option<u64>) {
        self.selected_node_id = None;
        self.selected_edge_id = None;
    }
    
    pub fn get_selected_node(&self) -> Option<&Node> {
        self.selected_node_id.and_then(|id| self.nodes.iter_mut().find(|n| n.id == id))
    }

    pub fn get_selected_node_mut(&mut self) -> Option<&mut Node> {
        self.selected_node_id.and_then(|id| self.nodes.iter_mut().find(|n| n.id == id))
    }

    pub fn get_selected_edge(&self) -> Option<&mut Node> {
        self.selected_edge_id.and_then(|id| self.edges.iter().find(|e| e.id == id))
    }

}
