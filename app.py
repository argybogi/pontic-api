import os
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Ορισμός του path για τη βάση δεδομένων
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DB_PATH = os.path.join(BASE_DIR, "pontic_project.db")  # Σωστή διαδρομή αρχείου

def get_songs():
    conn = sqlite3.connect(DB_PATH)  # Σιγουρευόμαστε ότι ανοίγει σωστά
    cursor = conn.cursor()
    cursor.execute("SELECT title, lyrics, artist, category, source FROM songs")
    songs = [{"title": row[0], "lyrics": row[1], "artist": row[2], "category": row[3], "source": row[4]} for row in cursor.fetchall()]
    conn.close()
    return songs

@app.route('/api/songs', methods=['GET'])
def api_songs():
    return jsonify(get_songs())

@app.route('/api/history', methods=['GET'])
def api_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT event, description, year, source FROM history")
    history = [{"event": row[0], "description": row[1], "year": row[2], "source": row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(history)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
