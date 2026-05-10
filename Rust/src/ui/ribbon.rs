// src/ui/ribbon.rs
use macroquad::prelude::*;
use egui_macroquad::egui;
use crate::settings::{
    RIBBON_HEIGHT, BASTILLE, WATER_OUZEL, GAINSBORO, TRASH_ICON,
    IN_THE_DARK, WESTCHESTER_GRAY, BRAINSTEM_GRAY, VULCAN, WHITE, egui_rgb,
};
use crate::core::node::EntityType;

#[derive(Clone, PartialEq)]
pub enum FileAction {
    New,
    Save,
    Load,
}

pub struct Ribbon {
    pub height: f32,
    pub add_node_dropdown_visible: bool,
    pub file_dropdown_visible: bool,
    pub selected_entity_type: Option<EntityType>,
    close_pending: bool,
    pub pending_file_action: Option<FileAction>,
    pub pending_delete: bool,
}

impl Ribbon {
    pub fn new() -> Self {
        Self {
            height: RIBBON_HEIGHT,
            add_node_dropdown_visible: false,
            file_dropdown_visible: false,
            selected_entity_type: None,
            close_pending: false,
            pending_file_action: None,
            pending_delete: false,
        }
    }

    pub fn draw(&mut self, ctx: &egui::Context) {
        let mut style = (*ctx.style()).clone();

        // Text
        style.visuals.override_text_color = Some(egui_rgb(GAINSBORO));

        // Widget visuals — inactive, hovered, active
        style.visuals.widgets.inactive = egui::style::WidgetVisuals {
            bg_fill: egui_rgb(BASTILLE),
            weak_bg_fill: egui_rgb(BASTILLE),
            bg_stroke: egui::Stroke::NONE,
            rounding: egui::Rounding::same(0.0),
            fg_stroke: egui::Stroke::new(1.0, egui_rgb(GAINSBORO)),
            expansion: 2.0,
        };

        style.visuals.widgets.hovered = egui::style::WidgetVisuals {
            bg_fill: egui_rgb(IN_THE_DARK),
            weak_bg_fill: egui_rgb(IN_THE_DARK),
            bg_stroke: egui::Stroke::NONE,
            rounding: egui::Rounding::same(0.0),
            fg_stroke: egui::Stroke::new(1.0, egui_rgb(WHITE)),
            expansion: 2.0,
        };

        style.visuals.widgets.active = egui::style::WidgetVisuals {
            bg_fill: egui_rgb(WATER_OUZEL),
            weak_bg_fill: egui_rgb(WATER_OUZEL),
            bg_stroke: egui::Stroke::new(1.0, egui_rgb(BRAINSTEM_GRAY)),
            rounding: egui::Rounding::same(0.0),
            fg_stroke: egui::Stroke::new(1.0, egui_rgb(WHITE)),
            expansion: 2.0,
        };

        style.visuals.window_rounding = egui::Rounding::same(0.0);
        style.visuals.striped = false;

        style.spacing.item_spacing = egui::Vec2::new(2.0, 0.0);
        style.spacing.button_padding = egui::Vec2::new(12.0, 6.0);

        ctx.set_style(style);

        // Close dropdowns when clicking on canvas (deferred by one frame)
        if self.close_pending {
            self.file_dropdown_visible = false;
            self.add_node_dropdown_visible = false;
            self.close_pending = false;
        }
        if ctx.input(|i| i.pointer.button_clicked(egui::PointerButton::Primary)) {
            let pointer_pos = ctx.input(|i| i.pointer.hover_pos());
            if let Some(pos) = pointer_pos {
                let below_ribbon = pos.y > self.height + 5.0;
                let mut clicking_on_dropdown = false;

                // Only check the dropdown that's currently visible
                if self.file_dropdown_visible {
                    if pos.x > 0.0 && pos.x < 120.0 && pos.y > 40.0 && pos.y < 130.0 {
                        clicking_on_dropdown = true;
                    }
                }
                if self.add_node_dropdown_visible {
                    if pos.x > 65.0 && pos.x < 240.0 && pos.y > 40.0 && pos.y < 340.0 {
                        clicking_on_dropdown = true;
                    }
                }

                if below_ribbon && !clicking_on_dropdown {
                    self.close_pending = true;
                }
            }
        }

        // --- Ribbon panel ---
        egui::TopBottomPanel::top("ribbon")
            .frame(egui::Frame {
                inner_margin: egui::Margin::symmetric(2.0, 2.0),
                outer_margin: egui::Margin::same(0.0),
                rounding: egui::Rounding::same(0.0),
                shadow: egui::epaint::Shadow::NONE,
                fill: egui_rgb(BASTILLE),
                stroke: egui::Stroke::new(1.0, egui_rgb(WATER_OUZEL)),
            })
            .show(ctx, |ui| {
                ui.horizontal(|ui| {
                    let file_btn = egui::Button::new("File")
                        .min_size(egui::Vec2::new(60.0, 38.0));
                    if ui.add(file_btn).clicked() {
                        self.file_dropdown_visible = !self.file_dropdown_visible;
                        self.add_node_dropdown_visible = false;
                    }

                    let add_btn = egui::Button::new("Add Node")
                        .min_size(egui::Vec2::new(80.0, 38.0));
                    if ui.add(add_btn).clicked() {
                        self.add_node_dropdown_visible = !self.add_node_dropdown_visible;
                        self.file_dropdown_visible = false;
                    }

                    let help_btn = egui::Button::new("Help")
                        .min_size(egui::Vec2::new(55.0, 38.0));
                    if ui.add(help_btn).clicked() {
                        println!("Help clicked!");
                    }

                    ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                        let img_data = macroquad::prelude::Image::from_file_with_format(
                            &std::fs::read(TRASH_ICON).expect("Failed to read trash icon"),
                            Some(image::ImageFormat::Png),
                        );
                        let raw_bytes: Vec<u8> = img_data
                            .get_image_data()
                            .iter()
                            .flat_map(|pixel| pixel.to_vec())
                            .collect();
                        let color_img = egui::ColorImage::from_rgba_unmultiplied(
                            [img_data.width() as usize, img_data.height() as usize],
                            &raw_bytes,
                        );
                        let trash_texture = ctx.load_texture("trash", color_img, egui::TextureOptions::default());
                    
                        let trash_response = ui.add(
                            egui::ImageButton::new(trash_texture.id(), egui::Vec2::new(15.0, 15.0))
                        );
                        
                        if trash_response.clicked() {
                            self.pending_delete = true;
                        }
                    
                    });
                });
            });

        // --- File Dropdown ---
        if self.file_dropdown_visible {
            egui::Window::new("File")
                .fixed_pos(egui::pos2(0.0, 42.5))
                .collapsible(false)
                .resizable(false)
                .title_bar(false)
                .auto_sized()
                .frame(egui::Frame {
                    inner_margin: egui::Margin::same(0.0),
                    outer_margin: egui::Margin::same(0.0),
                    rounding: egui::Rounding::same(0.0),
                    shadow: egui::epaint::Shadow::NONE,
                    fill: egui_rgb(VULCAN),
                    stroke: egui::Stroke::new(1.0, egui_rgb(WATER_OUZEL)),
                })
                .show(ctx, |ui| {
                    let width = 120.0;
                    ui.set_width(width);
                    ui.spacing_mut().item_spacing = egui::Vec2::new(0.0, 0.0);
                    ui.spacing_mut().button_padding = egui::Vec2::new(0.0, 6.0);
                    for item in &["New", "Save", "Load"] {
                        let response = ui.add_sized(
                            egui::Vec2::new(width, 28.0),
                            egui::Button::new(
                                egui::RichText::new(*item).size(14.0)
                            )
                            
                        );
                        if response.clicked() {
                            match *item {
                                "New" => self.pending_file_action = Some(FileAction::New),
                                "Save" => self.pending_file_action = Some(FileAction::Save),
                                "Load" => self.pending_file_action = Some(FileAction::Load),
                                _ => {}
                            }
                            self.file_dropdown_visible = false;
                        }
                    }
                });
        }

        // --- Add Node Dropdown ---
        if self.add_node_dropdown_visible {
            egui::Window::new("Add Node")
                .fixed_pos(egui::pos2(65.0, 42.5))
                .collapsible(false)
                .resizable(false)
                .title_bar(false)
                .auto_sized()
                .frame(egui::Frame {
                    inner_margin: egui::Margin::same(0.0),
                    outer_margin: egui::Margin::same(0.0),
                    rounding: egui::Rounding::same(0.0),
                    shadow: egui::epaint::Shadow::NONE,
                    fill: egui_rgb(VULCAN),
                    stroke: egui::Stroke::new(1.0, egui_rgb(WATER_OUZEL)),
                })
                .show(ctx, |ui| {
                    let width = 175.0;
                    ui.set_width(width);
                    ui.spacing_mut().item_spacing = egui::Vec2::new(0.0, 0.0);
                    ui.spacing_mut().button_padding = egui::Vec2::new(0.0, 6.0);

                    let node_types = [
                        "Person (Male)", "Person (Female)", "Organization",
                        "Email", "Phone", "Document", "Database",
                        "Social Media", "Location", "Device"
                    ];
                    for node_type in node_types {
                        let response = ui.add_sized(
                            egui::Vec2::new(width, 28.0),
                            egui::Button::new(
                                egui::RichText::new(node_type).size(14.0)
                            )
                        );

                        if response.clicked() {
                            self.selected_entity_type = Some(match node_type {
                                "Person (Male)" => EntityType::PersonMale,
                                "Person (Female)" => EntityType::PersonFemale,
                                "Organization" => EntityType::Organization,
                                "Email" => EntityType::Email,
                                "Phone" => EntityType::Phone,
                                "Document" => EntityType::Document,
                                "Database" => EntityType::Database,
                                "Social Media" => EntityType::SocialMedia,
                                "Location" => EntityType::Location,
                                "Device" => EntityType::Device,
                                _ => return,
                            });
                            self.add_node_dropdown_visible = false;
                        }
                    }
                });
        }
    }
}