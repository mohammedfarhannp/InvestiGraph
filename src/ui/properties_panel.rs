// src/ui/properties_panel.rs
use crate::core::graph::Graph;
use crate::settings::*;
use egui_macroquad::egui;

pub struct PropertiesPanel {
    pub width: f32,
}

impl PropertiesPanel {
    pub fn new() -> Self {
        Self {
            width: 280.0,
        }
    }

    pub fn draw(&mut self, graph: &mut Graph, ctx: &egui::Context) {
        // Only show if something is selected
        if graph.selected_node_id.is_none() && graph.selected_edge_id.is_none() {
            return;
        }

        let screen_width = ctx.input(|i| i.screen_rect.width());
        let x = screen_width - self.width;

        egui::Window::new("Properties")
            .fixed_pos(egui::pos2(x, RIBBON_HEIGHT))
            .auto_sized()
            .collapsible(false)
            .resizable(false)
            .title_bar(false)
            .frame(egui::Frame {
                inner_margin: egui::Margin::same(10.0),
                outer_margin: egui::Margin::same(0.0),
                rounding: egui::Rounding::same(0.0),
                shadow: egui::epaint::Shadow::NONE,
                fill: egui::Color32::from_rgb(40, 40, 45),
                stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(80, 80, 85)),
            })
            .show(ctx, |ui| {
                ui.spacing_mut().item_spacing = egui::Vec2::new(0.0, 8.0);

                
                if let Some(node) = graph.get_selected_node_mut() {
                    // Entity type header
                    ui.heading(
                        egui::RichText::new(node.entity_type.display_name())
                            .size(16.0)
                            .color(egui::Color32::from_rgb(220, 220, 220))
                    );
                    ui.separator();

                    // Label field
                    ui.label(
                        egui::RichText::new("Label")
                            .size(12.0)
                            .color(egui::Color32::from_rgb(180, 180, 180))
                    );
                    ui.add(
                        egui::TextEdit::singleline(&mut node.label)
                            .desired_width(self.width - 20.0)
                    );

                    ui.add_space(12.0);

                    // Notes field
                    ui.label(
                        egui::RichText::new("Notes")
                            .size(12.0)
                            .color(egui::Color32::from_rgb(180, 180, 180))
                    );
                    ui.add(
                        egui::TextEdit::multiline(&mut node.notes)
                            .desired_width(self.width - 20.0)
                            .desired_rows(12)
                    );
                }
                
                if let Some(edge) = graph.get_selected_edge_mut() {
                    // Edge header
                    ui.heading(
                        egui::RichText::new("Edge")
                            .size(16.0)
                            .color(egui::Color32::from_rgb(220, 220, 220))
                    );
                    ui.separator();

                    // Label field
                    ui.label(
                        egui::RichText::new("Label")
                            .size(12.0)
                            .color(egui::Color32::from_rgb(180, 180, 180))
                    );
                    ui.add(
                        egui::TextEdit::singleline(&mut edge.label)
                            .desired_width(self.width - 20.0)
                    );

                    ui.add_space(12.0);

                    // Notes field
                    ui.label(
                        egui::RichText::new("Notes")
                            .size(12.0)
                            .color(egui::Color32::from_rgb(180, 180, 180))
                    );
                    ui.add(
                        egui::TextEdit::multiline(&mut edge.notes)
                            .desired_width(self.width - 20.0)
                            .desired_rows(12)
                    );
                }
            });
    }
}