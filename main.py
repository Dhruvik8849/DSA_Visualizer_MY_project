# main.py

import streamlit as st
import stack_visualizer
import queue_visualizer
import tree_visualizer
import graph_visualizer

# Set the page configuration for the app
st.set_page_config(page_title="DSA Visualizer", layout="wide")

# Main title for the application
st.title("Data Structures & Algorithms Visualizer 🚀")

# Sidebar for navigation between different visualizers
with st.sidebar:
    st.title("Visualizers")
    visualizer_option = st.selectbox(
        "Choose a data structure:",
        ("Stack", "Queue", "Binary Search Tree", "Graph")
    )
    st.markdown("---")
    st.info("Select a data structure from the dropdown menu to see its visualization and interact with it.")

# A dictionary to map options to their respective functions
visualizers = {
    "Stack": stack_visualizer.run,
    "Queue": queue_visualizer.run,
    "Binary Search Tree": tree_visualizer.run,
    "Graph": graph_visualizer.run
}

# Run the selected visualizer's function
if visualizer_option in visualizers:
    visualizers[visualizer_option]()
