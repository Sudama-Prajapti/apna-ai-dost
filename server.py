from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from google import genai
from google.genai import types

app = Flask(__name__)

# 1. Gemini Setup (Aapki real key perfectly active hai)
client = genai.Client(api_key='AQ.Ab8RN6LPNqfv3cAC-HQ_ZqEAJUSF7hlaY8mKukYXCvVCJktkpQ')
SYSTEM_PROMPT = "You are a friendly Indian companion named 'Apna AI Dost'. Speak in Hinglish or casual Hindi. Be empathetic, use terms like 'yaar', 'bhai', 'chill'. Never give medical advice."

def get_gemini_reply(user_message):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_message,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
        )
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Arre yaar, dimaag thoda lag nahi raha peeche se. Dobara bol?"

# 2. Twilio Webhook (Bohot hi simple structure)
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    try:
        # Twilio message ka text 'Body' naam ke parameter me bhejta hai
        user_msg = request.values.get('Body', '')
        print(f"User Said: {user_msg}")
        
        # Gemini se reply lena
        bot_reply = get_gemini_reply(user_msg)
        print(f"AI Replied: {bot_reply}")
        
        # Twilio ke standard format (TwiML) me reply wapas bhejna
        resp = MessagingResponse()
        resp.message(bot_reply)
        
        return str(resp)
    except Exception as e:
        print(f"Twilio Core Error: {e}")
        return str(MessagingResponse().message("Arre yaar, dikkat aa gayi."))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
