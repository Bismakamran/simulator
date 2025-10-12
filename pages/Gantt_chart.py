import streamlit as st
import streamlit.components.v1 as components

# Load HTML content from file
with open("graphical.html", "r") as f:
    html_content = f.read()

# Render HTML in Streamlit
components.html(html_content, height=1000)
