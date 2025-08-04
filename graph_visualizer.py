# graph_visualizer.py

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def initialize_state(keys_and_defaults):
    """A helper function to initialize session state keys."""
    for key, default_value in keys_and_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def draw_graph():
    """Draws the graph using Matplotlib."""
    G = st.session_state.graph
    pos = st.session_state.node_positions
    
    # Recalculate positions only if the set of nodes changes
    if set(pos.keys()) != set(G.nodes()):
        pos = nx.spring_layout(G, seed=42)
        st.session_state.node_positions = pos

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#0E1117') # Match Streamlit dark theme background
    ax.set_facecolor('#0E1117')

    # Determine node colors based on traversal state
    traversal_nodes = st.session_state.traversal_result
    node_colors = []
    for node in G.nodes():
        if node in traversal_nodes:
            node_colors.append('#2ECC71') # Green for visited
        else:
            node_colors.append('#3498DB') # Blue for default

    nx.draw(G, pos, ax=ax, with_labels=True,
            node_color=node_colors, node_size=800,
            font_color='white', font_size=12, font_weight='bold',
            edge_color='gray', width=2.0)
    
    st.pyplot(fig)

def run():
    """Runs the Streamlit UI for the Graph visualizer."""
    st.subheader("Graph Traversal Visualizer")
    
    initialize_state({
        'graph': nx.Graph(),
        'node_positions': {},
        'traversal_result': []
    })

    # --- UI Controls Layout ---
    st.write("### Controls")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.write("**Add Elements**")
        node_to_add = st.text_input("Node Name", key="graph_node_input")
        if st.button("Add Node", use_container_width=True):
            if node_to_add and node_to_add not in st.session_state.graph:
                st.session_state.graph.add_node(node_to_add)
                st.session_state.traversal_result = []
                st.rerun()
            elif not node_to_add:
                st.warning("Please enter a node name.")
            else:
                st.warning(f"Node '{node_to_add}' already exists.")

        edge_u = st.text_input("From Node (u)", key="graph_edge_u")
        edge_v = st.text_input("To Node (v)", key="graph_edge_v")
        if st.button("Add Edge", use_container_width=True):
            if edge_u and edge_v:
                if edge_u in st.session_state.graph and edge_v in st.session_state.graph:
                    st.session_state.graph.add_edge(edge_u, edge_v)
                    st.session_state.traversal_result = []
                    st.rerun()
                else:
                    st.error("Both nodes must exist in the graph.")
            else:
                st.warning("Please enter both nodes for the edge.")

    with c2:
        st.write("**Run Traversal**")
        nodes_list = list(st.session_state.graph.nodes())
        start_node = st.selectbox("Start Node", options=nodes_list, index=0 if nodes_list else None)

        if st.button("Run BFS", disabled=not start_node, use_container_width=True):
            bfs_nodes = list(nx.bfs_nodes(st.session_state.graph, source=start_node))
            st.session_state.traversal_result = bfs_nodes
            st.rerun()

        if st.button("Run DFS", disabled=not start_node, use_container_width=True):
            dfs_nodes = list(nx.dfs_nodes(st.session_state.graph, source=start_node))
            st.session_state.traversal_result = dfs_nodes
            st.rerun()

    with c3:
        st.write("**Manage Graph**")
        if st.button("Clear Traversal Result", use_container_width=True):
            st.session_state.traversal_result = []
            st.rerun()

        if st.button("Clear Entire Graph", type="primary", use_container_width=True):
            st.session_state.graph.clear()
            st.session_state.node_positions = {}
            st.session_state.traversal_result = []
            st.rerun()

    # --- Visualization Area ---
    st.markdown("---")
    st.write("### Graph Visualization")
    if not st.session_state.graph.nodes():
        st.info("Graph is empty. Add nodes and edges to begin.")
    else:
        draw_graph()
        if st.session_state.traversal_result:
            st.success("**Traversal Order:** " + " → ".join(map(str, st.session_state.traversal_result)))
