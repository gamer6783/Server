from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Функція для підключення до бази даних
def connect_db():
    return sqlite3.connect("records.db")

# Створення таблиці (запустіть це один раз перед використанням)
def create_table():
    with connect_db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS records (name TEXT, score INTEGER)")
    print("Database initialized!")

create_table()  # Виконається при запуску сервера

# Отримати топ-10 рекордів
@app.route("/records", methods=["GET"])
def get_records():
    with connect_db() as conn:
        records = conn.execute("SELECT name, score FROM records ORDER BY score DESC LIMIT 10").fetchall()
    return jsonify(records)

# Додати новий рекорд
@app.route("/add_record", methods=["POST"])
def add_record():
    data = request.json
    name, score = data["name"], data["score"]
    with connect_db() as conn:
        conn.execute("INSERT INTO records (name, score) VALUES (?, ?)", (name, score))
        conn.commit()
    return jsonify({"message": "Record added!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
