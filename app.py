from flask import Flask, render_template, request, jsonify
import random
import sqlite3

app = Flask(__name__)

DATABASE = 'quiz.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Để truy cập cột theo tên
    return conn

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_random_questions(num_questions):
    questions = query_db("SELECT id, question_text, correct_answer FROM questions")
    if num_questions > len(questions):
        num_questions = len(questions)
    return random.sample(questions, num_questions)

def get_options(question_id):
    return query_db("SELECT option_text FROM options WHERE question_id = ?", (question_id,))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    num_questions = int(request.form['num_questions'])
    questions = get_random_questions(num_questions)
    quiz_data = []
    for question in questions:
        options = [row['option_text'] for row in get_options(question['id'])]
        random.shuffle(options)  # Xáo trộn đáp án
        quiz_data.append({
            'id': question['id'],
            'question_text': question['question_text'],
            'options': options,
            'correct_answer': question['correct_answer']  # Để kiểm tra sau này
        })
    return jsonify(quiz_data)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answers = request.get_json()
    score = 0
    for answer in answers:
        question = query_db("SELECT correct_answer FROM questions WHERE id = ?", (answer['question_id'],), one=True)
        if question and answer['selected_answer'] == question['correct_answer']:
            score += 1
    return jsonify({'score': score, 'total': len(answers)})

if __name__ == '__main__':
    app.run(debug=True)
