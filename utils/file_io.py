import json
import os
import pygame

from entities import *
from tkinter import filedialog
from core.edge import Edge

def save_graph(nodes, edges, camera):
    # Ask for file location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".investigraph",
        filetypes=[("InvestiGraph files", "*.investigraph"), ("All files", "*.*")]
    )
    
    if not file_path:
        return False
    
    # Prepare data
    data = {
        "version": "1.0",
        "camera": {
            "x": camera.x,
            "y": camera.y,
            "zoom": camera.zoom
        },
        "nodes": [],
        "edges": []
    }
    
    # Save nodes
    for node in nodes:
        node_data = {
            "id": node.id,
            "type": node.node_type,
            "label": node.label,
            "x": node.x,
            "y": node.y,
            "properties": node.properties if hasattr(node, 'properties') else {},
            "notes": node.notes if hasattr(node, 'notes') else ""
        }
        
        # Add gender for Person nodes
        if hasattr(node, 'gender'):
            node_data["gender"] = node.gender
        
        data["nodes"].append(node_data)
    
    # Save edges
    for edge in edges:
        edge_data = {
            "id": edge.id,
            "source_id": edge.source.id,
            "target_id": edge.target.id,
            "label": edge.label
        }
        data["edges"].append(edge_data)
    
    # Write file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return True

def load_graph(canvas):
    # Ask for file location
    file_path = filedialog.askopenfilename(
        filetypes=[("InvestiGraph files", "*.investigraph"), ("All files", "*.*")]
    )
    
    if not file_path:
        return False
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Clear current graph
    canvas.graph.nodes.clear()
    canvas.graph.edges.clear()
    canvas.selected_node = None
    canvas.selected_edge = None
    
    # Restore camera
    if "camera" in data:
        canvas.camera.x = data["camera"]["x"]
        canvas.camera.y = data["camera"]["y"]
        canvas.camera.zoom = data["camera"]["zoom"]
    
    # Dictionary to map saved ids to new node objects
    node_map = {}
    
    entity_classes = {
        "Person": Person,
        "Email": Email,
        "Phone": Phone,
        "Organization": Organization,
        "Document": Document,
        "Database": Database,
        "SocialMedia": SocialMedia,
        "Location":Location,
        "Device":Device
    }
    
    # Create nodes
    for node_data in data["nodes"]:
        node_type = node_data["type"]
        node_class = entity_classes.get(node_type)
        
        if node_class:
            if node_type == "Person":
                gender = node_data.get("gender", "male")
                new_node = node_class(node_data["id"], node_data["label"], 
                                     node_data["x"], node_data["y"], gender)
            else:
                new_node = node_class(node_data["id"], node_data["label"],
                                     node_data["x"], node_data["y"])
            
            # Restore properties
            if hasattr(new_node, 'properties'):
                new_node.properties.update(node_data.get("properties", {}))
            
            # Restore notes
            new_node.notes = node_data.get("notes", "")
            
            canvas.graph.nodes.append(new_node)
            node_map[node_data["id"]] = new_node
    
    # Create edges
    
    for edge_data in data["edges"]:
        source = node_map.get(edge_data["source_id"])
        target = node_map.get(edge_data["target_id"])
        
        if source and target:
            new_edge = Edge(edge_data["id"], source, target, edge_data["label"])
            canvas.graph.edges.append(new_edge)
    
    return True