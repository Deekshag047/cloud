from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

client = genai.Client(api_key="AIzaSyAM-idtg8OnximRbwyUNPjc-3XETiaQeZw")

def resp(content):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
    return response.text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    try:
        result = resp(user_input)
        return jsonify({"response": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
