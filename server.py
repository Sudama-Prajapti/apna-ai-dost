from flask import Flask, request, Response
import requests
from google import genai
from google.genai import types

app = Flask(__name__)

# 1. Gemini Setup (Aapki real Key perfectly added hai)
client = genai.Client(api_key='AQ.Ab8RN6LPNqfv3cAC-HQ_ZqEAJUSF7hlaY8mKukYXCvVCJktkpQ')
SYSTEM_PROMPT = "You are a friendly Indian companion named 'Apna AI Dost'. Speak in Hinglish or casual Hindi. Be empathetic, use terms like 'yaar', 'bhai', 'chill'. Never give medical advice."

# 2. WhatsApp Credentials (Aapka naya Token aur ID perfectly added hai)
WHATSAPP_TOKEN = "EAAfZBZAXKpEGQBRzCZAgKHjim3k64EZAjguNVLZA8sl4ZBKPccmfzGRHZC7X43pD5nLIgVqa0r1ZALsXh5PUUlGeycDlQoo3uDmHS1R7SPpEO8mgF1bGxppNizCO2uJl7QLbfAzLpUD2ZA75yzsL7C9Xvfa4Wb2y9q1POTqZA2DEpfkV3hZBqqbqdnhcixUDo4ZBznpf8zni6qZB1ZBudvv4gZBdvJn8a2Dp8VswHk15rn8kUUW7Xjlg1ZAsFYrVwZBZCdHNO4hNxgZAhr8jLpgJcj6HjZAzEKDvtLMk"
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
        print(f"Gemini API Crash Status: {e}")
        return "Arre yaar, dimaag thoda lag nahi raha peeche se. Dobara bol?"

def send_whatsapp_message(to_number, text_message):
    # ✅ FIXED: Meta Graph API ka absolute aur correct URL format lagaya gaya hai
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
        print(res.text) # Isse terminal me dikhega ki reply send hua ya fail
    except Exception as e:
        print(f"Error while triggering Meta Graph API: {e}")

# Webhook Verification Engine (GET Request)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == "my_secret_token_123":
        return Response(challenge, mimetype="text/plain", status=200)
    
    return Response("Verification Failed", status=403)

# Webhook Message Receiver (POST Request)
@app.route("/webhook", methods=["POST"])
def receive_message():
    body = request.get_json()
    print(f"\n--- INCOMING RAW DATA FROM META CHANNELS ---")
    print(body) # Isse confirm hoga ki message server tak aaya
    
    try:
        # ✅ FIXED: Loop mapping lagakar deep arrays ko foolproof parse kiya gaya hai
        if body.get("entry"):
            for entry in body["entry"]:
                if entry.get("changes"):
                    for change in entry["changes"]:
                        value = change.get("value", {})
                        if "messages" in value and value["messages"]:
                            # Fetching the first actual message array object safely
                            message_list = value["messages"]
                            if len(message_list) > 0:
                                message_data = message_list[0]
                                from_number = message_data["from"]
                                
                                if "text" in message_data:
                                    user_text = message_data["text"]["body"]
                                    print(f"User Phone: {from_number} | Msg: {user_text}")
                                    
                                    # Gemini AI se reply fetch karna
                                    bot_reply = get_gemini_reply(user_text)
                                    print(f"AI Responded: {bot_reply}")
                                    
                                    # Reply message user ko trigger karna
                                    send_whatsapp_message(from_number, bot_reply)
    except Exception as e:
        print(f"Deep JSON Matrix Parsing Exception Error: {e}")
        
    return Response("SUCCESS", status=200)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
