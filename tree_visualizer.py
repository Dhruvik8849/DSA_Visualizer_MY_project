# tree_visualizer.py

import streamlit as st
from graphviz import Digraph

# --- Helper Class and Functions ---

class Node:
    """A node in a binary search tree for visualization."""
    def __init__(self, key):
        self.key = int(key)
        self.left = None
        self.right = None

def initialize_state(keys_and_defaults):
    """A helper function to initialize session state keys."""
    for key, default_value in keys_and_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def insert_recursive(node, key):
    """Recursively inserts a key into the BST."""
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert_recursive(node.left, key)
    elif key > node.key:
        node.right = insert_recursive(node.right, key)
    else:
        st.warning(f"Value {key} already exists in the tree.")
    return node

def build_graphviz_tree(dot, node):
    """Recursively builds the Graphviz tree representation."""
    if node is not None:
        dot.node(str(node.key), str(node.key), shape='circle', style='filled', fillcolor='#9B59B6', fontcolor='white')
        if node.left:
            dot.edge(str(node.key), str(node.left.key))
            build_graphviz_tree(dot, node.left)
        if node.right:
            dot.edge(str(node.key), str(node.right.key))
            build_graphviz_tree(dot, node.right)

# --- Main Run Function ---

def run():
    """Runs the Streamlit UI for the BST visualizer."""
    st.subheader("Binary Search Tree Visualizer")
    initialize_state({'bst_root': None})

    col1, col2 = st.columns([1, 2])

    # --- Controls Column ---
    with col1:
        st.write("### Controls")
        value_to_insert = st.text_input("Value to Insert (integer)", key="bst_insert_input")
        
        if st.button("Insert", use_container_width=True):
            if value_to_insert:
                try:
                    key = int(value_to_insert)
                    st.session_state.bst_root = insert_recursive(st.session_state.bst_root, key)
                except ValueError:
                    st.error("Please enter a valid integer.")
            else:
                st.warning("Please enter a value to insert.")
        
        if st.button("Clear Tree", use_container_width=True):
            st.session_state.bst_root = None
            st.rerun()

    # --- Visualization Column ---
    with col2:
        st.write("### Tree Visualization")
        if st.session_state.bst_root is None:
            st.info("Tree is empty. Insert a value to begin.")
        else:
            dot = Digraph()
            dot.attr('node', shape='circle')
            build_graphviz_tree(dot, st.session_state.bst_root)
            st.graphviz_chart(dot)
