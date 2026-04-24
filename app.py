from flask import Flask, render_template, request, jsonify, session, redirect
import re
import torch
import sqlite3
from datetime import datetime

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
app.secret_key = "secret123"

# ------------------ SQLITE ------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ------------------ MONGODB (LOCAL ONLY) ------------------
try:
    client = MongoClient("mongodb://127.0.0.1:27017")  # FORCE LOCAL

    db = client["chatbot_db"]
    chat_collection = db["chats"]
    faq_collection = db["faqs"]

    faqs = list(faq_collection.find({}, {"_id": 0}))

    print("✅ Connected to LOCAL MongoDB")
    print("📂 DB:", db.name)

except Exception as e:
    print("❌ MongoDB Connection Error:", e)
    chat_collection = None
    faqs = []

# ------------------ MODEL ------------------
print("🔄 Loading models...")
st_model = SentenceTransformer('all-MiniLM-L6-v2')

questions = [faq["question"] for faq in faqs] if faqs else []
question_embeddings = st_model.encode(questions, convert_to_tensor=True) if questions else None

model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
llm_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
llm_model = llm_model.to(device)

# ------------------ CLEAN TEXT ------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

# ------------------ RULE BASE ------------------
def rule_based_response(user_msg):
    rules = {
        "what is ai": "Artificial Intelligence enables machines to think and learn.",
        "what is c": "C is a procedural programming language.",
        "what is http": "HTTP is used for web communication."
    }

    for key in rules:
        if key in user_msg:
            return rules[key]

    return None

# ------------------ AI RESPONSE ------------------
def ai_response(user_msg):
    prompt = f"Answer clearly in 2 lines:\nQuestion: {user_msg}\nAnswer:"

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = llm_model.generate(
        **inputs,
        max_new_tokens=60,
        num_beams=4,
        repetition_penalty=1.3
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    return answer if len(answer.split()) > 2 else "Try asking differently."

# ------------------ MAIN LOGIC ------------------
def get_response(user_msg):
    user_msg = clean_text(user_msg)

    if len(user_msg.split()) <= 1:
        return "Please ask a proper question"

    rule_ans = rule_based_response(user_msg)
    if rule_ans:
        return rule_ans

    if question_embeddings is not None:
        query_embedding = st_model.encode(user_msg, convert_to_tensor=True)
        scores = util.cos_sim(query_embedding, question_embeddings)

        best_score = scores.max().item()
        best_idx = scores.argmax().item()

        if best_score >= 0.70:
            return faqs[best_idx]["answer"]

    return ai_response(user_msg)

# ------------------ AUTH ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            return render_template("register.html", error="User exists")

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
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ------------------ HOME ------------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# ------------------ CHAT ------------------
@app.route("/chat", methods=["POST"])
def chat():
    print("\n🔥 /chat HIT")

    if "user" not in session:
        return jsonify({"response": "Please login first"})

    data = request.get_json()
    user_msg = data.get("message")

    response = get_response(user_msg)

    print("USER:", user_msg)
    print("BOT:", response)

    # ------------------ SAVE TO MONGO ------------------
    try:
        if chat_collection is not None:
            result = chat_collection.insert_one({
                "username": session["user"],
                "user": user_msg,
                "bot": response,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            print("📥 INSERTED ID:", result.inserted_id)

            total = chat_collection.count_documents({})
            print("📊 TOTAL DOCS IN DB:", total)

        else:
            print("❌ chat_collection is None")

    except Exception as e:
        print("❌ INSERT ERROR:", e)

    return jsonify({"response": response})

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)