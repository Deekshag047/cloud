import requests
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

# Your Gemini API key (please set this as env variable for safety)
GENI_API_KEY = os.environ.get("GEMINI_API_KEY")  # Keep Gemini key as env var

# Hardcoded OpenWeatherMap API key (your provided key)
WEATHER_API_KEY = "1bb7f8ee7780545eedd88449ea4a6827"

# Configure Gemini
if GENI_API_KEY is None:
    raise Exception("Please set GEMINI_API_KEY environment variable!")

genai.configure(api_key=GENI_API_KEY)
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

    if "weather in" in user_input.lower():
        try:
            city = user_input.lower().split("weather in")[-1].strip()

            if not city:
                return jsonify({"reply": "⚠️ Please provide a valid city name."})

            # Capitalize city for better API query
            city = city.title()

            # Optional: Add country code for ambiguous cities (example: Sydney)
            if city.lower() == "sydney":
                city += ",AU"

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

            print(f"🔍 Requesting weather for: {city}")
            print(f"🌐 URL: {url}")

            res = requests.get(url, timeout=5)
            weather_data = res.json()
            print(f"📦 API Response: {weather_data}")

            if weather_data.get("cod") != 200:
                return jsonify({"reply": f"⚠️ Couldn't find weather for '{city}'."})

            weather = weather_data["weather"][0]["description"].capitalize()
            temp = weather_data["main"]["temp"]
            feels = weather_data["main"]["feels_like"]

            reply = f"🌤 Weather in {city}:\n{weather}, {temp}°C (feels like {feels}°C)"
            return jsonify({"reply": reply})

        except requests.exceptions.Timeout:
            print("❌ Weather API timeout")
            return jsonify({"reply": "⚠️ Weather request timed out."})

        except Exception as e:
            print(f"❌ Error fetching weather: {e}")
            return jsonify({"reply": "⚠️ Error fetching weather."})

    try:
        print(f"🤖 Sending to Gemini: {user_input}")
        response = model.generate_content(user_input)
        print(f"🤖 Gemini response: {response.text}")
        return jsonify({"reply": response.text})

    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return jsonify({"error": "Something went wrong with Gemini."}), 500


if __name__ == '__main__':
    app.run(debug=True)
