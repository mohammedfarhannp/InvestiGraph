# InvestiGraph
An investigation graph tool built with Pygame — visualize and connect entities like people, organizations, emails, phones, documents, databases, and social media accounts.

## Screenshots

![InvestiGraph in action](https://github.com/mohammedfarhannp/InvestiGraph/blob/master/assets/screenshots/Screenshot%202.png)


## Features

- **8 Entity Types** — Person (Male/Female), Organization, Email, Phone, Document, Database, Social Media
- **Visual Graph** — Drag nodes, create directed edges, pan/zoom canvas
- **Properties Panel** — Edit labels, properties, and multi-line notes for each node
- **Edge Labels** — Name your relationships
- **Save/Load** — Native `.investigraph` file format
- **Unsaved Changes Tracking** — Never lose work
- **Zoom-Responsive UI** — Everything scales smoothly

## Controls

| Action | Control |
|--------|---------|
| Pan canvas | Left-click + drag (empty space) |
| Zoom | Scroll wheel |
| Select node/edge | Left-click |
| Move node | Click + drag selected node |
| Create edge | Right-click source node → move mouse → right-click target node |
| Delete selection | Delete key or trash icon |
| Add node | Click "Add Node" → choose type → click on canvas |

## File Menu

- **New** — Clear current graph (prompts to save if unsaved)
- **Save** — Save to `.investigraph` file
- **Load** — Load from `.investigraph` file

## Installation

```bash
git clone https://github.com/mohammedfarhannp/InvestiGraph.git
cd InvestiGraph
pip install -r requirements.txt
python main.py
```

## Requirements

- Python 3.8+
- Pygame 2.5+
- tkinter (included with Python)

## Project Structure

```
InvestiGraph/
├── core/           # Node, Edge classes
├── entities/       # Entity types (Person, Email, etc.)
├── ui/             # Canvas, Camera, Ribbon, Properties Panel
├── utils/          # File I/O helpers
├── assets/icons/   # 24x24 PNG icons
├── saves/          # Default save location
├── main.py
└── settings.py
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Author
Mohammed Farhan N P

