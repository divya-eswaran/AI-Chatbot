from flask import Flask, render_template, request, jsonify, session, redirect
import re
import torch
import sqlite3
import os
from datetime import datetime

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
app.secret_key = "secret123"

# ------------------ MONGODB CONNECTION ------------------
MONGO_URI = os.environ.get("MONGO_URI")

if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client["chatbot_db"]
    faq_collection = db["faqs"]
    chat_collection = db["chats"]
    faqs = list(faq_collection.find({}, {"_id": 0}))
else:
    print("⚠️ No MongoDB connected. Using empty FAQ.")
    faqs = []
    chat_collection = None

# ------------------ AI MODELS ------------------
st_model = SentenceTransformer('all-MiniLM-L6-v2')

questions = [faq["question"] for faq in faqs] if faqs else []
question_embeddings = st_model.encode(questions, convert_to_tensor=True) if questions else None

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
llm_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
llm_model = llm_model.to(device)

# ------------------ CLEAN INPUT ------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# ------------------ RULE BASED ------------------
def rule_based_response(user_msg):
    rules = {
        "what is ai": "Artificial Intelligence (AI) enables machines to perform tasks that require human intelligence like learning and decision-making.",
        "what is ml": "Machine Learning (ML) is a subset of AI that allows systems to learn from data.",
        "programming languages": "Examples: Python, Java, C, C++, JavaScript.",
    }

    for key in rules:
        if key in user_msg:
            return rules[key]

    return None

# ------------------ AI RESPONSE ------------------
def ai_response(user_msg):
    prompt = f"""
Answer clearly in 2-3 lines. No repetition.

Question: {user_msg}
Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = llm_model.generate(
        **inputs,
        max_new_tokens=60,
        num_beams=4,
        repetition_penalty=1.2,
        no_repeat_ngram_size=2
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# ------------------ MAIN LOGIC ------------------
def get_response(user_msg):
    user_msg = clean_text(user_msg)

    if len(user_msg.split()) <= 1:
        return "Please ask a proper question"

    # Rule-based
    rule_ans = rule_based_response(user_msg)
    if rule_ans:
        return rule_ans

    # FAQ (only if available)
    if question_embeddings is not None:
        query_embedding = st_model.encode(user_msg, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, question_embeddings)

        best_score = scores.max().item()
        best_idx = scores.argmax().item()

        if best_score >= 0.70:
            return faqs[best_idx]["answer"]

    return ai_response(user_msg)

# ------------------ AUTH (SQLITE) ------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", user=session["user"])


@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"response": "Please login first"})

    user_msg = request.json.get("message")
    response = get_response(user_msg)

    # Save chat only if MongoDB exists
    if chat_collection:
        chat_collection.insert_one({
            "username": session["user"],
            "user": user_msg,
            "bot": response,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({"response": response})

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))