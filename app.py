"""
Simple Flask Notes Application
Demonstrates docker-compose deployment to Kubernetes with database integration
"""
from flask import Flask, render_template, jsonify, request
import os
import socket
import datetime
import sqlite3
from pathlib import Path

app = Flask(__name__)

# Database setup
DB_PATH = Path('/data/notes.db') if Path('/data').exists() else Path('notes.db')

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Home page with notes list"""
    conn = get_db()
    notes = conn.execute('SELECT * FROM notes ORDER BY updated_at DESC').fetchall()
    conn.close()

    return render_template('index.html',
                         hostname=socket.gethostname(),
                         timestamp=datetime.datetime.now().isoformat(),
                         notes=notes)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat(),
        'database': str(DB_PATH)
    })

@app.route('/api/info')
def info():
    """API endpoint with system info"""
    conn = get_db()
    note_count = conn.execute('SELECT COUNT(*) as count FROM notes').fetchone()['count']
    conn.close()

    return jsonify({
        'app': 'SimpleWebAppPython - Notes',
        'version': '2.0.0',
        'hostname': socket.gethostname(),
        'environment': os.getenv('FLASK_ENV', 'production'),
        'timestamp': datetime.datetime.now().isoformat(),
        'notes_count': note_count
    })

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes"""
    conn = get_db()
    notes = conn.execute('SELECT * FROM notes ORDER BY updated_at DESC').fetchall()
    conn.close()

    return jsonify([dict(note) for note in notes])

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    data = request.json

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400

    conn = get_db()
    cursor = conn.execute(
        'INSERT INTO notes (title, content) VALUES (?, ?)',
        (data['title'], data['content'])
    )
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': note_id, 'message': 'Note created successfully'}), 201

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note"""
    conn = get_db()
    note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
    conn.close()

    if note is None:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify(dict(note))

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a note"""
    data = request.json

    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and content are required'}), 400

    conn = get_db()
    conn.execute(
        'UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        (data['title'], data['content'], note_id)
    )
    conn.commit()
    changes = conn.total_changes
    conn.close()

    if changes == 0:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify({'message': 'Note updated successfully'})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    conn = get_db()
    conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    changes = conn.total_changes
    conn.close()

    if changes == 0:
        return jsonify({'error': 'Note not found'}), 404

    return jsonify({'message': 'Note deleted successfully'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
