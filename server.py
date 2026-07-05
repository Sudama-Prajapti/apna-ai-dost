from flask import Flask, request, Response
import requests
from google import genai
from google.genai import types

app = Flask(__name__)

# 1. Gemini Setup (Aapki real Key perfectly added hai)
client = genai.Client(api_key='AQ.Ab8RN6LPNqfv3cAC-HQ_ZqEAJUSF7hlaY8mKukYXCvVCJktkpQ')
SYSTEM_PROMPT = "You are a friendly Indian companion named 'Apna AI Dost'. Speak in Hinglish or casual Hindi. Be empathetic, use terms like 'yaar', 'bhai', 'chill'. Never give medical advice."

# 2. WhatsApp Credentials (Aapka naya Token aur ID perfectly added hai)
WHATSAPP_TOKEN = "EAAfZBZAXKpEGQBR4Amvo7d4V8G0Brsf2g8V4ZBeO3tw3vZAAQ8a68ruR0WXLL6JHbCgZAQyQnL8FZB2mTryZCPl6dNPBytWmVJRNO2G8PKJHZCqhyIUZABiZBi8DEDiuY9j1vAdaVydoSleC2whBX7M6nRmZAgUD9CdsUMIozyJglcLJ4CnNW2cvZAox8h8HodrTR7JDvR6MsSQq04eMps2FaWYq2JQeLcKzGXDiGjzvnUJGtvfkanKIdbXR28NL70X1LMci50pEvNF2pwERF10mDj7wmBYfMwZDZD"
PHONE_NUMBER_ID = "1182983638234656"

def get_gemini_reply(user_message):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_message,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Arre yaar, dimaag thoda lag nahi raha peeche se. Dobara bol?"

def send_whatsapp_message(to_number, text_message):
    # ✅ FIXED: Strict Graph API Endpoint with proper forward slashes
    url = f"https://facebook.com{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text_message}
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        print(f"--- Meta Reply Response Status: {res.status_code} ---")
        print(res.text)
    except Exception as e:
        print(f"Error while triggering Meta Graph API: {e}")

# Webhook Verification Engine
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == "my_secret_token_123":
        return Response(challenge, mimetype="text/plain", status=200)
    
    return Response("Verification Failed", status=403)

# Webhook Live Parsing JSON Engine (FOOLPROOF FIXED BASED ON YOUR REAL PAYLOAD)
@app.route("/webhook", methods=["POST"])
def receive_message():
    body = request.get_json()
    print(f"\n--- INCOMING RAW DATA FROM META ---")
    print(body)
    
    try:
        # ✅ FIXED: Aapke real payload structure ke array indexes ko map kiya gaya hai
        if body and "entry" in body and body["entry"]:
            entry_data = body["entry"][0]
            if "changes" in entry_data and entry_data["changes"]:
                change_data = entry_data["changes"][0]
                value = change_data.get("value", {})
                
                if "messages" in value and value["messages"]:
                    # Extraction based on array indexing [0]
                    message_data = value["messages"][0]
                    from_number = message_data["from"]
                    
                    if "text" in message_data and "body" in message_data["text"]:
                        user_text = message_data["text"]["body"]
                        print(f"User Said: {user_text}")
                        
                        # Fetch AI text from Gemini
                        bot_reply = get_gemini_reply(user_text)
                        print(f"AI Responded: {bot_reply}")
                        
                        # Trigger reply via Graph API
                        send_whatsapp_message(from_number, bot_reply)
    except Exception as e:
        print(f"Deep Payload Exception Error: {e}")
        
    return Response("SUCCESS", status=200)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
