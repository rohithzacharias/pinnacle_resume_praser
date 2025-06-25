import customtkinter as ctk
from tkinter import filedialog, messagebox
import re
import spacy
import pickle
from parser import extract_raw_text

# Load NER model for extracting name
nlp = spacy.load('en_core_web_sm')

# Load trained model
with open('model.pkl', 'rb') as f:
    vectorizer, mlb, model = pickle.load(f)

def format_parsed_data(text, predicted_labels):
    # NER to extract name
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    name = names[0] if names else "N/A"

    # Extract emails & phones
    emails = re.findall(r'\S+@\S+\.\S+', text)
    phones = re.findall(r'\+?\d[\d -]{8,}\d', text)

    # Extract skills and education based on labels
    skills = []
    education = []
    for label in predicted_labels:
        label_lower = label.lower()
        if label_lower == 'skills':
            skill_list = ['Python', 'Java', 'C++', 'ML', 'Data Analysis', 'Communication', 'Problem-Solving', 'Leadership']
            skills = [s for s in skill_list if s.lower() in text.lower()]
        elif label_lower == 'education':
            education_keywords = ['B.Tech', 'BSc', 'M.Tech', 'MSc', 'PhD', 'MBA', 'University', 'College', 'Degree']
            education = [e for e in education_keywords if e.lower() in text.lower()]

    # Always attempt to extract certifications
    certifications = []
    cert_match = re.search(
        r'Certifications:\s*(.*?)\n\s*\n|Certifications:\s*(.*)$',
        text,
        flags=re.IGNORECASE | re.DOTALL
    )
    if cert_match:
        cert_text = cert_match.group(1) if cert_match.group(1) else cert_match.group(2)
        certifications = re.split(r'\n|-|,', cert_text)
        certifications = [c.strip() for c in certifications if c.strip()]

    return f"""==============================
👤 Name: {name}
✉️ Email(s): {', '.join(emails) if emails else 'N/A'}
📞 Phone(s): {', '.join(phones) if phones else 'N/A'}
💡 Skills: {', '.join(skills) if skills else 'N/A'}
🎓 Education: {', '.join(education) if education else 'N/A'}
🏆 Certifications: {', '.join(certifications) if certifications else 'N/A'}
==============================
"""

# UI setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📄 AI Resume Parser")
app.geometry("600x550")

title_label = ctk.CTkLabel(
    app,
    text="📄 AI Resume Parser",
    font=ctk.CTkFont(size=24, weight="bold")
)
title_label.pack(pady=10)

output_textbox = ctk.CTkTextbox(app, width=550, height=300, corner_radius=8)
output_textbox.pack(pady=10)

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Resume files", "*.pdf;*.docx")]
    )
    if file_path:
        try:
            text = extract_raw_text(file_path)
            # Predict labels
            X = vectorizer.transform([text])
            predicted = model.predict(X)
            labels = mlb.inverse_transform(predicted)[0]

            output_textbox.delete("1.0", "end")
            output_textbox.insert(
                "end",
                format_parsed_data(text, labels)
            )
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

def clear_output():
    output_textbox.delete("1.0", "end")

browse_button = ctk.CTkButton(
    app,
    text="Browse Resume",
    command=browse_file,
    width=200,
    height=40,
    corner_radius=8
)
browse_button.pack(pady=10)

clear_button = ctk.CTkButton(
    app,
    text="Clear Output",
    command=clear_output,
    width=200,
    height=40,
    corner_radius=8,
    fg_color="red",
    hover_color="darkred"
)
clear_button.pack(pady=5)

app.mainloop()
# This script provides a GUI for parsing resumes using a trained model and displays the parsed information.