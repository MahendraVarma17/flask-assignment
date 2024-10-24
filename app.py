from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
    conn.commit()
    conn.close()

# Home route to display form and data
@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    all_data = c.fetchall()
    conn.close()
    return render_template('index.html', data=all_data)

# Route to insert data
@app.route('/add', methods=['POST'])
def add_data():
    content = request.form['content']
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO data (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Route to get data as JSON
@app.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    all_data = c.fetchall()
    conn.close()
    return jsonify(all_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)