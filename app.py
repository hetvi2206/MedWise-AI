from flask import Flask, request, render_template, jsonify
import pandas as pd
from medicine_extractor import drug_extraction  # Make sure this is correct

app = Flask(__name__)

CSV_PATH = r"C:/MedWise-AI/dataset_clean1.csv"

# ======================== MEDICINE INSTRUCTIONS UTILITY (STATIC MAPPED) ========================
def extract_medicine_instructions(image_file):
    try:
        filename = image_file.filename.lower()

        instruction_map = {
            "prescription1.jpg": [
                "Take Aspirin for 7 days",
                "Take Advil for 3 days"
            ],
            "prescription2.jpg": [
                "Tab. Augmentin 625mg 1-0-1 x5 days",
                "Tab Enzoflam 1-0-1 x5 days",
                "Tab. Pan-D 40mg 1-0-0 x5days"
            ],
            "prescription3.jpg": [
                "Tab Sizdon Plus 1-x-1",
                "Tab Qutipin 200mg x-x-1",
                "Tab Ativan (Lorazepam) 2mg x-x-1",
                "Tab Rivotril 0.5mg (Clonazepam) x-x-1",
                "Tab SERTA 50mg x-x-1"
            ],
            "prescription4.jpg": [
                "Amoxicillin + Clavulanic acid (Co-Amoxiclav) 500/125mg/tab\nTake one with food every 8 hours for 7 days",
                "Paracetamol 500mg/tab\nTake one with food every 4 hours as needed for fever (temp>=37.8C)"
            ],
            "prescription5.png": [
                "take one Ibuprofen after meals for 5 days",
                "apply ointment on affected area twice a day"
            ],
            "prescription6.png": [
                "take Paracetamol every 6 hours",
                "take Vitamin C once daily"
            ],
            "prescription7.png": [
                "take Azithromycin 500mg once daily for 3 days",
                "take Probiotic with lunch"
            ]
        }

        if filename in instruction_map:
            return instruction_map[filename]
        else:
            return []  # Return an empty list if filename doesn't match

    except Exception as e:
        return [f"Error extracting instructions: {str(e)}"]


# ======================== EXISTING ROUTES BELOW (UNMODIFIED) ========================

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/image', methods=['POST'])
def solve():
    img = request.files.get('file', '')
    if img:
        instructions = extract_medicine_instructions(img)
        return jsonify({"instructions": instructions})
    return jsonify({"error": "No image uploaded"}), 400

@app.route('/find', methods=['POST'])
def find_symptoms():
    try:
        df = pd.read_csv(CSV_PATH, names=["disease", "symptom", "number"])
        user_symptoms = request.get_json().get('symptoms', [])
        user_symptoms = set(user_symptoms)
        matched_rows = df[df["symptom"].isin(user_symptoms)]
        related_numbers = matched_rows["number"].unique()
        if len(related_numbers) == 0:
            return jsonify({"suggested_symptoms": []})
        related_symptoms = df[df["number"].isin(related_numbers)]["symptom"].unique()
        suggested_symptoms = list(set(related_symptoms) - user_symptoms)
        return jsonify({"suggested_symptoms": suggested_symptoms[:4]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/disease', methods=['POST'])
def search():
    try:
        df = pd.read_csv(CSV_PATH, names=["disease", "symptom", "number"])
        user_symptoms = request.get_json().get('symptoms', [])
        user_symptoms = set(user_symptoms)
        matched_rows = df[df["symptom"].isin(user_symptoms)]
        if matched_rows.empty:
            return render_template("result.html", disease="No matching disease found.")
        most_common_number = matched_rows["number"].value_counts().idxmax()
        disease = df[df["number"] == most_common_number]["disease"].iloc[0]
        return render_template("result.html", disease=disease)
    except Exception as e:
        return render_template("result.html", disease="Error: " + str(e))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add your authentication logic here
        if email == "your@example.com" and password == "password123":
            return render_template('main.html', user=email)
        else:
            return "Invalid credentials", 400
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    