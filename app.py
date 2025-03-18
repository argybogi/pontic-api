from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Pontic API is live!"})

# Συνάρτηση για ανάκτηση τραγουδιών
def get_songs():
    conn = sqlite3.connect("pontic_project.db")  # Αντικατάστησε με PostgreSQL URL αν χρειαστεί
    cursor = conn.cursor()
    cursor.execute("SELECT title, lyrics, artist, category, source FROM songs")
    songs = [{"title": row[0], "lyrics": row[1], "artist": row[2], "category": row[3], "source": row[4]} for row in cursor.fetchall()]
    conn.close()
    return songs

# API διαδρομές
@app.route('/api/songs', methods=['GET'])
def api_songs():
    return jsonify(get_songs())

@app.route('/api/history', methods=['GET'])
def api_history():
    conn = sqlite3.connect("pontic_project.db")
    cursor = conn.cursor()
    cursor.execute("SELECT event, description, year, source FROM history")
    history = [{"event": row[0], "description": row[1], "year": row[2], "source": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(history)

# Εκκίνηση του API
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
