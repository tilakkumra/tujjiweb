from flask import Flask, request, jsonify
from flask_cors import CORS  # 1. Import CORS
import speech_recognition as sr
import pyttsx3
from google import genai
import time

app = Flask(__name__)
CORS(app)  # 2. Enable CORS for your app

# Note: Keep your API key private in real projects!
client = genai.Client(api_key="AIzaSyBdtttCzK8llDRDohc7RGRZ4fDsijXBp2w")

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    # Note: runAndWait() can sometimes block the Flask response 
    # until the speaking finishes. 
    engine.say(text)
    engine.runAndWait()




def ask_ai(question):  
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=f"""
            You are Tujji, created by Tilak.

            Rules:
            - Answer in ARTICLE format
            - Use simple English
            - Structure:
            1. Title
            2. 2–3 bullet points
            3. One-line conclusion
            - Do not give long paragraphs

            User question: {question}""",
                                      

        )
       
        print("FULL RESPONSE:", response)
        print("AI TEXT:", response.text)



        return response.text 


    except Exception as e:
        print("Error:", e)

        if "429" in str(e):
            return "Too many requests. Please wait a moment."

        return "AI is not available now"
    


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("message")

    print("USER:", question)

    reply = ask_ai(question)

    print("SENDING TO FRONTEND:", reply)  # ✅ IMPORTANT

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Added debug=True so you can see errors in the terminal clearly
    app.run(host='0.0.0.0', port=5000, debug=True)
    time.sleep(2)
