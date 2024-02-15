
from baselib import baselog as log
from ui.ui_state import ApplicationState

from ui.questions import (
    Question,
    QuestionRepo
)

def _getMenuItem(question: Question):
     # - [item1](/?arg1='item1')
    name = question.brief_description
    id = question.id
    mi = f"1. [{name}](/?question={id})"
    return mi

def getQuestionMenu(questionRepo: QuestionRepo):
    menuStr = f"# Questions"
    qr = questionRepo
    qlist = qr.getQuestionList()
    for item in qlist:
        question: Question = item
        qurl = _getMenuItem(question)
        menuStr = f"{menuStr}\n{qurl}"
    return menuStr


def _getMenuItemHtml(question: Question):
     # - [item1](/?arg1='item1')
    name = question.brief_description
    id = question.id
    mi = f"<li><a href='/?question={id}' target='_self'>{name}</a></li>"
    return mi

def getQuestionMenu2(questionRepo: QuestionRepo):
    menuStr = f"<h3>Questions</h3>\n<ol>"
    qr = questionRepo
    qlist = qr.getQuestionList()
    for item in qlist:
        question: Question = item
        qurl = _getMenuItemHtml(question)
        menuStr = f"{menuStr}\n{qurl}"
    menuStr = f"{menuStr}\n</ol>"
    return menuStr

def test():
    q = Question.getASampleQuestion()
    log.info(_getMenuItem(q))

def testMenu():
    qrepo = QuestionRepo.getSampleRepo()
    menu = getQuestionMenu(qrepo)
    log.ph("Menu",menu)

def localTest():
    log.ph1("Starting local test")
    testMenu()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()