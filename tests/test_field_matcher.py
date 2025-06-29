from backend.autofill.field_matcher import match_label_to_key

def test_match_label_to_resume_key():
    assert match_label_to_key("Full Name") == "name"
    assert match_label_to_key("E-Mail Address") == "email"
    assert match_label_to_key("Skillset") == "skills"
    assert match_label_to_key("Phone Number") == "phone"
    assert match_label_to_key("   FULL   name   ") == "name"
    assert match_label_to_key("contact-email!") == "email"
    assert match_label_to_key("Random Unmatched Label") is None
    
def test_rule_matching_full_name():
    assert match_label_to_key("Full Name") == "name"
    
def test_rule_matching_linkedin_profile():
    assert match_label_to_key("Linkedin Profile") == "linkedin"

def test_rule_matching_upload_resume():
    assert match_label_to_key("Resume/CV") == "resume"
    
def test_fuzzy_matching_contact_email():
    assert match_label_to_key("Contct Email") == "email"