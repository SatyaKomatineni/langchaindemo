
from ui.wizard import (
    Wizard,
    FakeWizard
)
from ui.LangChainHFWizard import LangChainHFWizard

class WizardServices():
    class_wizard: Wizard = FakeWizard()
    class_real_wizard: Wizard = LangChainHFWizard()

    @staticmethod
    def getWizard() -> Wizard:
        return WizardServices.class_real_wizard
    
    @staticmethod
    def getFakeWizard() -> Wizard:
        return WizardServices.class_wizard
    
    @staticmethod
    def getRealWizard() -> Wizard:
        return WizardServices.class_real_wizard
