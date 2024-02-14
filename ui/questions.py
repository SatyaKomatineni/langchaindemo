

from baselib import baselog as log
from collections import OrderedDict

class Question:
    def __init__(self, id, brief_description, full_description, answer=None):
        self.id = id
        self.brief_description = brief_description
        self.full_description = full_description
        self.answer = answer

    def addAnswer(self, answer):
        """Sets the answer for the question."""
        self.answer = answer


class QuestionRepo:
    def __init__(self):
        self.questions = OrderedDict()

    def addQuestion(self, question):
        """Adds a Question object to the questions dictionary."""
        self.questions[question.id] = question

    def clear(self):
        """Empties the questions dictionary."""
        self.questions.clear()

    def getQuestionList(self):
        """Returns a list of questions in the order they were inserted."""
        return list(self.questions.values())

    def getQuestion(self, question_id):
        """Returns the question for the given question_id, or None if not found."""
        return self.questions.get(question_id)

def test_question_repo():
    # Create Question instances
    question1 = Question(1, "Brief description 1", "Full description 1")
    question2 = Question(2, "Brief description 2", "Full description 2", "Answer 2")
    question3 = Question(3, "Brief description 3", "Full description 3")
    
    # Create a QuestionRepo instance and add questions
    repo = QuestionRepo()
    repo.addQuestion(question1)
    repo.addQuestion(question2)
    repo.addQuestion(question3)
    
    # Test adding and retrieving questions
    assert len(repo.getQuestionList()) == 3, "Should contain 3 questions"
    assert repo.getQuestion(2) == question2, "Should retrieve question 2 correctly"
    
    # Test getQuestionList() returns questions in the order they were inserted
    questions = repo.getQuestionList()
    assert questions[0].id == 1 and questions[1].id == 2 and questions[2].id == 3, "Questions should be in insertion order"
    
    # Test clear method
    repo.clear()
    assert len(repo.getQuestionList()) == 0, "Repo should be empty after clear"

    print("All tests passed!")

def localTest():
    log.ph1("Starting local test")
    test_question_repo()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()