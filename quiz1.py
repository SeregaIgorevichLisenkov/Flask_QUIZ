import os
from random import shuffle
from flask import Flask, redirect, url_for, session, request, render_template
from db_scripts1 import next_question_id, get_question, get_quizes, current_question_id

# Переменные:
def create_session(quiz_id = None):
    session['quiz_id'] = quiz_id
    session['question_id'] = 0
    session['correct_answer'] = None
    session['ready_answers'] = None
    session['score'] = 0
    session['answers_list'] = []

# Проверка ответов:
def check_answer(answer):
    if answer == session['correct_answer']:
        session['score'] += 1

# Функции View:
def index():
    if request.method == 'GET':
        create_session()
        return render_template('index.html', quizes = get_quizes())
    if request.method == 'POST':     
        create_session(int(request.form.get('quiz')))
        session['ready_answers'] = 0
        return redirect(url_for('test'))
def test():
    if not ('quiz_id' in session):
        return redirect(url_for('index'))
    else:
        if session['quiz_id'] == None:
            return redirect(url_for('index'))
        else:
            if request.method == 'GET':
                question = get_question(next_question_id(session['quiz_id'], session['question_id']))
                if question == None:
                    return redirect(url_for('result'))
                else:
                    session['correct_answer'] = question[0][2]
                    session['answers_list'] = []
                    for i in question[0][2:]:
                        session['answers_list'].append(i)
                    shuffle(session['answers_list'])
                    return render_template('test.html', id = current_question_id(question[0][0]), question = question[0][1], answers = session['answers_list'])
            if request.method == 'POST':
                session['ready_answers'] += 1
                session['question_id'] = int(request.form.get('question_id'))
                check_answer(request.form.get('answer'))
                return redirect(url_for('test')) 
def result():
    if not ('ready_answers' in session):
        return redirect(url_for('index'))
    else:
        if session['ready_answers'] == None:
            return redirect(url_for('index'))
        else:
            return render_template('result.html', score = session['score'], ready_answers = session['ready_answers'])            

# Приложение и Странички:
folder = os.getcwd()
app = Flask(__name__, template_folder = folder, static_folder = folder)
app.config['SECRET_KEY'] = 'Khorevich13'
app.add_url_rule('/', 'index', index, methods = ['GET', 'POST'])
app.add_url_rule('/test', 'test', test, methods = ['GET', 'POST'])
app.add_url_rule('/result', 'result', result)
if __name__ == "__main__":
    # app.run(host = ('0.0.0.0'))
    app.run()