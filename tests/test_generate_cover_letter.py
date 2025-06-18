import os
from dotenv import load_dotenv
from backend.generator.services.generate_cover_letter import generate_cover_letter
from backend.generator.cover_letter_saver import save_cover_letter
load_dotenv()

resume_summary = """
Senior iOS Developer with 6+ years of experience building scalable, user-centric apps using Swift and SwiftUI. Led performance optimizations and modularization at companies like Groupon, Ford, and WillowTree (NBA App).
"""

job_description = """
We’re hiring a Mobile Engineer to join our team at Flock Safety. You’ll build new features in our iOS app using Swift, collaborate cross-functionally, and help us scale our engineering practices.
"""

user_notes = "Highlight experience with the NBA app and collaborative team environments."

if __name__ == "__main__":
    cover_letter = generate_cover_letter(resume_summary, job_description, user_notes)
    print("\n📄 Generated Cover Letter:\n")
    print(cover_letter)
    
    # Save it to a file
    path = save_cover_letter(cover_letter, job_title="Mobile Engineer", company="Flock Safety")
    print(f"\n✅ Cover letter saved to: {path}")

