import os
from google import genai

# 1. Apni Gemini API key quotes ke andar set karein
client = genai.Client(api_key='AQ.Ab8RN6LPNqfv3cAC-HQ_ZqEAJUSF7hlaY8mKukYXCvVCJktkpQ')

# 2. AI ke liye system rules (Dost persona aur safety instructions)
system_prompt = """
You are a warm, empathetic, and culturally aware Indian friend and mental health companion. Your name is "Apna AI Dost". 
- Language: Strictly speak in friendly Hinglish (Hindi written in Latin script) or conversational Hindi, depending on how the user inputs.
- Tone: Extremely supportive, calm, non-judgmental, and casual (like a close college friend or mentor). Use words like "yaar", "bhai", "chill", "tension mat le".
- Boundaries: Never give medical prescriptions or heavy psychiatric terms.
- SAFETY RULE: If the user types keywords related to self-harm, suicide, or severe depression (e.g., "mar jana", "suicide", "zindagi khatam"), instantly stop the casual conversation and reply with this exact text: "Yaar, mujhe teri bohot chinta ho rahi hai. Main ek AI hoon aur is waqt shayad teri poori madad na kar paun. Kripya is govt helpline par call kar, wahan log teri madad ke liye hain: KIRAN - 1800-599-0019 (Free & Anonymous)."
"""

def chat_with_dost(user_message):
    try:
        # 3. Google ke sabse naye gemini-3.5-flash model aur Interactions API ka use
        full_input = f"{system_prompt}\n\nUser: {user_message}\nReply in friendly Hinglish:"
        
        interaction = client.interactions.create(
            model="gemini-2.5-flash",
            input=full_input
        )
        return interaction.output_text
    except Exception as e:
        return f"Arre yaar, lagta hai peeche se koi dikkat aa gayi hai: {e}"

# 4. Terminal par live testing loop
print("--- Apna AI Dost Active Hai! (Type 'exit' to stop) ---")
while True:
    user_input = input("\nTum: ")
    if user_input.lower() == 'exit':
        print("Apna AI Dost: Chalo apna khayal rakhna yaar, phir baat karte hain! Bye.")
        break
    
    if not user_input.strip():
        continue
        
    bot_reply = chat_with_dost(user_input)
    print(f"Apna AI Dost: {bot_reply}")
