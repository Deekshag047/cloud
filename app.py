import os
import requests
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Weather API key
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # 🔍 Detect weather-related queries
    if "weather in" in user_input.lower():
        try:
            city = user_input.lower().split("weather in")[-1].strip()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={bd50413ad3bac07f8e6115ebdbc39853}&units=metric"
            res = requests.get(url).json()

            if res.get("cod") != 200:
                return jsonify({"reply": f"⚠️ Couldn't find weather for '{city}'."})

            weather = res["weather"][0]["description"].capitalize()
            temp = res["main"]["temp"]
            feels = res["main"]["feels_like"]
            reply = f"🌤 Weather in {city.title()}:\n{weather}, {temp}°C (feels like {feels}°C)"
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"reply": "⚠️ Error fetching weather."})

    # 🤖 Default: use Gemini
    try:
        response = model.generate_content(user_input)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
