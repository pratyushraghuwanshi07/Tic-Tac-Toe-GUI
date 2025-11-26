import streamlit as st
# Paste your entire Tic-Tac-Toe code here, but replace:
#   root = Tk()  →  st.set_page_config(layout="centered")
#   root.mainloop() → remove it
# Add this at the very top:
st.title("Tic-Tac-Toe")

# Your existing game code goes here (just indent properly)
# Example quick fix for Tkinter → use streamlit components instead, or:
# If you’re using Pygame, use pygame-streamlit (5 lines):
# pip install pygame-streamlit
from pygame_streamlit import pygame_embed
pygame_embed("tic_tac_toe_gui.py")  # or embed your logic directly