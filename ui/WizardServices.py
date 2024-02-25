
from ui.wizard import (
    Wizard,
    FakeWizard
)
from ui.LangChainHFWizard import LangChainHFWizard
from ui.LangChainHFWizard2 import LangChainHFWizard2

class WizardServices():
    class_wizard: Wizard = FakeWizard()
    class_real_wizard: Wizard = LangChainHFWizard()
    class_wizard2: Wizard = LangChainHFWizard2()

    @staticmethod
    def getWizard() -> Wizard:
        return WizardServices.class_wizard2
    
    @staticmethod
    def getFakeWizard() -> Wizard:
        return WizardServices.class_wizard
    
    @staticmethod
    def getRealWizard() -> Wizard:
        return WizardServices.class_real_wizard
