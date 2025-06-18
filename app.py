from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai

# Load API key from environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize Gemini model (use correct version)
model = genai.GenerativeModel("gemini-1.5-flash")  # You can also try "gemini-pro"

app = Flask(__name__)

# Route for home page (optional: if you have templates/index.html)
@app.route('/')
def home():
    return render_template('index.html')  # You can change this to return plain text if needed

# Route to get response from Gemini
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        response = model.generate_content(user_input)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
