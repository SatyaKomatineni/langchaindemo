
import streamlit as st

# Using HTML with inline CSS to change text color
red_text_html = '<p style="color: red;">This text is red.</p>'

def sendToScreen(html: str):
    st.markdown(html, unsafe_allow_html=True)

def writeNote(text: str):
    note = f"<p style='color:red;'>{text}</p>"
    sendToScreen(note)
