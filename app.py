from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

chatbot = pipeline("text-generation", model="gpt2")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"response": "Please enter a message."})

    result = chatbot(prompt, max_new_tokens=50, do_sample=True)[0]["generated_text"]
    reply = result[len(prompt):].strip()
    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run()
