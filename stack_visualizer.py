# stack_visualizer.py

import streamlit as st

def initialize_state(keys_and_defaults):
    """A helper function to initialize session state keys."""
    for key, default_value in keys_and_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def run():
    """Runs the Streamlit UI for the Stack visualizer."""
    st.subheader("Stack Visualizer")
    initialize_state({'stack': []})

    col1, col2 = st.columns([1, 2])

    # --- Controls Column ---
    with col1:
        st.write("### Controls")
        value_to_push = st.text_input("Value to Push", key="stack_push_input", help="Enter a value and click 'Push'")
        
        if st.button("Push", use_container_width=True):
            if value_to_push:
                st.session_state.stack.append(value_to_push)
            else:
                st.warning("Please enter a value to push.")

        if st.button("Pop", use_container_width=True, disabled=not st.session_state.stack):
            popped_value = st.session_state.stack.pop()
            st.success(f"Popped: {popped_value}")
        
        if st.button("Clear Stack", use_container_width=True):
            st.session_state.stack.clear()
            st.rerun()

    # --- Visualization Column ---
    with col2:
        st.write("### Current Stack")
        if not st.session_state.stack:
            st.info("Stack is empty.")
        else:
            container = st.container(border=True)
            # Display stack with the top element highlighted
            for i, item in enumerate(reversed(st.session_state.stack)):
                if i == 0:  # Top of the stack
                    container.markdown(f"<div style='padding: 10px; margin: 5px; border: 2px solid #3498DB; border-radius: 5px; text-align: center; background-color: #AED6F1;'>{item} &nbsp; <b>(Top)</b></div>", unsafe_allow_html=True)
                else:
                    container.markdown(f"<div style='padding: 10px; margin: 5px; border: 1px solid #BDC3C7; border-radius: 5px; text-align: center;'>{item}</div>", unsafe_allow_html=True)
