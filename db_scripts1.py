import sqlite3 as sq

# Переменные:
db_name = 'quiz.sqlite'
conn = None
cursor = None

# В других функциях:
def open():
    global conn, cursor
    conn = sq.connect(db_name)
    cursor = conn.cursor()
def do(query):
    cursor.execute(query)
    conn.commit()
def close():
    cursor.close()
    conn.close()   

# Основные функции:
def clear_db():
    open()
    do('DROP TABLE IF EXISTS quiz_content')
    do('DROP TABLE IF EXISTS question')
    do('DROP TABLE IF EXISTS quiz')
    close()
def create():
    open()
    do('PRAGMA foreign_keys = on')
    do('''CREATE TABLE IF NOT EXISTS quiz (id INTEGER PRIMARY KEY, 
        name VARCHAR)''' )
    do('''CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, 
        question VARCHAR, 
        answer VARCHAR, 
        wrong1 VARCHAR, 
        wrong2 VARCHAR, 
        wrong3 VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id))''')
    close()
def add_quiz():
    quizes = [('Викторина 1', ),
        ('Викторина 2', ),
        ('Викторина-непоймикакая', )]
    open()
    cursor.executemany('INSERT INTO quiz (name) VALUES (?)', quizes)
    conn.commit()
    close() 
def add_questions():
    questions = [('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        ('Каким станет зеленый утес, если упадет в Красное море?', 'Мокрым?', 'Красным', 'Не изменится', 'Фиолетовым'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако'),]
    open()
    cursor.executemany('INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)', questions)
    conn.commit()
    close()
def add_links():
    open()
    query = 'INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)'
    for quiz_id in range(1, 4):
        if quiz_id == 1:
            cursor.execute(query, [quiz_id, 1])
            cursor.execute(query, [quiz_id, 2])
        elif quiz_id == 2:
            cursor.execute(query, [quiz_id, 3])
            cursor.execute(query, [quiz_id, 4])
        elif quiz_id == 3:
            cursor.execute(query, [quiz_id, 5])
            cursor.execute(query, [quiz_id, 6])
        conn.commit()
    close()  
def current_question_id(question_id):
    query = '''SELECT id
            FROM quiz_content
            WHERE question_id == (?)'''
    cursor.execute(query, [question_id])
    return cursor.fetchall()[0][0]
def next_question_id(quiz_id, question_id):
    open()
    if question_id == 0:
        query = '''SELECT id
            FROM quiz_content
            WHERE quiz_id == (?)'''
        cursor.execute(query, [quiz_id])
        questions = cursor.fetchall()
        return min(questions[0][0], questions[1][0])
    else:
        if question_id == 6:
            return None
        else:
            query = '''SELECT quiz_id
                FROM quiz_content 
                WHERE id == (?)'''
            cursor.execute(query, [question_id + 1])
            if cursor.fetchall()[0][0] == quiz_id:
                return question_id + 1
            else:
                return None            
    conn.commit()
    close()
def get_question(question_id):
    open()
    if question_id == None:
        return None
    else:
        query = '''SELECT question_id
            FROM quiz_content
            WHERE id == (?)'''
        cursor.execute(query, [question_id])
        question = cursor.fetchall()[0][0]
        query = '''SELECT id, question, answer, wrong1, wrong2, wrong3
            FROM question 
            WHERE id == (?)'''
        cursor.execute(query, [question])
        return cursor.fetchall()
    conn.commit()
    close()
def get_quizes():
    open()
    do('SELECT * FROM quiz ORDER BY id')
    return cursor.fetchall()
    close()

# Сервер:
def main():
    clear_db()
    create()
    add_quiz()
    add_questions()
    add_links()
if __name__ == "__main__":
    main()