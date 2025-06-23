from backend.generation.generate_cover_letter import generate_cover_letter_pdf

resume_summary = "Experienced iOS engineer with Swift, SwiftUI, and MVVM expertise."
job_description = "We're hiring a mobile engineer to lead iOS development on our next-gen app."
user_notes = "Mention excitement about health tech and experience with push notifications."

pdf_path = generate_cover_letter_pdf("cover_test", resume_summary, job_description, user_notes)
print(f"✅ Cover letter exported to: {pdf_path}")
