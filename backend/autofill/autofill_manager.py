class AutofillManager:
    def __init__(self, engine):
        self.engine = engine
    
    def autofill(self, application_data: dict):
        self.engine.fill_form(application_data)