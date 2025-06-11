from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HF_TOKEN = "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"  
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"response": "Please enter a prompt."})

      
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        print("HF RAW RESPONSE:", response.text)

        try:
            result = response.json()
        except Exception as parse_error:
            return jsonify({"response": f"HF returned invalid JSON: {parse_error} | Raw: {response.text}"})

        # Return proper reply
        if isinstance(result, list):
            reply = result[0].get("generated_text", "").replace(prompt, "").strip()
        elif "error" in result:
            reply = f"HuggingFace error: {result['error']}"
        else:
            reply = "Unexpected response structure."

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Server error: {str(e)}"})
