from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
merchant_context = {}
conversation_state = {}

@app.route("/v1/healthz", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/v1/metadata", methods=["GET"])
def metadata():
    return jsonify({
        "bot_name": "Simple Vera AI Bot",
        "version": "1.0",
        "description": "Rule-based AI assistant for merchants"
    })

@app.route("/v1/context", methods=["POST"])
def context():
    data = request.json
    context_id = data.get("context_id")
    merchant_context[context_id] = data.get("payload")
    return jsonify({"accepted": True})

@app.route("/v1/tick", methods=["POST"])
def tick():
    # Can be used for time-based logic (keep simple)
    return jsonify({"status": "tick received"})

@app.route("/v1/reply", methods=["POST"])
def reply():
    data = request.json
    
    context_id = data.get("context_id")
    user_message = data.get("message", "").lower()

    merchant = merchant_context.get(context_id, {})

    # Simple AI logic
    offer = "10% discount"

    if "low" in user_message:
        offer = "20% discount to boost footfall"
    elif "festival" in user_message:
        offer = "Special festive combo offer"
    
    response = f"Hey! 🎉 Try this: {offer}. It can help increase engagement!"

    return jsonify({
        "reply": response,
        "actions": [
            {"type": "suggest_offer", "value": offer}
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)