import os
from flask import Flask, render_template, request, jsonify
from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

MIRA_API_KEY = os.getenv("MIRA_API_KEY")  # Load API key from .env
client = MiraClient(config={"API_KEY": MIRA_API_KEY})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        if not data or "modelQA" not in data or "studentQuestion" not in data:
            return jsonify({"error": "Invalid request, missing fields"}), 400

        model_qa = data["modelQA"].strip()
        student_question = data["studentQuestion"].strip()

        if not student_question:
            return jsonify({"error": "Student question cannot be empty"}), 400

        # Prepare input for Mira API with correct keys
        flow = Flow(source="autograder.yaml")
        input_dict = {"input1": model_qa, "input2": student_question}

        # Call Mira API
        response = client.flow.test(flow, input_dict)
        print(response)

        return response, 200

    except Exception as e:
        print("🔥 Error:", str(e))  # Print error to the terminal
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Server is running at http://127.0.0.1:5000/")
    app.run(debug=True)
