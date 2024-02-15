from baselib import baselog as log

import streamlit as st
from ui.ui_state import ApplicationState
import ui.question_utils as qutils

from ui import html_utils as html

from ui.wizard import Wizard
from ui.WizardServices import WizardServices

from ui.questions import (
    Question,
    QuestionRepo
)
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
    st.title("Exploring State of the Union")

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
#* Approach 2
#*************************************************
#"""
def initialize_state2():
    writeIntro()

def writeOutput2():
    # Display the accumulated text
    html.writeNote("Note: Due to rate limitations there is an artificial delay in answering the question from the LLM. Sorry for the inonvenience. Thanks for your patience.")
    for line in reversed(appState.log_messages):
        #st.write(line)
        st.markdown(line,unsafe_allow_html=True)

def process_input2(input_text):
    wizard = WizardServices.getWizard()
    q, a = wizard.question(input_text)
    message = constructAnAnswer(q,a)
    appState.addMessage(message)

def constructAnAnswer(question: str, answer: str):
    return f"<h3>{question}</h3>\n\n<p>{answer}</p>"

def addQuestionToDB(text_input):
    addAQuestion(text_input)


def addAQuestion(question:str):
    appState.questionRepo.addStringAsQuestion(question)

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

def getQuestionFromParams() -> Question | None :
    query_params = st.query_params
    question_id = query_params.get("question")
    if not question_id:
        return None
    id: str = question_id.strip()
    return appState.questionRepo.getQuestion(int(id))

def getQuestionTextFromParams() -> str:
    question = getQuestionFromParams()
    if not question:
        return ""
    #question is there
    return question.full_description

def creaeSidebar():
    with st.sidebar:
        # Use HTML to create links and Markdown to render them
        st.markdown("""
            # Menu Items
            - [item1](/?arg1='item1')
            - [item2](/?arg1='item2')
            - [item3](/?arg1='item3')
        """, unsafe_allow_html=True)

def creaeSidebarQuestionMenu():
    with st.sidebar:
        # Use HTML to create links and Markdown to render them
        menustr = qutils.getQuestionMenu(appState.questionRepo)
        st.markdown(menustr, unsafe_allow_html=True)

#"""
#*************************************************
#* Main function
#*************************************************
#"""
def main():
    """Main function to render the Streamlit page."""
    initialize_state2()

    # Create a form
    with st.form(key='input_form'):
        #Question text
        questionText = getQuestionTextFromParams()
        log.trace(f"Question text:{questionText}")
        if questionText == "":
            text_input = st.text_input("Enter your question")
        else:
            text_input = st.text_input("Enter your question", value=questionText)

        #Go after the buttons
        col1, col2, col3 = st.columns([0.2,0.2,0.6], gap="small")
        with col1:
            submit_button = st.form_submit_button("Submit")
        with col2:
            clear_button = st.form_submit_button("Clear text", on_click=lambda: clearLog2())
        with col3:
            add_question_button = st.form_submit_button("Add the question to db")

    # Process the form submission
    if submit_button and text_input:
        process_input2(text_input)
    if clear_button:
        clearLog2()
    if add_question_button:
        addQuestionToDB(text_input)

    queryParams()
    creaeSidebarQuestionMenu()
    writeOutput2()
    saveState()

#Kick it off
main()