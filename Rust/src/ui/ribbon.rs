// src/ui/ribbon.rs
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
            // --- Create a fully custom style ---
            let mut style = (*ctx.style()).clone();

            // Text
            style.visuals.override_text_color = Some(egui::Color32::from_rgb(220, 220, 220));

            // Widget visuals — inactive, hovered, active
            style.visuals.widgets.inactive = egui::style::WidgetVisuals {
                bg_fill: egui::Color32::from_rgb(45, 45, 50),
                weak_bg_fill: egui::Color32::from_rgb(45, 45, 50),
                bg_stroke: egui::Stroke::NONE,
                rounding: egui::Rounding::same(0.0),  // sharp corners like Python version
                fg_stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(220, 220, 220)),
                expansion: 2.0,
            };

            style.visuals.widgets.hovered = egui::style::WidgetVisuals {
                bg_fill: egui::Color32::from_rgb(70, 70, 75),
                weak_bg_fill: egui::Color32::from_rgb(70, 70, 75),
                bg_stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(120, 120, 120)),
                rounding: egui::Rounding::same(0.0),
                fg_stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(255, 255, 255)),
                expansion: 2.0,
            };

            style.visuals.widgets.active = egui::style::WidgetVisuals {
                bg_fill: egui::Color32::from_rgb(100, 100, 105),
                weak_bg_fill: egui::Color32::from_rgb(100, 100, 105),
                bg_stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(160, 160, 160)),
                rounding: egui::Rounding::same(0.0),
                fg_stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(255, 255, 255)),
                expansion: 2.0,
            };

            // Panel framing — border on the ribbon
            style.visuals.window_rounding = egui::Rounding::same(0.0);
            style.visuals.striped = false;

            // Spacing
            style.spacing.item_spacing = egui::Vec2::new(2.0, 0.0);  // small gap between buttons
            style.spacing.button_padding = egui::Vec2::new(12.0, 6.0); // roomier buttons

            ctx.set_style(style);

            // --- Ribbon panel with border ---
            egui::TopBottomPanel::top("ribbon")
                .frame(egui::Frame {
                    inner_margin: egui::Margin::symmetric(2.0, 2.0),
                    outer_margin: egui::Margin::same(0.0),
                    rounding: egui::Rounding::same(0.0),
                    shadow: egui::epaint::Shadow::NONE,
                    fill: egui::Color32::from_rgb(45, 45, 50),
                    stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(80, 80, 85)),
                })
                .show(ctx, |ui| {
                    ui.horizontal(|ui| {
                        // File button
                        let file_btn = egui::Button::new("File")
                            .min_size(egui::Vec2::new(60.0, 38.0));
                        if ui.add(file_btn).clicked() {
                            self.file_dropdown_visible = !self.file_dropdown_visible;
                            self.add_node_dropdown_visible = false;
                        }

                        // Add Node button
                        let add_btn = egui::Button::new("Add Node")
                            .min_size(egui::Vec2::new(80.0, 38.0));
                        if ui.add(add_btn).clicked() {
                            self.add_node_dropdown_visible = !self.add_node_dropdown_visible;
                            self.file_dropdown_visible = false;
                        }

                        // Help button
                        let help_btn = egui::Button::new("Help")
                            .min_size(egui::Vec2::new(55.0, 38.0));
                        if ui.add(help_btn).clicked() {
                            println!("Help clicked!");
                        }

                        // Spacer pushes trash icon to right
                        ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                            let trash_btn = egui::Button::new("🗑")
                                .min_size(egui::Vec2::new(40.0, 38.0));
                            if ui.add(trash_btn).clicked() {
                                println!("Delete clicked");
                            }
                        });
                    });
                });

            // --- File Dropdown ---
            if self.file_dropdown_visible {
                egui::Window::new("File")
                    .fixed_pos(egui::pos2(0.0, 40.0))
                    .collapsible(false)
                    .resizable(false)
                    .title_bar(false)
                    .frame(egui::Frame {
                        inner_margin: egui::Margin::same(4.0),
                        outer_margin: egui::Margin::same(0.0),
                        rounding: egui::Rounding::same(0.0),
                        shadow: egui::epaint::Shadow::NONE,
                        fill: egui::Color32::from_rgb(55, 55, 60),
                        stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(80, 80, 85)),
                    })
                    .show(ctx, |ui| {
                        ui.set_min_width(120.0);
                        for item in &["New", "Save", "Load"] {
                            if ui.button(*item).clicked() {
                                println!("{}", item);
                                self.file_dropdown_visible = false;
                            }
                        }
                    });
            }

            // --- Add Node Dropdown ---
            if self.add_node_dropdown_visible {
                egui::Window::new("Add Node")
                    .fixed_pos(egui::pos2(65.0, 40.0))
                    .collapsible(false)
                    .resizable(false)
                    .title_bar(false)
                    .frame(egui::Frame {
                        inner_margin: egui::Margin::same(4.0),
                        outer_margin: egui::Margin::same(0.0),
                        rounding: egui::Rounding::same(0.0),
                        shadow: egui::epaint::Shadow::NONE,
                        fill: egui::Color32::from_rgb(55, 55, 60),
                        stroke: egui::Stroke::new(1.0, egui::Color32::from_rgb(80, 80, 85)),
                    })
                    .show(ctx, |ui| {
                        ui.set_min_width(160.0);
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