// src/utils/file_io.rs
use crate::core::graph::Graph;
use crate::core::node::Node;
use crate::core::edge::Edge;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct SaveData {
    nodes: Vec<Node>,
    edges: Vec<Edge>,
    camera_x: f32,
    camera_y: f32,
    camera_zoom: f32,
    next_id: u64,
}

pub fn save_graph(graph: &Graph, camera_x: f32, camera_y: f32, camera_zoom: f32) -> Option<String> {
    let path = rfd::FileDialog::new()
        .add_filter("InvestiGraph", &["investigraph"])
        .set_file_name("unnamed_graph")
        .save_file()?;

    let save_data = SaveData {
        nodes: graph.nodes.clone(),
        edges: graph.edges.clone(),
        camera_x,
        camera_y,
        camera_zoom,
        next_id: graph.next_id(),
    };

    let json = serde_json::to_string_pretty(&save_data).ok()?;
    std::fs::write(&path, json).ok()?;
    Some(path.to_string_lossy().to_string())
}

pub fn load_graph() -> Option<(Graph, f32, f32, f32)> {
    let path = rfd::FileDialog::new()
        .add_filter("InvestiGraph", &["investigraph"])
        .pick_file()?;

    let json = std::fs::read_to_string(&path).ok()?;
    let save_data: SaveData = serde_json::from_str(&json).ok()?;

    let mut graph = Graph::from_saved(save_data.nodes, save_data.edges, save_data.next_id);
    Some((graph, save_data.camera_x, save_data.camera_y, save_data.camera_zoom))
}

pub fn new_graph() -> bool {
    let result = rfd::MessageDialog::new()
        .set_title("New Graph")
        .set_description("Discard current graph and start new?")
        .set_buttons(rfd::MessageButtons::YesNo)
        .show();
    
    result == rfd::MessageDialogResult::Yes
}