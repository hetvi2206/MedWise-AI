from flask import Flask, request, render_template, jsonify
from backend.medicine_extractor import *
from backend.symptoms import *
import json

b, c, d = None, None, None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/image', methods=['POST'])
def solve():
    # Try to get the file from the request
    img = request.files.get('file')
    
    # Check if a file was uploaded
    if img:
        # Call your image processing function here
        annotation = drug_extraction(img)
        print(type(annotation))  # Ensure the annotation is returned correctly
        # Ensure annotation.get_entity_annotations() returns a dictionary
        return jsonify(annotation.get_entity_annotations(return_dictionary=True))
    else:
        # Return an error if no file was uploaded
        return jsonify({"error": "No file uploaded"}), 400

@app.route('/disease', methods=['POST'])
def search():
    global b, c, d
    # Get the symptoms from the request data
    data = request.get_json()['symptoms']
    
    # Process the symptoms using the solver function
    a, b, c, d = solver(data)
    
    # Return the processed result as JSON
    return jsonify(a)

@app.route('/find', methods=['POST'])
def super():
    # Get the symptoms from the request data
    data = request.get_json()['symptoms']
    print(data)
    
    # Process the symptoms and return the response
    return react_out(data, b, c, d)

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True, port=3000)
