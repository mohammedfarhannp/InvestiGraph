# InvestiGraph

A investigation graph tool for mapping relationships between entities. rebuilt with Rust that which is orginally built with python.

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)

## Overview

InvestiGraph allows investigators, analysts, and OSINT practitioners to visually map connections between people, organizations, devices, and other entities.

![InvestiGraph in Action](https://github.com/mohammedfarhannp/InvestiGraph/blob/master/assets/screenshots/Screenshot%201.png)

## Features

- **10 Entity Types**: Person (Male/Female), Organization, Email, Phone, Document, Database, Social Media, Location, Device
- **Interactive Graph**: Pan, zoom, drag nodes, create directed edges
- **Properties Panel**: Edit labels and notes for nodes and edges
- **Save/Load**: `.investigraph` JSON format with native file dialogs
- **Unsaved Changes Tracking**: Prompts before discarding work
- **Zoom-Responsive**: Nodes, icons, labels, edges, and arrowheads scale with zoom

## Controls

| Action | Control |
|--------|---------|
| Pan canvas | Left-click + drag (empty space) |
| Zoom | Scroll wheel (0.4x–2.0x) |
| Select node/edge | Left-click |
| Move node | Click + drag selected node |
| Create edge | Right-click source node → right-click target node |
| Delete selected | Delete key or trash icon |
| Add node | Add Node dropdown → choose type → click canvas |
| Save | File → Save |
| Load | File → Load |
| New | File → New |
| Cancel edge/placement | Escape |

## Entity Colors

| Entity | Color |
|--------|-------|
| Person (Male) | Blue |
| Person (Female) | Pink |
| Organization | Orange |
| Email | Green |
| Phone | Purple |
| Document | Yellow |
| Database | Gray |
| Social Media | Twitter Blue |
| Location | Teal |
| Device | Light Green |

## File Format

Saves use `.investigraph` extension (JSON internally). Includes:
- All nodes and edges
- Camera position and zoom
- Labels, notes, and properties

## Building

### Requirements
- Rust 1.70+
- Cargo

### Build & Run
```bash
cargo build --release
cargo run
```

## Dependencies

- [macroquad](https://crates.io/crates/macroquad) — Rendering
- [egui](https://crates.io/crates/egui) — UI framework
- [egui-macroquad](https://crates.io/crates/egui-macroquad) — egui + macroquad integration
- [serde](https://crates.io/crates/serde) + [serde_json](https://crates.io/crates/serde_json) — Serialization
- [rfd](https://crates.io/crates/rfd) — Native file dialogs
- [image](https://crates.io/crates/image) — Icon loading

## Project Structure

```
src/
├── main.rs              # Entry point, render loop, input handling
├── settings.rs          # Constants, colors, paths
├── core/
│   ├── node.rs          # Node struct, entity types
│   ├── edge.rs          # Edge struct
│   ├── graph.rs         # Graph state management
│   └── mod.rs
├── ui/
│   ├── ribbon.rs        # Top toolbar (File, Add Node, Help, Trash)
│   ├── properties_panel.rs  # Right-side panel for editing
│   ├── camera.rs        # Pan/zoom camera
│   └── mod.rs
└── utils/
    ├── assets.rs        # Icon texture loading
    ├── file_io.rs       # Save/Load operations
    └── mod.rs
```

## License

GNU General Public License v3.0

## Platform Support

- [x] Windows
- [ ] Linux
- [ ] macOS