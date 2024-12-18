from flask import Flask, request, jsonify
import openai
import speech_recognition as sr
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI GPT settings
openai.api_key = 'your-openai-api-key'

# Database setup
def init_db():
    conn = sqlite3.connect('language_learner.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE,
                      language_level TEXT,
                      preferences TEXT)''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register_user():
    # Register a new user
    username = request.json.get('username')
    initial_language_level = request.json.get('language_level', 'beginner')
    preferences = request.json.get('preferences', '')
    
    conn = sqlite3.connect('language_learner.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO users (username, language_level, preferences) 
                          VALUES (?, ?, ?)''', (username, initial_language_level, preferences))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'message': 'User already exists'}), 400
    finally:
        conn.close()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/conversation', methods=['POST'])
def conversation():
    # Process a conversation between user and AI
    user_input = request.json.get('message')
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=user_input,
      max_tokens=150
    )
    return jsonify({'response': response.choices[0].text.strip()})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
