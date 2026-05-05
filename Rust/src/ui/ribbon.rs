use macroquad::prelude::*;
use egui_macroquad::{ui, egui};

pub struct Ribbon {
    pub height: f32,
    pub add_node_dropdown_visible: bool,
    pub file_dropdown_visible: bool,
}

impl Ribbon {
    pub fn new() -> Self {
        Self {
            height: 40.0,
            add_node_dropdown_visible: false,
            file_dropdown_visible: false,
        }
    }

    pub fn draw(&mut self) {
        ui(|ctx| {
            // Top panel (ribbon)
            egui::TopBottomPanel::top("ribbon").show(ctx, |ui| {
                ui.horizontal(|ui| {
                    if ui.button("File").clicked() {
                        self.file_dropdown_visible = !self.file_dropdown_visible;
                        self.add_node_dropdown_visible = false;
                    }
                    if ui.button("Add Node").clicked() {
                        self.add_node_dropdown_visible = !self.add_node_dropdown_visible;
                        self.file_dropdown_visible = false;
                    }
                    if ui.button("Help").clicked() {
                        println!("Help clicked!");
                    }
                    ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                        if ui.button("🗑").clicked() {
                            println!("Delete clicked");
                        }
                    });
                });
            });

            // File Dropdown
            if self.file_dropdown_visible {
                egui::Window::new("File")
                    .fixed_pos(egui::pos2(10.0, 40.0))
                    .collapsible(false)
                    .resizable(false)
                    .show(ctx, |ui| {
                        if ui.button("New").clicked() {
                            println!("New");
                            self.file_dropdown_visible = false;
                        }
                        if ui.button("Save").clicked() {
                            println!("Save");
                            self.file_dropdown_visible = false;
                        }
                        if ui.button("Load").clicked() {
                            println!("Load");
                            self.file_dropdown_visible = false;
                        }
                    });
            }

            // Add Node Dropdown
            if self.add_node_dropdown_visible {
                egui::Window::new("Add Node")
                    .fixed_pos(egui::pos2(70.0, 40.0))
                    .collapsible(false)
                    .resizable(false)
                    .show(ctx, |ui| {
                        let node_types = [
                            "Person (Male)", "Person (Female)", "Organization",
                            "Email", "Phone", "Document", "Database",
                            "Social Media", "Location", "Device"
                        ];
                        for node_type in node_types {
                            if ui.button(node_type).clicked() {
                                println!("Selected: {}", node_type);
                                self.add_node_dropdown_visible = false;
                            }
                        }
                    });
            }
        });
    }
}