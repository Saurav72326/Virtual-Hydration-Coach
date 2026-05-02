from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
#from dotenv import load_dotenv
import os

#load_dotenv()

api_key = os.getenv("API_KEY")

app = Flask(__name__)

genai.configure(api_key="AIzaSyAzD-SDAnF_jsVEeD19-UmJgvFw1gA8ktA")

model = genai.GenerativeModel("gemini-flash-latest")

SYSTEM_PROMPT = """
You are a virtual Hydration Coach.

Rules:
- Only answer hydration-related questions.
- Reject unrelated questions politely.
- Give clear and friendly answers.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message")
        history = data.get("history", [])

        chat_history = [
            {"role": "user", "parts": [SYSTEM_PROMPT]},
            {"role": "model", "parts": ["Got it. I am your Hydration Coach."]}
        ]

        for msg in history:
            chat_history.append({
                "role": msg["role"],
                "parts": [msg["parts"]]
            })

        chat_history.append({
            "role": "user",
            "parts": [user_message]
        })

        response = model.generate_content(chat_history)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)