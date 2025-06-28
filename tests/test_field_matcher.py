from backend.autofill.field_matcher import match_label_to_key
    
def test_rule_matching_full_name():
    assert match_label_to_key("Full Name") == "name"
    
def test_rule_matching_linkedin_profile():
    assert match_label_to_key("Linkedin Profile") == "linkedin"

def test_rule_matching_upload_resume():
    assert match_label_to_key("Resume/CV") == "resume"