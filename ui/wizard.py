
"""
*************************************************
* Imports
*************************************************
"""
from abc import ABC, abstractmethod
from typing import Tuple

"""
*************************************************
* Wizard interface
*************************************************
"""
class Wizard(ABC):
    #return a tuple
    @abstractmethod
    def question(self, question: str) -> Tuple[str, str]:
        pass

class FakeWizard(Wizard):
    def question(self, question: str):
        return (f"your question: {question}",f"Here is the fake answer to your question: {question}")


