use crate::core::graph::Graph;

const MAX_HISTORY_STATES: usize = 100;

pub struct GraphHistory {
    undo_stack: Vec<Graph>,
    redo_stack: Vec<Graph>,
}

impl GraphHistory {
    pub fn new() -> Self {
        Self {
            undo_stack: Vec::new(),
            redo_stack: Vec::new(),
        }
    }

    pub fn record(&mut self, graph: &Graph) {
        self.undo_stack.push(graph.clone());
        if self.undo_stack.len() > MAX_HISTORY_STATES {
            self.undo_stack.remove(0);
        }
        self.redo_stack.clear();
    }

    pub fn undo(&mut self, graph: &mut Graph) -> bool {
        if let Some(previous_graph) = self.undo_stack.pop() {
            self.redo_stack.push(graph.clone());
            *graph = previous_graph;
            graph.mark_changed();
            true
        } else {
            false
        }
    }

    pub fn redo(&mut self, graph: &mut Graph) -> bool {
        if let Some(next_graph) = self.redo_stack.pop() {
            self.undo_stack.push(graph.clone());
            *graph = next_graph;
            graph.mark_changed();
            true
        } else {
            false
        }
    }

}
