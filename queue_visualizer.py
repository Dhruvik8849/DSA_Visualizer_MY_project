# queue_visualizer.py

import streamlit as st

def initialize_state(keys_and_defaults):
    """A helper function to initialize session state keys."""
    for key, default_value in keys_and_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def run():
    """Runs the Streamlit UI for the Queue visualizer."""
    st.subheader("Queue Visualizer")
    initialize_state({'queue': []})

    col1, col2 = st.columns([1, 2])

    # --- Controls Column ---
    with col1:
        st.write("### Controls")
        value_to_enqueue = st.text_input("Value to Enqueue", key="queue_enqueue_input", help="Enter a value and click 'Enqueue'")
        
        if st.button("Enqueue", use_container_width=True):
            if value_to_enqueue:
                st.session_state.queue.append(value_to_enqueue)
            else:
                st.warning("Please enter a value to enqueue.")

        if st.button("Dequeue", use_container_width=True, disabled=not st.session_state.queue):
            dequeued_value = st.session_state.queue.pop(0)
            st.success(f"Dequeued: {dequeued_value}")

        if st.button("Clear Queue", use_container_width=True):
            st.session_state.queue.clear()
            st.rerun()

    # --- Visualization Column ---
    with col2:
        st.write("### Current Queue")
        if not st.session_state.queue:
            st.info("Queue is empty.")
        else:
            # Display queue horizontally
            container = st.container(border=True)
            with container:
                cols = st.columns(len(st.session_state.queue))
                for i, item in enumerate(st.session_state.queue):
                    label = ""
                    if i == 0:
                        label = " (Front)"
                    if i == len(st.session_state.queue) - 1:
                        label = " (Rear)"
                    cols[i].markdown(f"<div style='padding: 10px; margin: 2px; border: 2px solid #58D68D; border-radius: 5px; text-align: center;'>{item}{label}</div>", unsafe_allow_html=True)
