from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your real HF token
HF_TOKEN = "hf_YourActualTokenHere"

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")

    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    try:
        result = response.json()
        if isinstance(result, list):
            reply = result[0]["generated_text"][len(prompt):].strip()
        else:
            reply = result.get("error", "Sorry, no response.")
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)  # Important: define port for Render
