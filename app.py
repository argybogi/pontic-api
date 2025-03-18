import os
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Ορισμός του path για τη βάση δεδομένων
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DB_PATH = os.path.join(BASE_DIR, "pontic_project.db")  # Σωστή διαδρομή αρχείου

# Συνάρτηση για ανάκτηση τραγουδιών
def get_songs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT title, lyrics, artist, category, source FROM songs")
    songs = [{"title": row[0], "lyrics": row[1], "artist": row[2], "category": row[3], "source": row[4]} for row in cursor.fetchall()]
    conn.close()
    return songs

# Συνάρτηση για ανάκτηση ιστορικών γεγονότων
def get_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT event, description, year, source FROM history")
    history = [{"event": row[0], "description": row[1], "year": row[2], "source": row[3]} for row in cursor.fetchall()]
    conn.close()
    return history

# Route για να ελέγξεις αν το API είναι online
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Pontic API is live!"})

# Endpoint για τα τραγούδια
@app.route('/api/songs', methods=['GET'])
def api_songs():
    return jsonify(get_songs())

# Endpoint για τα ιστορικά γεγονότα
@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify(get_history())

# Εκκίνηση της εφαρμογής
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Χρησιμοποιεί το PORT από το Render
    app.run(host="0.0.0.0", port=port, debug=True)
