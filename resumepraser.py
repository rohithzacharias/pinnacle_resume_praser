import customtkinter as ctk
from tkinter import filedialog, messagebox
import re
import spacy
import pickle
from parser import extract_raw_text

# Load NER model for name
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

    # Extract sections based on labels
    skills = []
    education = []
    certifications = []
    for label in predicted_labels:
        if label.lower() == 'skills':
            # Just a simple keyword list
            skill_list = ['Python', 'Java', 'C++', 'ML', 'Data Analysis', 'Communication']
            skills = [s for s in skill_list if s.lower() in text.lower()]
        elif label.lower() == 'education':
            education_keywords = ['B.Tech', 'BSc', 'M.Tech', 'MSc', 'PhD', 'MBA']
            education = [e for e in education_keywords if e.lower() in text.lower()]
        elif label.lower() == 'certifications':
            # Dummy certification list
            certs_list = ['AWS Certified', 'Microsoft Certified', 'Azure Fundamentals']
            certifications = [c for c in certs_list if c.lower() in text.lower()]

    return f"""\
==============================
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
app.geometry("600x500")

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

browse_button = ctk.CTkButton(
    app,
    text="Browse Resume",
    command=browse_file,
    width=200,
    height=40,
    corner_radius=8
)
browse_button.pack(pady=10)

app.mainloop()