from backend.autofill.autofill_manager import AutofillManager
def test_autofill_manager_uses_provided_engine():
    class FakeEngine:
        def __init__(self):
            self.fill_form_was_called = False
            self.last_data = None

        def fill_form(self, data: dict):
            self.fill_form_was_called = True
            self.last_data = data
    
    # Arrange
    mock_engine = FakeEngine()
    application_data = {
        "name": "Test User",
        "email": "test.user@example.com",
        "skills": ["iOS Development", "Swift", "SwiftUI"]
    }

    manager = AutofillManager(engine=mock_engine)
   
    # Act
    manager.autofill(application_data)

    # Assert
    assert mock_engine.fill_form_was_called == True
    assert mock_engine.last_data == application_data
