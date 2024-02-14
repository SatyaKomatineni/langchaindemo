
import streamlit as st
from ui.ui_state import ApplicationState

#
#**************************************************
# Key elements
# 1. A form with a submit
# 2. Process text input
# 3. Write back what is entered so far
# 4. Rememebers with each web refresh the state
#**************************************************
#
def writeIntro():
    # Streamlit page layout
    st.title("Demo page")

    st.write("hello there")
    st.write("hello there")
    st.write("hello there")

#"""
#************************************************
#* Manage state
#*************************************************
#"""
appState =  ApplicationState.restore()

def saveState():
    appState.save()

#"""
#*************************************************
#* Approach 1
#*************************************************
#"""
def initialize_state1():
    writeIntro()
    
    """Initialize the state variable."""
    if 'totalResponseText' not in st.session_state:
        st.session_state.totalResponseText = []

def writeOutput1():
    # Display the accumulated text
    st.write("Accumulated Text:")
    for line in st.session_state.totalResponseText:
        st.write(line)

def process_input1(input_text):
    """Append the input text to the totalResponseText state variable."""
    st.session_state.totalResponseText.append(input_text)

def addToLog1(text: str):
    st.session_state.totalResponseText.append(text)

def clearLog1():
    st.session_state.totalResponseText.clear()

#"""
#*************************************************
#* Approach 2
#*************************************************
#"""
def initialize_state2():
    writeIntro()
    
def writeOutput2():
    # Display the accumulated text
    st.write("Accumulated Text:")
    for line in appState.log_messages:
        st.write(line)

def process_input2(input_text):
    """Append the input text to the totalResponseText state variable."""
    appState.addMessage(input_text)

def addToLog2(text: str):
    appState.addMessage(text)

def clearLog2():
    appState.clear()

def saveState2():
    appState.save()


#"""
#*************************************************
#* Approach 2: end
#*************************************************
#"""
def queryParams():
    query_params = st.query_params
    arg1 = query_params.get("arg1")  
    if arg1:
        addToLog2(arg1)

def creaeSidebar():
    with st.sidebar:
        # Use HTML to create links and Markdown to render them
        st.markdown("""
            # Menu Items
            - [item1](/?arg1='item1')
            - [item2](/?arg1='item2')
            - [item3](/?arg1='item3')
        """, unsafe_allow_html=True)

def main():
    """Main function to render the Streamlit page."""
    initialize_state2()

    # Create a form
    with st.form(key='input_form'):
        text_input = st.text_input("Enter your text")
        col1, col2, col3 = st.columns([0.2,0.2,0.6], gap="small")
        with col1:
            submit_button = st.form_submit_button("Submit")
        with col2:
            st.form_submit_button("Clear text", on_click=lambda: clearLog2())

    # Process the form submission
    if submit_button and text_input:
        process_input2(text_input)

    queryParams()
    creaeSidebar()
    writeOutput2()
    saveState()

#Kick it off
main()