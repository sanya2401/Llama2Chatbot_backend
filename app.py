from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


HF_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route('/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"response": "Prompt missing."})

    payload = {"inputs": prompt}
    print(f"Sending to HF: {payload}")

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        print(f"Hugging Face raw response: {response.text}")
        
        result = response.json()

        if isinstance(result, list):
            reply = result[0]["generated_text"][len(prompt):].strip()
        elif isinstance(result, dict) and "error" in result:
            reply = f"HF Error: {result['error']}"
        else:
            reply = "Unknown response format."

    except Exception as e:
        reply = f"Server error: {str(e)}"

    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)  # Important: define port for Render
