import sqlite3

DATABASE = 'quiz.db'

def create_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Tạo bảng questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        )
    ''')

    # Tạo bảng options
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            option_text TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
    ''')

    # Thêm dữ liệu mẫu
    questions_data = [
        ("Thủ đô của Việt Nam là gì?", "Hà Nội"),
        ("2 + 2 bằng bao nhiêu?", "4"),
        ("Ngôn ngữ lập trình Python được đặt theo tên của ai?", "Monty Python")
    ]

    options_data = [
        (1, "Hà Nội"), (1, "Hồ Chí Minh"), (1, "Đà Nẵng"), (1, "Cần Thơ"),
        (2, "3"), (2, "4"), (2, "5"), (2, "6"),
        (3, "Guido van Rossum"), (3, "Monty Python"), (3, "Dennis Ritchie"), (3, "Linus Torvalds")
    ]

    cursor.executemany("INSERT INTO questions (question_text, correct_answer) VALUES (?, ?)", questions_data)
    cursor.executemany("INSERT INTO options (question_id, option_text) VALUES (?, ?)", options_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
