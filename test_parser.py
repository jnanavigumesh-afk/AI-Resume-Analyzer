
from resume_parser import extract_resume_text
from text_cleaner import clean_text

# Replace this path with the path to your own resume.
resume_path = r"sample_resume.pdf"

try:
    extracted_text = extract_resume_text(resume_path)
    cleaned_text = clean_text(extracted_text)

    print("\n--- EXTRACTED RESUME TEXT ---")
    print(extracted_text[:1000])

    print("\n--- CLEANED RESUME TEXT ---")
    print(cleaned_text[:1000])

    print("\nResume parsing test completed successfully.")

except (FileNotFoundError, ValueError) as error:
    print("Error:", error)
